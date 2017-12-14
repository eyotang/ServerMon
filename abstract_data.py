#!/usr/bin/env python
# -*- coding: utf-8 -*-   
'''
Created on 2015年9月14日

@author: LiBiao
'''

import os,time
import subprocess
import getCmds
import del_old_file
from write_log import writeLog


#需要手动配置的数据
#SERVER_NAME = ['srs_2.0.0.','nginx']#'nginx'    #可以输入nginx或者srs
SERVERS_D = {'1935':'srs-rtmp','18080':'srs-hls','80':'nginx'}

#系统语言编码
LANG = "en_US.UTF-8"

#获取系统当前使用的语言
def getSysLANG():
    popen = subprocess.Popen('echo $LANG',stdout=subprocess.PIPE,shell=True)
    return popen.stdout.read().strip()

# 根据系统语言编码获取对应配置文件路径
def getConfPath():
    if getSysLANG() == LANG:
        return "./conf/abstractConf_en.xml"
    return "./conf/abstractConf_ch.xml"

class AbstractKPI(object):
    def __init__(self,*args):
        (self.cmds,) = args

    def abstract_kpi(self):
        for cmd in self.cmds:
            # print cmd
            subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)


#获取本机ip地址，用来产生区别于其他机器的数据
def get_local_ip():
    try:
        ip = os.popen("ifconfig | grep 'inet addr' | awk '{print $2}'").read()
        ip = ip[ip.find(':') + 1:ip.find('\n')]
    except Exception,e:
        print e
    return ip

#将最终采集数据打包
def to_tar():
    ip = get_local_ip()
    times = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())
    subprocess.call("cp res/linking_number res/timeConsum " +"res/%s "*len(SERVERS_D.items()) %tuple([v + "\:" + k for k,v in SERVERS_D.items()]) + "result/",shell=True)
    files = ["result/" + filename for filename in os.listdir("result/")]
    cmd = 'tar -cf SYS_KPI_'+ ip + "_" + times + '.tar' + ' %s'*len(files) %tuple(files)
    try:
        subprocess.call(cmd,shell=True)
    except Exception as err:
        writeLog("ERROR",r">>>>> 文件压缩出现错误 %s" %str(err))
        exit()

    writeLog("INFO",r">>>>> 指标文件打包完成")


#脚本主入口函数
def main_start():
    #删除旧的kpi文件
    del_old_file.Del_Old_File("result/").del_old_file()

    #获取到配置文件路径
    confpath = getConfPath()

    #调用getCmds获取解析kpi文件的命令
    cmds = getCmds.Get_Cmds(confpath).getcmds()

    #从原始指标文件提取有用的数据
    AbstractKPI(cmds).abstract_kpi()

    #将result目录下的解析后的kpi文件打包
    to_tar()
    writeLog("INFO",r">>>>> 指标数据提取并打包完成")

if __name__ == '__main__':
    main_start()
