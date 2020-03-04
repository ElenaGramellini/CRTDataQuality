from ROOT import *
import argparse
from sortedcontainers import SortedList
from datetime import datetime
from sets import Set
import pprint
import copy
from array import array
import os, sys



# Make 73 histograms with date as x and y = mean, err y = sqrt(mean)
# display readout time in each plot




'''

    # Create Summary TTree
    t = TTree( 'summaryTree', 'ttree which sums up the crt data quality' )
    febName  = array( 'i', [ 0 ] )
    entries  = array( 'i', [ 0 ] )
    nHitMean = array( 'd', [ 0 ] )
    nHitRMS  = array( 'd', [ 0 ] )
    chi2     = array( 'd', [ 0 ] )
    dof      = array( 'd', [ 0 ] )
    prob     = array( 'd', [ 0 ] )
    readoutT = array( 'd', [ 0 ] )
'''



def __main__():
    dirs = os.listdir("rootFilesUncorrectedRates")
    inputFileList = []
    for d in dirs:
        if "CRT_DQ" in d:
            if ".root" in d:
                inputFileList.append("rootFilesUncorrectedRates/"+d)
                print d

    inputFileList.sort()
    # Get the Feb index... this is awful, but ok
    firstFileName = inputFileList[0]
    febIndex = quickReadFile(firstFileName)[0]

    # Determine Number of bins in the histograms
    nBins = len(inputFileList)    
    histoList = []
    

    # Create histograms and fitting functions
    for i in xrange(73):
        histoTemp    = TH1D("nHitsCRT_FEB_" +str(febIndex[i]),"nHitsCRT_FEB"+str(febIndex[i])+"; Date ; Raw Hit Rate  ",nBins,-0.5,nBins-0.5)
        histoTemp2   = TH1D("nHitsCRT_FEB2_"+str(febIndex[i]),"nHitsCRT_FEB2_"+str(febIndex[i])+"; Date ; Raw Hit Rate  ",nBins,-0.5,nBins-0.5)
        hHitsOverEvt = TH1D("hHitsOverEvt_FEB_"+str(febIndex[i]),"hHitsOverEvt_FEB"+str(febIndex[i])+"; Date ; Raw Hit Rate  ",nBins,-0.5,nBins-0.5)


        for iFile in xrange(len(inputFileList)):
            f = inputFileList[iFile]
            thisDateName = ((f[:-5]).split("_"))[2]
            result = quickReadFile(f)
            meanList      = result[1]
            rmsList       = result[2]
            readoutTList  = result[3]
            totNumberList = result[4]
            entriesList   = result[5]

            histoTemp.SetBinContent(iFile+1 , meanList[i])
            histoTemp.SetBinError  (iFile+1 ,  rmsList[i])
            histoTemp.GetXaxis().SetBinLabel(iFile+1,thisDateName)
            histoTemp.SetLineColor(kRed)

            histoTemp2.SetBinContent(iFile+1 , meanList[i])
            histoTemp2.SetBinError  (iFile+1 , TMath.Sqrt(meanList[i]))
            histoTemp2.GetXaxis().SetBinLabel(iFile+1,thisDateName)
            histoTemp2.SetLineColor(kGreen)

            # Michelle's Smarter plots
            if entriesList[i]>0 and totNumberList[i] > 0:
                hHitsOverEvtBin = float(totNumberList[i])/float(entriesList[i])
                hHitsOverEvtErr = hHitsOverEvtBin * TMath.Sqrt( 1./float(totNumberList[i]) + 1./float(entriesList[i])  )
                hHitsOverEvt.SetBinContent(iFile+1 ,hHitsOverEvtBin)
                hHitsOverEvt.SetBinError(iFile+1   ,hHitsOverEvtErr)
                hHitsOverEvt.GetXaxis().SetBinLabel(iFile+1,thisDateName)

        histoList.append(histoTemp)    
        histoList.append(histoTemp2)    
        histoList.append(hHitsOverEvt)    


    # Out File
    outFile = TFile("perDatePlots/CRTDataQuality_RatePerDateUncorrectedRate.root","recreate")
    for h in histoList:
        outFile.Add(h)
    outFile.Write()
    outFile.Close()

    



def quickReadFile( thisFileName ):
    inFile =  TFile.Open(thisFileName)
    myTree =  inFile.Get("summaryTree")
    febIDList     = []
    meanList      = []
    rmsList       = []
    readoutTList  = []
    totNumberList = []
    entriesList   = []
    for e in myTree:
        febIDList    .append(e.febName)
        meanList     .append(e.nHitMean)
        rmsList      .append(e.nHitRMS )
        readoutTList .append(e.readoutT)
        totNumberList.append(e.totNumbHits)
        entriesList  .append(e.entries)


    return febIDList, meanList, rmsList, readoutTList, totNumberList, entriesList


__main__()




