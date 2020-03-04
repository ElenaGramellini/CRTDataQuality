from ROOT import *
import argparse
from sortedcontainers import SortedList
from datetime import datetime
from sets import Set
import pprint
import copy
from array import array
import os, sys



def __main__():
    dirs = os.listdir("rootFilesTrackMatch")
    inputFileList = []
    for d in dirs:
        if "Track_CRT_DQ" in d:
            if ".root" in d:
                inputFileList.append("rootFilesTrackMatch/"+d)
                print d

    inputFileList.sort()
    # Determine Number of bins in the histograms
    nBins = len(inputFileList)    
    histoList = []
    

    hNTracksAvg = TH1D("hNTracksAvg", "nTracksAvg ; Date ; Average N flashes per event",nBins,-0.5,nBins-0.5)
    hNTracksStd = TH1D("hNTracksStd", "nTracksStd ; Date ; Standard Dev N flashes per event",nBins,-0.5,nBins-0.5)
    hNMatchesAvg = TH1D("hNMatchesAvg", "nMatchesAvg ; Date ; Average N matches per event",nBins,-0.5,nBins-0.5)
    hNMatchesStd = TH1D("hNMatchesStd", "nMatchesStd ; Date ; Standard Dev N matches per event",nBins,-0.5,nBins-0.5)
    hEffAvg      = TH1D("hEffAvg"     , "average eff ; Date ; Avg Eff  ",nBins,-0.5,nBins-0.5)
    hEffStd      = TH1D("hEffStd"     , "Standard Dev Eff ; Date ; Standard Dev Eff  ",nBins,-0.5,nBins-0.5)


    for iFile in xrange(len(inputFileList)):
        print iFile
        f = inputFileList[iFile]
        thisDateName = ((f[:-5]).split("_"))[3]
        result = quickReadFile(f)
        
        hNTracksAvg.SetBinContent(iFile+1,result[0]) 
        hNTracksAvg.SetBinError(iFile+1,result[1]) 
        hNTracksStd.SetBinContent(iFile+1,result[1])
        hNMatchesAvg.SetBinContent(iFile+1,result[2])
        hNMatchesAvg.SetBinError(iFile+1,result[3])
        hNMatchesStd.SetBinContent(iFile+1,result[3])
        hEffAvg     .SetBinContent(iFile+1,result[4])
        hEffAvg     .SetBinError(iFile+1,result[5])
        hEffStd     .SetBinContent(iFile+1,result[5])

        hNTracksAvg.GetXaxis().SetBinLabel(iFile+1,thisDateName)
        hNMatchesAvg.GetXaxis().SetBinLabel(iFile+1,thisDateName)
        hEffAvg.GetXaxis().SetBinLabel(iFile+1,thisDateName)


    # Out File
    outFile = TFile("perDatePlots/TrackCRTDataQuality_RatePerDate.root","recreate")
    outFile.Add(hNTracksAvg)
    outFile.Add(hNTracksStd)
    outFile.Add(hNMatchesAvg)
    outFile.Add(hNMatchesStd)
    outFile.Add(hEffAvg     )
    outFile.Add(hEffStd     )
    outFile.Write()
    outFile.Close()

    



def quickReadFile( thisFileName ):
    inFile  =  TFile.Open(thisFileName)
    hTrack  =  inFile.Get("nTracks")
    hTrackM =  inFile.Get("nTracksMatched")
    hnFMEff =  inFile.Get("nFMEff")
    return hTrack.GetMean(), hTrack.GetStdDev(), hTrackM.GetMean(), hTrackM.GetStdDev(), hnFMEff.GetMean(), hnFMEff.GetStdDev()


__main__()




