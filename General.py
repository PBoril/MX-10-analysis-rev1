# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 19:34:36 2022

@author: pbori
"""
import os
from tkinter import filedialog
from tkinter import messagebox as mb

"make array from file"
def LoadFile(path):
    FileArray=[]
    SourceFile=open(path, "r")
    for line in SourceFile:
        FileArray.append([float(x) for x in line.split()])
    SourceFile.close()
    return FileArray

"Create list of files in one folder"
def FilesList(folder):
    FilesRegistry=[]
    for path in os.listdir(folder):
        FilesRegistry.append(folder+path)
    return FilesRegistry
def ExportObjectsList(ObjectRegister, path):
    with open(path, "w") as file:
        for row in ObjectRegister:
            file.write(" ".join([str(item) for item in row]))
            file.write("\n")
def SeparateObjects(InputData):
    Support=[]
    Output=[]
    ObjectsArray=[]
    R=len(InputData)
    C=len(InputData[0])
    for i in range(R+2):
        temp1=[]
        for j in range (C+2):
            temp1.append(0)
        Support.append(list(temp1))

    for i in range(R+2):
        temp2=[]
        for j in range (C+2):
            temp2.append(0)
        Output.append(list(temp2))
    for i in range(R):
        for j in range(C):
            if InputData[i][j]!=0:
                Support[i+1][j+1]=1
    for i in range(R):
        for j in range(C):
            if InputData[i][j]!=0:
                Support[i+1][j+1]=1
    for i in range(R):
        temp3=[]
        for j in range(C):
            temp3.append(0)
        ObjectsArray.append(list(temp3))
    ObjectN=0
    detection=1
    ObjectN=1
    Hit=1
    while detection!=0:
        detection=0
        Found=0
        for i in range (R):
            for j in range(C):                
                x=i+1
                y=j+1
            
                if Found==0:
                    if Support[x][y]==1:
                        Support[x][y]=2
                        detection=1
                        Found=1
        while ObjectN!=0:
                ObjectN=0
                for i in range (R):
                    for j in range(C):
                        x=i+1
                        y=j+1
                        if Support[x][y]==2:
                    
                            if Support[x-1][y-1]==1:
                                Support[x-1][y-1]=2
                                ObjectN=1
                            
                            if Support[x-1][y]==1:
                                Support[x-1][y]=2
                                ObjectN=1
                            
                            if Support[x-1][y+1]==1:
                                Support[x-1][y+1]=2
                                ObjectN=1
                            
                            if Support[x][y-1]==1:
                                Support[x][y-1]=2
                                ObjectN=1
                            
                            if Support[x][y+1]==1:
                                Support[x][y+1]=2
                                ObjectN=1
                            
                            if Support[x+1][y-1]==1:
                                Support[x+1][y-1]=2
                                ObjectN=1
                            
                            if Support[x+1][y]==1:
                                Support[x+1][y]=2
                                ObjectN=1
                            
                            if Support[x+1][y+1]==1:
                                Support[x+1][y+1]=2
                                ObjectN=1
                if ObjectN==0:
                    for i in range(R):
                        for j in range(C):
                            x=i+1
                            y=j+1                    
                            if Support[x][y]==2:
                                test=1
                                Support[x][y]=0
                                Output[x][y]=Hit
                                if test==0:
                                    test=1
                                    ObjectN=1
        for i in range(R):
            for j in range(C):
                if ObjectN==0:
                    x=i+1
                    y=j+1
                    if Support[x][y]!=0:
                        detection=1
                        ObjectN=1
                        Hit=Hit+1
    for i in range(R):
        for j in range(C):
            ObjectsArray[i][j]=Output[i+1][j+1]
    
    
    return ObjectsArray
        

        
def ParticleTypeString(Input):
    String=""
    if Input==0:
        String="  Unknown  "
    if Input==1:
        String="   Alpha   "
    if Input==2:
        String="    Beta   "
    if Input==3:
        String="   Gamma   "
    if Input==4:
        String="    Muon   "
    if Input==5:
        String="    HEP    "
    return String
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        