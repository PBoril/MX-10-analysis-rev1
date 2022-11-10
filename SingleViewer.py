# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 17:36:49 2022

@author: pbori
"""

import tkinter
from tkinter import *
from tkinter import filedialog as fd
import sys
from os import listdir
from os.path import isfile, join
import General
import Image
import numpy as np
import Analysis
import Configmanager
Cropping=False
LogScale=False
path=Configmanager.LoadConfigPath()
FilesList=General.FilesList(path)
root = tkinter.Tk()
root.geometry("1200x800") 
root.title("Name") 
root.option_add('*Font', 'Arial 10') 
PathStr=tkinter.StringVar()
PathStr.set(path)





ObjectNumber=tkinter.IntVar()
ObjectNumber.set(0)
IndexNumber=tkinter.IntVar()
IndexNumber.set(0)
ObjectArray=[]
TKFileID=tkinter.StringVar()
TObjectID=tkinter.StringVar()

XCut=tkinter.IntVar()
YCut=tkinter.IntVar()
XCut.set(-1)
YCut.set(-1)

XCMin=tkinter.IntVar()
YCMin=tkinter.IntVar()
XCMax=tkinter.IntVar()
YCMax=tkinter.IntVar()

XCMin.set(-1)
YCMin.set(-1)
YCMax.set(-1)
XCMax.set(-1)

ObjectCount=tkinter.StringVar()
TotalEnergy=tkinter.StringVar()
Saturation=tkinter.StringVar()
PixelCount=tkinter.StringVar()
AlphaCount=tkinter.StringVar()
BetaCount=tkinter.StringVar()
GammaCount=tkinter.StringVar()
MuonCount=tkinter.StringVar()
HEPCount=tkinter.StringVar()
TotalObjectCount=tkinter.StringVar()

ParticleEnergy=tkinter.StringVar()
ParticlePixelCount=tkinter.StringVar()
ParticleType=tkinter.StringVar()



def RefreshFolder():
    global FilesList
    global ObjectArray
    NewFolder=Configmanager.SelectFolder()
    Configmanager.ReplaceLineConfig(0,"Load Folder Path = "+NewFolder+"/")
    path=Configmanager.LoadConfigPath()
    PathStr=tkinter.StringVar()
    PathStr.set(path)
    FilesList=General.FilesList(path)
    tkinter.Label(Selector, text="Folder = "+PathStr.get()).grid(row=10,column=10)
    IndexNumber.set(0)
    ObjectNumber.set(0)
    ObjectArray=[]
    Update()

Selector=tkinter.LabelFrame(root, text="Main")
Selector.grid(row=5, column=10)
tkinter.Label(Selector, text="Folder = "+PathStr.get()).grid(row=10,column=10)
tkinter.Button(Selector, text="Select folder", command=RefreshFolder).grid(row=10, column=20)



def ExportDetectionList():
    global DetectionList
    Path=fd.asksaveasfilename()
    General.ExportObjectsList(DetectionList,Path)
    print("Saved into: "+ Path)
    


tkinter.Button(Selector, text="Export", command=ExportDetectionList).grid(row=20, column=15)


def Update():
    global LogScale
    global Cropping
    global FilesList
    global DetectionList
    tkinter.Label(control, text="File "+str(IndexNumber.get()+1)+"/"+str(len(FilesList))).grid(row=20, column=20)
    tkinter.Label(control, text="File Name: "+((FilesList[IndexNumber.get()]))[len(path):]).grid(row=30, column=20)
    if Cropping==False:
        tkinter.Button(ObjectSelect, text="Crop", command=Crop,relief=tkinter.RAISED, state=NORMAL, padx=5, pady=5).grid(row=20,column=20,sticky=W)
        tkinter.Button(ObjectSelect, text="Uncrop", command=Uncrop, relief=tkinter.SUNKEN, state=DISABLED, padx=5, pady=5).grid(row=20,column=20,sticky=E)
    if Cropping==True:
        tkinter.Button(ObjectSelect, text="Crop", command=Crop,relief=tkinter.SUNKEN, state=DISABLED, padx=5, pady=5).grid(row=20,column=20,sticky=W)
        tkinter.Button(ObjectSelect, text="Uncrop", command=Uncrop, relief=tkinter.RAISED, state=NORMAL, padx=5, pady=5).grid(row=20,column=20,sticky=E)
    tkinter.Label(ObjectSelect, text="Object: "+str(ObjectNumber.get())+"/"+str(ObjectCount.get())).grid(row=17, column=20)
    tkinter.Label(ObjectPar, text="Detected Size="+ParticlePixelCount.get()+" pixels").grid(row=10, column=20)
    tkinter.Label(ObjectPar, text="Energy ="+ParticleEnergy.get()+" KeV").grid(row=20, column=20)
    tkinter.Label(ObjectPar, text="Particle type: "+ParticleType.get()).grid(row=30, column=20)

def Select():
    IndexNumber.set(int(TKFileID.get())-1)
    Reload()

def Reload():
    if IndexNumber.get()<0:
        IndexNumber.set(0)
    Array=General.LoadFile(FilesList[IndexNumber.get()])
    Image.PlotArray(Array)
    Update()
def up():
    IndexNumber.set(IndexNumber.get()+1)
    Reload()
def down():
    IndexNumber.set(IndexNumber.get()-1)
    Reload()
    
def AnalyseFolder():
    AlphaCount.set(0)
    BetaCount.set(0)
    GammaCount.set(0)
    MuonCount.set(0)
    HEPCount.set(0)
    PUsed=0
    PTotal=0
    
    global DetectionList
    global ObjectArray
    global FilesList
    DetectionList=[]
    TotalEnergy.set(0)
    for k in range (len(FilesList)):
        Array=General.LoadFile(FilesList[k])
        ObjectArray=General.SeparateObjects(General.LoadFile(FilesList[k]))
        DetectionListFile=Analysis.ObjectRegister(Array,ObjectArray)
        DetectionListFile=Analysis.BasicSeparation(Array, ObjectArray, DetectionListFile)
        print("File "+str(k+1)+" out of "+str(len(FilesList))+" loaded.")
        DetectionList=DetectionList+DetectionListFile
        PUsedFile=np.count_nonzero(ObjectArray)
        PTotalFile=len(ObjectArray)*len(ObjectArray[0])
        TotalEnergyFile=(np.sum(Array))
        TotalEnergy.set(str(float(TotalEnergy.get())+float(TotalEnergyFile)))
        PUsed=PUsedFile+PUsed
        PTotal=PTotalFile+PTotal
        Image.PlotArray(Array)
    for k in range(len(DetectionList)):
        DetectionList[k][0]=k+1
    for i in range (len(DetectionList)):
        if DetectionList[i][4]==1:
            AlphaCount.set(str(int(AlphaCount.get())+1))
        if DetectionList[i][4]==2:
            BetaCount.set(str(int(BetaCount.get())+1))
        if DetectionList[i][4]==3:
            GammaCount.set(str(int(GammaCount.get())+1))
        if DetectionList[i][4]==4:
            MuonCount.set(str(int(MuonCount.get())+1))
        if DetectionList[i][4]==5:
            HEPCount.set(str(int(HEPCount.get())+1))
    TotalObjectCount.set(str(len(DetectionList)))
    
    ObjectCount.set(str(len(DetectionList)))
    tkinter.Label(FilePar, text=TotalEnergy.get()+" KeV").grid(row=20,column=20)
    PShow=((PUsed/PTotal)*100)
    PShow=str('{0:.3f}'.format(PShow))+" %"
    PixelCount.set(PUsed)
    Saturation.set(PShow)
    tkinter.Label(FilePar, text=ObjectCount.get()).grid(row=10,column=20)
    tkinter.Label(FilePar, text=Saturation.get()).grid(row=30,column=20)
    tkinter.Label(FilePar, text=PixelCount.get()).grid(row=40,column=20)
    tkinter.Label(FilePar, text=AlphaCount.get()).grid(row=50,column=20)
    tkinter.Label(FilePar, text=BetaCount.get()).grid(row=60,column=20)
    tkinter.Label(FilePar, text=GammaCount.get()).grid(row=70,column=20)
    tkinter.Label(FilePar, text=MuonCount.get()).grid(row=80,column=20)
    tkinter.Label(FilePar, text=HEPCount.get()).grid(row=90,column=20)
    tkinter.Label(FilePar, text=TotalObjectCount.get()).grid(row=45,column=20)
    
    

    
    
def AnalyseFile():
    global DetectionList
    global ObjectArray
    ObjectArray=General.SeparateObjects(General.LoadFile(FilesList[IndexNumber.get()]))
    ObjectCount.set(np.amax(ObjectArray))
    tkinter.Label(FilePar, text=ObjectCount.get()).grid(row=10,column=20)
    Array=General.LoadFile(FilesList[IndexNumber.get()])
    TotalEnergy.set(np.sum(Array))
    tkinter.Label(FilePar, text=TotalEnergy.get()+" KeV").grid(row=20,column=20)
    PUsed=np.count_nonzero(ObjectArray)
    PTotal=len(ObjectArray)*len(ObjectArray[0])
    PShow=((PUsed/PTotal)*100)
    PShow=str('{0:.3f}'.format(PShow))+" %"
    Saturation.set(PShow)
    tkinter.Label(FilePar, text=Saturation.get()).grid(row=30,column=20)
    PixelCount.set(PUsed)
    tkinter.Label(FilePar, text=PixelCount.get()).grid(row=40,column=20)
    DetectionList=Analysis.ObjectRegister(Array,ObjectArray)
    AlphaCount.set(0)
    BetaCount.set(0)
    GammaCount.set(0)
    MuonCount.set(0)
    HEPCount.set(0)
    TotalObjectCount.set(len(DetectionList))
    DetectionList=Analysis.BasicSeparation(Array, ObjectArray, DetectionList)
    for i in range (len(DetectionList)):
        if DetectionList[i][4]==1:
            AlphaCount.set(str(int(AlphaCount.get())+1))
        if DetectionList[i][4]==2:
            BetaCount.set(str(int(BetaCount.get())+1))
        if DetectionList[i][4]==3:
            GammaCount.set(str(int(GammaCount.get())+1))
        if DetectionList[i][4]==4:
            MuonCount.set(str(int(MuonCount.get())+1))
        if DetectionList[i][4]==5:
            HEPCount.set(str(int(HEPCount.get())+1))
    tkinter.Label(FilePar, text=AlphaCount.get()).grid(row=50,column=20)
    tkinter.Label(FilePar, text=BetaCount.get()).grid(row=60,column=20)
    tkinter.Label(FilePar, text=GammaCount.get()).grid(row=70,column=20)
    tkinter.Label(FilePar, text=MuonCount.get()).grid(row=80,column=20)
    tkinter.Label(FilePar, text=HEPCount.get()).grid(row=90,column=20)
    tkinter.Label(FilePar, text=TotalObjectCount.get()).grid(row=45,column=20)
        
File=tkinter.LabelFrame(root, text="File", padx=5, pady=5)
File.grid(row=10, column=10, sticky=N)
control=tkinter.LabelFrame(File, text="File Control", padx=5, pady=5)
control.grid(row=10, column=10)

tkinter.Label(control, text="File N.: "+str(IndexNumber.get()+1)).grid(row=20, column=20)
tkinter.Label(control, text="File Name: "+((FilesList[IndexNumber.get()+1]))[len(path):]).grid(row=30, column=20)
tkinter.Button(control, text=">", command=up, padx=5, pady=5).grid(row=10, column=30)
tkinter.Button(control, text="<", command=down, padx=5, pady=5).grid(row=10, column=10)
tkinter.Label(control, text="File Number:").grid(row=10, column=20, sticky=W)
FileID=tkinter.Entry(control, textvariable=TKFileID, width=10).grid(row=10, column=20, sticky=E)
tkinter.Button(control, text="Select", command=Select, padx=5, pady=5).grid(row=15, column=20)
tkinter.Button(control, text="Analyse file", command=AnalyseFile).grid(row=40, column=10, sticky=E)
tkinter.Button(control, text="Analyse folder", command=AnalyseFolder).grid(row=40, column=30, sticky=W)

FileAnalysis=tkinter.LabelFrame(File, text="File Data")
FileAnalysis.grid(row=20, column=10)
tkinter.Label(FileAnalysis, text="test").grid(row=10, column=10)


def SelectObject():
    ObjectNumber.set(int(TObjectID.get()))
    OKObject()


def OKObject():
    global Cropping
    global ObjectArray
    global DetectionList
    if ObjectNumber.get()<0:
        ObjectNumber.set(0)
    if IndexNumber.get()<0:
        IndexNumber.set(0)
    Array=General.LoadFile(FilesList[IndexNumber.get()])
    Image.ShowSingleObject(Array, ObjectArray, ObjectNumber.get(), Cropping)
    if len(DetectionList)<0:
        DetectionList=Analysis.ObjectRegister(Array,ObjectArray)
    ParticlePixelCount.set(DetectionList[ObjectNumber.get()-1][1])
    ParticleEnergy.set(str(round(DetectionList[ObjectNumber.get()-1][2],2)))
    ParticleType.set(General.ParticleTypeString(DetectionList[ObjectNumber.get()-1][4]))
    Update()

def NextObject():
    ObjectNumber.set(ObjectNumber.get()+1)
    OKObject()
def PreviousObject():
    ObjectNumber.set(ObjectNumber.get()-1)
    OKObject()

def Crop():
    global Cropping
    Cropping=True
    OKObject()
    Update()
def Uncrop():
    global Cropping
    Cropping=False
    OKObject()
    Update()



Object=tkinter.LabelFrame(root, text="Object",padx=5,pady=5)
Object.grid(row=10, column=20, sticky=N)
ObjectSelect=tkinter.LabelFrame(Object, text="Object Control",padx=5, pady=5)
ObjectSelect.grid(row=10,column=10)
ObjectSelect.columnconfigure(20,minsize=175)
tkinter.Button(ObjectSelect, text=">", command=NextObject, padx=5, pady=5).grid(row=10, column=30)
tkinter.Button(ObjectSelect, text="<", command=PreviousObject, padx=5, pady=5).grid(row=10, column=10)
tkinter.Label(ObjectSelect, text="Object Number:").grid(row=10, column=20, sticky=W)
FileID=tkinter.Entry(ObjectSelect, textvariable=TObjectID, width=10).grid(row=10, column=20, sticky=E)
tkinter.Button(ObjectSelect, text="Select", command=SelectObject, padx=5, pady=5).grid(row=15, column=20)
tkinter.Label(ObjectSelect, text="Object: "+str(ObjectNumber.get())+"/"+str(ObjectCount.get())).grid(row=17, column=20)
tkinter.Button(ObjectSelect, text="Crop", command=Crop,relief=tkinter.RAISED, state=NORMAL, padx=5, pady=5).grid(row=20,column=20, sticky=W)
tkinter.Button(ObjectSelect, text="Uncrop", command=Uncrop, relief=tkinter.SUNKEN, state=DISABLED, padx=5, pady=5).grid(row=20,column=20, sticky=E)

ObjectPar=tkinter.LabelFrame(Object, text="Object Parametres", padx=5, pady=5)
ObjectPar.grid(row=20, column=10)
tkinter.Label(ObjectPar, text="Detected Size="+ParticlePixelCount.get()+" pixels").grid(row=10, column=20)
tkinter.Label(ObjectPar, text="Energy ="+ParticleEnergy.get()+" KeV").grid(row=20, column=20)
tkinter.Label(ObjectPar, text="Particle type: "+ParticleType.get()).grid(row=30, column=20)



FilePar=tkinter.LabelFrame(File, text="File parametres")
FilePar.grid(row=20,column=10)
tkinter.Label(FilePar, text="Object count:").grid(row=10,column=10)
tkinter.Label(FilePar, text="Total Energy: ").grid(row=20,column=10)
tkinter.Label(FilePar, text="Saturation: ").grid(row=30,column=10)
tkinter.Label(FilePar, text="Total Objects:").grid(row=45,column=10)
tkinter.Label(FilePar, text="Pixel count: ").grid(row=40,column=10)
tkinter.Label(FilePar, text="Alpha count: ").grid(row=50,column=10)
tkinter.Label(FilePar, text="Beta Count: ").grid(row=60,column=10)
tkinter.Label(FilePar, text="Gamma Count: ").grid(row=70,column=10)
tkinter.Label(FilePar, text="Muon Count: ").grid(row=80,column=10)
tkinter.Label(FilePar, text="HEP Count: ").grid(row=90,column=10)





def ShowAlpha():
    global ObjectArray
    global DetectionList
    Array=General.LoadFile(FilesList[IndexNumber.get()])
    TypeArray=np.zeros((len(Array),len(Array[0])))

    for k in range(len(DetectionList)):
        if DetectionList[k][4]==1:
            for i in range (len(Array)):
                for j in range(len(Array[0])):
                    if ObjectArray[i][j]==k+1:
                        TypeArray[i][j]=Array[i][j]
    Image.PlotArray(TypeArray)
    
def ShowBeta():
    global ObjectArray
    global DetectionList
    Array=General.LoadFile(FilesList[IndexNumber.get()])
    TypeArray=np.zeros((len(Array),len(Array[0])))

    for k in range(len(DetectionList)):
        if DetectionList[k][4]==2:
            for i in range (len(Array)):
                for j in range(len(Array[0])):
                    if ObjectArray[i][j]==k+1:
                        TypeArray[i][j]=Array[i][j]
    Image.PlotArray(TypeArray)
def ShowGamma():
    global ObjectArray
    global DetectionList
    Array=General.LoadFile(FilesList[IndexNumber.get()])
    TypeArray=np.zeros((len(Array),len(Array[0])))

    for k in range(len(DetectionList)):
        if DetectionList[k][4]==3:
            for i in range (len(Array)):
                for j in range(len(Array[0])):
                    if ObjectArray[i][j]==k+1:
                        TypeArray[i][j]=Array[i][j]
    Image.PlotArray(TypeArray)
def ShowMuon():
    global ObjectArray
    global DetectionList
    Array=General.LoadFile(FilesList[IndexNumber.get()])
    TypeArray=np.zeros((len(Array),len(Array[0])))

    for k in range(len(DetectionList)):
        if DetectionList[k][4]==4:
            for i in range (len(Array)):
                for j in range(len(Array[0])):
                    if ObjectArray[i][j]==k+1:
                        TypeArray[i][j]=Array[i][j]
    Image.PlotArray(TypeArray)
def ShowHEP():
    global ObjectArray
    global DetectionList
    Array=General.LoadFile(FilesList[IndexNumber.get()])
    TypeArray=np.zeros((len(Array),len(Array[0])))

    for k in range(len(DetectionList)):
        if DetectionList[k][4]==5:
            for i in range (len(Array)):
                for j in range(len(Array[0])):
                    if ObjectArray[i][j]==k+1:
                        TypeArray[i][j]=Array[i][j]
    Image.PlotArray(TypeArray)



ObjectTypeLabelFrame=tkinter.LabelFrame(root, text="Show particle types")
ObjectTypeLabelFrame.grid(row=10, column=30, sticky=N)
tkinter.Button(ObjectTypeLabelFrame, text="Show Alpha", command=ShowAlpha).grid(row=10, column=10)
tkinter.Button(ObjectTypeLabelFrame, text="Show Beta", command=ShowBeta).grid(row=20, column=10)
tkinter.Button(ObjectTypeLabelFrame, text="Show Gamma", command=ShowGamma).grid(row=30, column=10)
tkinter.Button(ObjectTypeLabelFrame, text="Show Muon", command=ShowMuon).grid(row=40, column=10)
tkinter.Button(ObjectTypeLabelFrame, text="Show HEP", command=ShowHEP).grid(row=50, column=10)

def LogS():
    global LogScale
    LogScale=True
    RefreshHist()
def StanS():
    global LogScale
    LogScale=False
    RefreshHist()
def RefreshHist():
    global LogScale
    if LogScale==False:
        tkinter.Button(Histogrames, text="Log", command=LogS,relief=tkinter.RAISED, state=NORMAL, padx=5, pady=5).grid(row=5,column=15,sticky=E)
        tkinter.Button(Histogrames, text="Standart", command=StanS, relief=tkinter.SUNKEN, state=DISABLED, padx=5, pady=5).grid(row=5,column=20,sticky=W)
    if LogScale==True:
        tkinter.Button(Histogrames, text="Log", command=LogS,relief=tkinter.SUNKEN, state=DISABLED, padx=5, pady=5).grid(row=5,column=15,sticky=E)
        tkinter.Button(Histogrames, text="Standart", command=StanS, relief=tkinter.RAISED, state=NORMAL, padx=5, pady=5).grid(row=5,column=20,sticky=W)

def HistogrameFunction(PType, HType):
    global LogScale
    global DetectionList
    HistList=[]
    
    for k in range (len(DetectionList)):
        if DetectionList[k][4]==PType:
            HistList.append(DetectionList[k][HType])
        if PType==6:
            HistList.append(DetectionList[k][HType])
    if HType==1:
        Image.HistogramePixel(HistList, 10, LogScale)
    if HType==2:
        Image.HistogrameEnergy(HistList, 10, LogScale)
def AlphaPixel():
    HistogrameFunction(1,1)
def AlphaEnergy():
    HistogrameFunction(1,2)
def BetaPixel():
    HistogrameFunction(2,1)
def BetaEnergy():
    HistogrameFunction(2,2)
def GammaPixel():
    HistogrameFunction(3,1)
def GammaEnergy():
    HistogrameFunction(3,2)
def MuonPixel():
    HistogrameFunction(4,1)
def MuonEnergy():
    HistogrameFunction(4,2)
def HEPPixel():
    HistogrameFunction(5,1)
def HEPEnergy():
    HistogrameFunction(5,2)
def FilePixel():
    HistogrameFunction(6,1)
def FileEnergy():
    HistogrameFunction(6,2)
def TypeDist():
    global DetectionList
    TypeCount=np.zeros(6)
    for k in range (len(DetectionList)):
        TypeCount[DetectionList[k][4]]=TypeCount[DetectionList[k][4]]+1
    
    Image.ShowTypeCount(TypeCount)





Histogrames=tkinter.LabelFrame(root, text="Create Histograme")
Histogrames.grid(row=10, column=40, sticky=N)

tkinter.Label(Histogrames, text="Alpha ").grid(row=10,column=5)
tkinter.Label(Histogrames, text="Beta ").grid(row=20,column=5)
tkinter.Label(Histogrames, text="Gamma ").grid(row=30,column=5)
tkinter.Label(Histogrames, text="Muon ").grid(row=40,column=5)
tkinter.Label(Histogrames, text="HEP ").grid(row=50,column=5)
tkinter.Label(Histogrames, text="File ").grid(row=60,column=5)

tkinter.Button(Histogrames, text="Pixel", command=AlphaPixel).grid(row=10,column=10)
tkinter.Button(Histogrames, text="Energy", command=AlphaEnergy).grid(row=10, column=15)
tkinter.Button(Histogrames, text="Pixel", command=BetaPixel).grid(row=20,column=10)
tkinter.Button(Histogrames, text="Energy", command=BetaEnergy).grid(row=20, column=15)
tkinter.Button(Histogrames, text="Pixel", command=GammaPixel).grid(row=30,column=10)
tkinter.Button(Histogrames, text="Energy", command=GammaEnergy).grid(row=30, column=15)
tkinter.Button(Histogrames, text="Pixel", command=MuonPixel).grid(row=40,column=10)
tkinter.Button(Histogrames, text="Energy", command=MuonEnergy).grid(row=40, column=15)
tkinter.Button(Histogrames, text="Pixel", command=HEPPixel).grid(row=50,column=10)
tkinter.Button(Histogrames, text="Energy", command=HEPEnergy).grid(row=50, column=15)

tkinter.Button(Histogrames, text="Pixel", command=FilePixel).grid(row=60,column=10)
tkinter.Button(Histogrames, text="Energy", command=FileEnergy).grid(row=60, column=15)
    
tkinter.Button(Histogrames, text="Particle type distribution", command=TypeDist).grid(row=70, column=15)    

tkinter.Button(Histogrames, text="Log", command=LogS,relief=tkinter.RAISED, state=NORMAL, padx=5, pady=5).grid(row=5,column=15,sticky=E)
tkinter.Button(Histogrames, text="Standart", command=StanS, relief=tkinter.SUNKEN, state=DISABLED, padx=5, pady=5).grid(row=5,column=20,sticky=W)

def CutRefresh():
    tkinter.Label(HCutting, text=YCut.get()).grid(row=10, column=20)
    tkinter.Label(VCutting, text=XCut.get()).grid(row=10, column=20)

def HCutD10():
    YCut.set(YCut.get()-10)
    CutRefresh()
def HCutD():
    YCut.set(YCut.get()-1)
    CutRefresh()
def HCutU():
    YCut.set(YCut.get()+1)
    CutRefresh()
def HCutU10():
    YCut.set(YCut.get()+10)
    CutRefresh()
def VCutD10():
    XCut.set(XCut.get()-10)
    CutRefresh()
def VCutD():
    XCut.set(XCut.get()-1)
    CutRefresh()
def VCutU():
    XCut.set(XCut.get()+1)
    CutRefresh()
def VCutU10():
    XCut.set(XCut.get()+10)
    CutRefresh()
def ShowHLine():
    Array=General.LoadFile(FilesList[IndexNumber.get()])
    Image.PlotArray(Array, 0, YCut.get(),-1)
def ShowVLine():
    Array=General.LoadFile(FilesList[IndexNumber.get()])
    Image.PlotArray(Array, 0,-1, XCut.get())
def ShowBLine():
    Array=General.LoadFile(FilesList[IndexNumber.get()])
    Image.PlotArray(Array, 0, YCut.get(), XCut.get())
    
    
def MakeHCut():
    Array=General.LoadFile(FilesList[IndexNumber.get()])
    Image.ShowHCut(Array, YCut.get(), XCMin.get(), XCMax.get())    
def MakeVCut():
    Array=General.LoadFile(FilesList[IndexNumber.get()])
    Image.ShowVCut(Array, XCut.get(),YCMin.get(), YCMax.get())     
    
Cutting=tkinter.LabelFrame(root, text="Cut", padx=5, pady=5)

Cutting.grid(row=20, column=10, sticky=N)
HCutting=tkinter.LabelFrame(Cutting, text="Horizontal", padx=5, pady=5)
HCutting.grid(row=10, column=10)
tkinter.Label(HCutting, text=YCut.get()).grid(row=10, column=20)
tkinter.Button(HCutting, text="↓↓", command=HCutD10).grid(row=10, column=10)
tkinter.Button(HCutting, text="↓", command=HCutD).grid(row=10, column=15)
tkinter.Button(HCutting, text="↑", command=HCutU).grid(row=10, column=25)
tkinter.Button(HCutting, text="↑↑", command=HCutU10).grid(row=10, column=30)

VCutting=tkinter.LabelFrame(Cutting, text="Vertical", padx=5, pady=5)
VCutting.grid(row=10, column=20)
tkinter.Label(VCutting, text=XCut.get()).grid(row=10, column=20)
tkinter.Button(VCutting, text="<<", command=VCutD10).grid(row=10, column=10)
tkinter.Button(VCutting, text="<", command=VCutD).grid(row=10, column=15)
tkinter.Button(VCutting, text=">", command=VCutU).grid(row=10, column=25)
tkinter.Button(VCutting, text=">>", command=VCutU10).grid(row=10, column=30)


tkinter.Button(Cutting, text="Show Horizontal cut line", command=ShowHLine).grid(row=20, column=10)
tkinter.Button(Cutting, text="Show both", command=ShowBLine).grid(row=20, column=15)
tkinter.Button(Cutting, text="Show Vertical cut line", command=ShowVLine).grid(row=20, column=20)

CuttingRanges=tkinter.LabelFrame(Cutting, text="Cutting ranges")
CuttingRanges.grid(row=30, column=15)

tkinter.Label(CuttingRanges, text="X min").grid(row=10, column=10)
tkinter.Label(CuttingRanges, text="X max").grid(row=10, column=20)
tkinter.Label(CuttingRanges, text="Y min").grid(row=10, column=30)
tkinter.Label(CuttingRanges, text="Y max").grid(row=10, column=40)

tkinter.Entry(CuttingRanges, textvariable=XCMin,width=5).grid(row=20, column=10)
tkinter.Entry(CuttingRanges, textvariable=XCMax,width=5).grid(row=20, column=20)
tkinter.Entry(CuttingRanges, textvariable=YCMin,width=5).grid(row=20, column=30)
tkinter.Entry(CuttingRanges, textvariable=YCMax,width=5).grid(row=20, column=40)






tkinter.Button(Cutting, text="Make Horizontal cut", command=MakeHCut).grid(row=50, column=10)
tkinter.Button(Cutting, text="Make Vertical cut", command=MakeVCut).grid(row=50, column=20)





































root.mainloop()