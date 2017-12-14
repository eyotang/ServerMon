# -*- coding: utf-8 -*-

import os

class Del_Old_File(object):
    def __init__(self, directory):
        self.directory = directory

    def del_old_file(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            return

        for f in os.listdir(self.directory):
            os.unlink(os.path.join(self.directory, f))
