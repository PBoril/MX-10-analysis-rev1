# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 21:03:54 2022

@author: pbori
"""
import os
from tkinter import filedialog
from tkinter import messagebox as mb


def LoadConfigPath():
    Pfile=open("Config.txt","r")
    ReadStr=Pfile.read()
    Pfile.close()
    return ReadStr[19:]


def CreateConfigFile(path):
    Cfile=open("Config.txt", "w")
    Cfile.write("\nLoad Folder Path = "+path+"/")
    Cfile.close()
    
def SelectFolder():
    path = filedialog.askdirectory()
    return path



def ReplaceLineConfig(Line, Str):
    with open("Config.txt", "r") as Read:
        lines = [line.rstrip() for line in Read]
    lines[Line]=Str
    Write=open("Config.txt", "w")
    for k in range (len(lines)):
        Write.write(lines[k])
    Write.close()
        