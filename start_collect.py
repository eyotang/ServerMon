#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
reated on 2015年10月16日

@author: LiBiao
"""

import os, sys, traceback, signal
import time
import subprocess
import multiprocessing
from write_log import writeLog
import del_old_file
from record_test_data import Record_Data
from server_memory_collect import serverMemoryCollect
from get_linking_number import GetLinkingNumber

#需要手动设置的参数
SERVERS_D = {'1935':'srs-rtmp','18080':'srs-hls','80':'nginx'} #可以输入srs或者nginx或者ATS

#间隔时间
INTERVAL_TIME = 10


class KPI_Collect(object):
    def __init__(self):
        self.getLinkNum = GetLinkingNumber()
        self.TCP_COUNT = self.getLinkNum.getLinkingNumber(SERVERS_D)
        self.tcpRecord = Record_Data("res/linking_number")

    def getStr(self,alist):
        ret = ""
        for s  in alist:
            ret += str(s)
            ret += ' '
        return [ret.rstrip(' ')]

    #通过调用collect.sh脚本来执行服务器性能数据采集
    def sys_kpi_collect(self):
        flag = '1'
        cmds = ['./collect.sh']
        popen = subprocess.Popen(cmds[0],stdout=subprocess.PIPE,shell=True)
        pid = popen.pid
        writeLog('INFO','>>>>> 性能指标采集进程执行中.....')
        self.to_stop_subprocess(flag,popen)

    #停止sys_kpi_collect执行的程序的popen句柄
    def to_stop_subprocess(self,flag,popen):
        curr_tcpnum = self.getLinkNum.getLinkingNumber(SERVERS_D)
        self.tcpRecord.recordData(["srs&nginx Linking","%s %s %s" %tuple(SERVERS_D.values()),"Time(s) Numbers"])
        self.tcpRecord.recordData(self.getStr(self.TCP_COUNT))
        if flag is '1':
            loops = 0
            while True:
                if sum(curr_tcpnum) <= sum(self.TCP_COUNT):
                    if loops == 15:
                        #15s内当前连接数小于初始化连接数，退出程序
                        #删除还存在于系统中的sar和iostat进程
                        names = ['sar','iostat']
                        cmd = "killall -9 %s %s" %tuple(names)
                        subprocess.call(cmd,shell=True)
                        #终止子进程
                        popen.kill()
                        if subprocess.Popen.poll(popen) is not None:
                            break
                        else:
                            writeLog("INFO",r">>>>> 等待子进程终止")
                    else:
                        loops += 5
                        time.sleep(5)
                else:
                    loops = 0
                    time.sleep(INTERVAL_TIME)#等待INTERVAL_TIME时间
                curr_tcpnum = self.getLinkNum.getLinkingNumber(SERVERS_D)
                self.tcpRecord.recordData(self.getStr(curr_tcpnum))
            writeLog("INFO",r">>>>> 性能指标采集完成")
        else:
            while True:
                if subprocess.Popen.poll(popen) is not None:
                    break
                else:
                    writeLog("INFO",r">>>>> 等待子进程终止")
            writeLog("INFO",r">>>>> 性能指标采集完成")


    #判断系统中是否还存留sar和iostat进程
    def is_process_exists(self,name):
        cmd = "ps ax | grep %s | grep -v grep" %name
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
        p.wait()
        if p.stdout.readline():
            return 1
        return 0


    def main_start(self):
        start_times = 0.0
        timeRecord = Record_Data("res/timeConsum")
        for server,num in zip(SERVERS_D.values(),self.TCP_COUNT):
            writeLog("INFO",r">>>>> 初始 %s 服务连接数 %d" %(server,num))
        curr_tcpN = self.getLinkNum.getLinkingNumber(SERVERS_D)
        time.sleep(10)
        while True:
            if not sum(curr_tcpN) <= sum(self.TCP_COUNT):
                start_times = time.time()
                global g_starttime
                g_starttime = start_times
                for server,num in zip(SERVERS_D.values(),curr_tcpN):
                    writeLog("INFO",r">>>>> 指标采集任务开始，当前 %s 连接数 %d" %(server,num))

                #删除旧的kpi文件
                del_old_file.Del_Old_File("res/").del_old_file()
                #单独线程执行其他服务（srs、nginx等）进程内存指标采集任务
                for port,server in SERVERS_D.items():
                    multiprocessing.Process(target=serverMemoryCollect,
                                            args=([port,server],
                                                  INTERVAL_TIME,
                                                  sum(self.TCP_COUNT),
                                                  self.getLinkNum)).start()

                #采集服务器系统kpi指标
                self.sys_kpi_collect()

                writeLog("INFO",r">>>>> 性能数据采集结束！")
                time_consum = time.time() - start_times
                timeRecord.recordData([str(time_consum)])
                break
            else:
                time.sleep(1)
            curr_tcpN = self.getLinkNum.getLinkingNumber(SERVERS_D)


g_starttime = time.time()
def onsignal_int(signum, frame) :
    time_consum = time.time() - g_starttime
    timeRecord = Record_Data("res/timeConsum")
    timeRecord.recordData([str(time_consum)])
    print ("\nReceive SIGINT[Ctrl+C] to stop process by force !")
    sys.exit(-1)

def register_signal() :
    signal.signal(signal.SIGINT, onsignal_int)

def main():
    register_signal()

    kpiCollect = KPI_Collect()
    kpiCollect.main_start()


if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception as e :
        traceback.print_exc(file = sys.stderr)
        sys.exit(2)
