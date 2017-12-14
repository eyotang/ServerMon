#-*- coding:utf-8 -*-

"""
reated on 2015年10月16日

@author: LiBiao
"""

import time
import subprocess
from write_log import writeLog
from record_test_data import Record_Data

#Record the memory of server used
def serverMemoryCollect(servers,intervaltime,tcpNum,getLinkObj):
    getLinkNum = getLinkObj
    memRecord = Record_Data("res/%s" %(servers[1]+":"+servers[0]))
    cmd = "ps -ef | grep %s | grep -v grep | awk \'{print $2}\'" %servers[1]
    (status_code, lines) = subprocess.getstatusoutput(cmd)
    writeLog("INFO",">>>>> %s 指标采集进程执行中....." %servers[1])
    if not lines:
        return -1

    pids = lines.split("\n")

    heard = [servers[1],'used','Linking_Number Memory_Capacity(MB)']
    try:
        memRecord.recordData(heard)
        curr_tcpN = sum(getLinkNum.getLinkingNumber(servers[0]))
        loops = 0
        while True:
            vrss = []
            for pid in pids:
                cmd2 = "cat /proc/%s/status | grep VmRSS | awk \'{print $2}\'" %(pid)
                (status_code, result) = subprocess.getstatusoutput(cmd2)
                vrss.append(int(result))
            memRecord.recordData([str(sum(vrss)/1024)])
            if curr_tcpN <= tcpNum:
                if loops == 15:
                    #15s之内，当前连接数小于初始化连接数，程序退出
                    break
                else:
                    loops += 5
                    time.sleep(5)
            else:
                loops = 0
                time.sleep(intervaltime)
            curr_tcpN = sum(getLinkNum.getLinkingNumber(servers[0]))

        writeLog("INFO",r">>>>> %s 进程内存采集完成" %servers[1])
    except IOError as err:
        writeLog("INFO","File error: " + str(err))
        return 0
