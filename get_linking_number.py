# coding:utf-8
#__author__ = 'Libiao'

import subprocess

class GetLinkingNumber(object):
    def __init__(self):
        pass

    def getLinkingNumber(serlf,servers):
        ret = []
        if isinstance(servers,str):
            num = subprocess.Popen("netstat -tnap | grep tcp | grep %s | wc -l" %servers,stdout=subprocess.PIPE,shell=True).stdout
            ret.append(int(num.readline().strip()))
        elif isinstance(servers,dict):
            for k,v in servers.items():
                num = subprocess.Popen("netstat -tnap | grep tcp | grep %s | wc -l" %v,stdout=subprocess.PIPE,shell=True).stdout
                ret.append(int(num.readline().strip()))
        else:
            pass
        return ret
