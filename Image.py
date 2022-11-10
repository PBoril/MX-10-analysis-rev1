# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 20:37:37 2022

@author: pbori
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import Analysis



#"Create heatmap from array&max value input"
def PlotArray(DataArray, MaxValue=0, Yc=-1,  Xc=-1,):
    VMAX=np.amax(DataArray)
    if MaxValue>0:
        VMAX=MaxValue
    if Xc>-1:
        plt.axvline(x=Xc, color='r', linestyle='dotted')
    if Yc>-1:
        plt.axhline(y=Yc, color='g', linestyle='dotted')
    plt.pcolormesh(DataArray, rasterized=True, vmin=0, vmax=VMAX)
    plt.colorbar()
    plt.axis()
    plt.ylabel("Energy [KeV]", labelpad=-375)
    plt.show()
    return

def RotateArray(DataArray): #"Rotation is clockwise, flip is horisontal, R=Rotate, F=Flip"
    RotatedArrayList=[]
    for i in range(4):
        I=i+1
        RotatedArrayList.append(np.rot90(DataArray,I, axes=(0,1)))
        RotatedArrayList.append(np.fliplr(np.rot90(DataArray,I, axes=(0,1))))
    return RotatedArrayList #"1R0F,1R1F,2R0F,2R1F,3R0F,3R1F,4R0F,4R1F"

def ShowSingleObject(DataArray, ObjectsArray, ObjectNumber, Crop=False):
    DisplayArray=Analysis.CreateObjectArray(DataArray, ObjectsArray, ObjectNumber)
    if Crop==False:
        PlotArray(DisplayArray)
    if (Crop==True):
        plt.pcolormesh(DisplayArray, rasterized=True, vmin=0, vmax=np.amax(DisplayArray))
        CropRanges=GetCropRanges(DisplayArray)
        plt.xlim(CropRanges[2]-1,CropRanges[3]+2)
        plt.ylim(CropRanges[0]-1, CropRanges[1]+2)
        plt.colorbar()
        plt.ylabel("Energy [KeV]", labelpad=-375)
        plt.show()
def GetCropRanges(SingleObjectArray):
    R=len(SingleObjectArray)
    C=len(SingleObjectArray[0])
    Rmin=R+1
    Cmin=C+1
    Rmax=0
    Cmax=0
    Output=[]
    for i in range (R):
        for j in range (C):
            if SingleObjectArray[i][j]!=0:
                if i<Rmin:
                    Rmin=i
                if j<Cmin:
                    Cmin=j
                if i>Rmax:
                    Rmax=i
                if j>Cmax:
                    Cmax=j
    return(Rmin, Rmax, Cmin, Cmax)


def HistogramePixel(Data, Bins, Scale):
    D_pixely=np.ravel(np.array(Data))
    D_pixely = [i for i in D_pixely if i != 0]
    maxim_pixel=np.amax(Data)
    plt.hist(D_pixely,density=True, bins=Bins)
    plt.xlabel("Energy [KeV]")
    if (Scale==True):
        plt.xscale("log")
    plt.ylabel("Quantity")
    plt.grid(b=True, which="both", axis="both")
    plt.show()

def HistogrameEnergy(Data, Bins, Scale):
    D_pixely=np.ravel(np.array(Data))
    D_pixely = [i for i in D_pixely if i != 0]
    maxim_pixel=np.amax(Data)
    plt.hist(D_pixely,density=True, bins=Bins)
    plt.xlabel("Energy [KeV]")
    if (Scale==True):
        plt.xscale("log")
    plt.ylabel("Quantity")
    plt.grid(b=True, which="both", axis="both")
    plt.show()
    
def ShowTypeCount(Count):
    ArrayCounts={"Unknown":Count[0], "Alpha":Count[1],"Beta":Count[2],"Gamma":Count[3],"Muion":Count[4],"HEP":Count[5]}
    Keys0=list(ArrayCounts.keys())
    Values0=list(ArrayCounts.values())
    plt.bar(Keys0,Values0)
    print(ArrayCounts)
    plt.ylabel("Count [N]")
    plt.grid(b=True, which="both", axis="y")
    plt.show()
   
       

    
def ShowVCut(DataArray, XCord, YAxMin, YAxMax):
    GraphData=[]
    Y=[]
    for k in range(len(DataArray)):
        GraphData.append(DataArray[k][XCord])
        Y.append(k)
    plt.plot(GraphData, Y)
    plt.xlabel("Energy [KeV]")
    plt.ylabel("Y")
    if YAxMin>-1 or YAxMax>-1:
        plt.ylim(YAxMin, YAxMax)
    plt.show()
    
def ShowHCut(DataArray, YCord, XAxMin, XAxMax):
    GraphData=[]
    X=[]
    for k in range(len(DataArray[YCord])):
        GraphData.append(DataArray[YCord][k])
        X.append(k)
    plt.plot(X, GraphData)
    plt.xlabel("X")
    plt.ylabel("Energy [KeV]")
    if XAxMin>-1 or XAxMax>-1:
        plt.xlim(XAxMin, XAxMax)
    plt.show()
        
    