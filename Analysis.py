# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 19:05:26 2022

@author: pbori
"""
import numpy as np
def ObjectRegister(InputArray, ObjectsArray):
    DetectionList=[]
    R=len(InputArray)
    C=len(InputArray[0])
    SupportDet=[0,0,0,0,0,0]   #ObjectID, PixCount, Energy, Diameter, ParticleType, Border
    for k in range (np.amax(ObjectsArray)):
        DetectionList.append(list(SupportDet))
        DetectionList[k][0]=k+1
    for k in range (len(DetectionList)):
        for i in range(R):
            for j in range(C):
                if ObjectsArray[i][j]==k+1:
                    DetectionList[k][1]=DetectionList[k][1]+1
                    DetectionList[k][2]=DetectionList[k][2]+InputArray[i][j]
    return DetectionList

def CreateObjectArray(InputArray, ObjectsArray, ObjectNumber):
    R=len(InputArray)
    C=len(InputArray[0])
    SingleObjectArray=[ [0] * R for _ in range(C)]
    for i in range(R):
        for j in range(C):
            if ObjectsArray[i][j]==ObjectNumber:
                SingleObjectArray[i][j]=InputArray[i][j]
    return SingleObjectArray
    


def BasicSeparation(InputArray, ObjectsArray, ObjectsList):
    for i in range (len(ObjectsList)):
        
        if ObjectsList[i][2]>500:
            if ObjectsList[i][1]<100:
                ObjectsList[i][4]=1
            if ObjectsList[i][1]>=100:
                ObjectsList[i][4]=5
        if ObjectsList[i][2]<=500:
            if ObjectsList[i][1]<30:
                ObjectsList[i][4]=2
            if ObjectsList[i][1]>=30:
                ObjectsList[i][4]=4
        if ObjectsList[i][1]<4:
            ObjectsList[i][4]=3
            
            
            
    return ObjectsList
