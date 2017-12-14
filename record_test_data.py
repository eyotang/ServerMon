#-*- coding:utf-8 -*-
import os

class Record_Data(object):
    def __init__(self, filepath):
        filedir = os.path.dirname(filepath)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        self.filepath = filepath

    def recordData(self, data):
        print(data)
        with open(self.filepath, 'a') as f:
            if isinstance(data, list):
                for content in data:
                    f.write(content)
                    f.write("\n")
            else:
                f.write(data)
                f.write("\n")
        f.close()
