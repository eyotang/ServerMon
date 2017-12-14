# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

class Get_Cmds(object):
    def __init__(self, filepath):
        self.root = ET.parse(filepath).getroot()

    def getcmds(self):
        cmds = []
        for child in self.root.findall("res_file"):
            orgFile = child.attrib.get("name")
            uniqFlag = child.find("uniqflag").text
            tgtFile = child.find("object_file").text
            graphTitle = child.find("graphtitle").text
            lineLabel = child.find("linelabel").text
            xylabel = child.find("x_y_label").text
            cmd = child.find("cmd").text

            cmd = cmd %(orgFile, uniqFlag, graphTitle, lineLabel, xylabel, tgtFile)
            cmds.append(cmd)
        return cmds
