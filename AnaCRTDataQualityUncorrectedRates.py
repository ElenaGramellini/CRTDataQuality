#!/usr/bin/env python


# Python macro from Elena Gramellini on April 3rd 2019
# Analyze the output of CRT data quality monitor, 
# Outputs summary of CRT hit frequency in each panel for each date

from ROOT import *
import argparse
from sortedcontainers import SortedList
from datetime import datetime
from sets import Set
import pprint
import copy
from array import array

# Sort of profiling what I'm doing
import time
start_time = time.time()

# I need to re-define an event cause the ROOT memory management is horrific
# So, when looping on the TTree, I'll construct my own event class
class event:
    def __init__(self, date, nCRThits):
        self.date         = date
        self.nCRThits     = nCRThits




# Let's see how distant the histograms are from the poisson distribution with the same mean
def CalculateChi2 ( histo , f1 ):
    lambda_pois = histo.GetMean()
    totNumbHits = 0
    for i in xrange(1,histo.GetSize()-2):
        totNumbHits += histo.GetBinContent(i) * (i -1)
    histo.Scale(1./histo.Integral())
    f1.SetParameter(0,lambda_pois)
    fitResult = histo.Fit(f1,"SQ")
    return lambda_pois, f1.GetChisquare(), f1.GetNDF(), f1.GetProb(), histo.GetEntries(), f1.GetParError(0), totNumbHits


# function that analyzes events in one date
def analyze(date, eventList, febIndex, originalReadoutTime):
    outFile = TFile("rootFilesUncorrectedRates/CRT_DQ_"+str(date)+".root","recreate")
    # Declare the final histograms
    histoList = []
    fitFunct  = []

    # Create histograms and fitting functions
    for i in xrange(len(febIndex)):
        histoTemp = TH1D("nHitsCRT_FEB"+str(febIndex[i]),"nHitsCRT_FEB"+str(febIndex[i])+"; N Hits in readout time; Area Norm Count ",30,-0.5,29.5)
        histoList.append(histoTemp)
        f1 = TF1("poisson"+str(febIndex[i]),"TMath::Poisson(x,[0])",0,30)
        fitFunct.append(f1)

    readoutTime = originalReadoutTime
    # Fill the Histograms
    for e in eventList:
        for i in xrange(len(histoList)):
            histoList[i].Fill(e.nCRThits[i])

    # Create Summary TTree
    t = TTree( 'summaryTree', 'ttree which sums up the crt data quality' )
    febName     = array( 'i', [ 0 ] )
    entries     = array( 'i', [ 0 ] )
    nHitMean    = array( 'd', [ 0 ] )
    nHitRMS     = array( 'd', [ 0 ] )
    chi2        = array( 'd', [ 0 ] )
    dof         = array( 'd', [ 0 ] )
    prob        = array( 'd', [ 0 ] )
    readoutT    = array( 'd', [ 0 ] )
    totNumbHits = array( 'i', [ 0 ] )

    t.Branch( 'febName'    , febName    , 'febName/I' )
    t.Branch( 'entries'    , entries    , 'entries/I' )
    t.Branch( 'nHitMean'   , nHitMean   , 'nHitMean/D')
    t.Branch( 'nHitRMS'    , nHitRMS    , 'nHitRMS/D' )
    t.Branch( 'chi2'       , chi2       , 'chi2/D'    )
    t.Branch( 'dof'        , dof        , 'dof/D'     )
    t.Branch( 'prob'       , prob       , 'prob/D'    )
    t.Branch( 'readoutT'   , readoutT   , 'readoutT/D')
    t.Branch( 'totNumbHits', totNumbHits, 'totNumbHits/I')

    # for each module, calculate the paramters with the CalculateChi2 function
    for i in xrange(len(histoList)):
        # All the calculation happens here
        result = CalculateChi2(histoList[i],fitFunct[i])
        # Fill the ttree
        febName    [ 0 ] = int( febIndex[i] )
        entries    [ 0 ] = int( result[4] )
        nHitMean   [ 0 ] = result[0] 
        nHitRMS    [ 0 ] = result[5]
        chi2       [ 0 ] = result[1]
        dof        [ 0 ] = result[2]
        prob       [ 0 ] = result[3]
        readoutT   [ 0 ] = readoutTime
        totNumbHits[ 0 ] = int( result[6] ) 
        t.Fill()

    # Save Output Files
    outFile.Write()
    outFile.Close()



# In the main, we read the input file and divide events by dates
def __main__():
    
    # Get input file
    parser = argparse.ArgumentParser()
    parser.add_argument("input"     , nargs='?', default = "", type = str, help="insert input filename")
    args     = parser.parse_args()
    filename      = args.input

    inFile =  TFile.Open(filename);
    myTree =  inFile.Get("CRTDataQuality/CRTDataQuality")
    


    # Get info which will be the same for all entries from the first entry
    # It's kind of barbaric, but I can't think of another way
    febIndex            = []
    originalReadoutTime = 0
    for firstEvt in myTree:
        febIndex = [febID for febID in firstEvt.febIndex]
        originalReadoutTime = firstEvt.reaoutTime
        break

    print "Original readout time", originalReadoutTime

    # Get the list of dates in this file, which we're going to use as keys to an event dictionary
    # Declare an empty set, dictionary and list
    # I'm going to use the set to check if there's a new date in this set of events
    # in case there's a new date, I'll declare a new key to the dictionary, and use the empty list as my value
    setOfEventDates = Set([])
    myEvtDict = {}    
    sillyCounter = 0


    for evt in myTree:
        # Converting wierd ass pyROOT buffer into list
        myNCRThits = [nHit for nHit in evt.nCRThits]
        thisEvent = event(evt.date, myNCRThits)
        thisDateTS = evt.date # Get the time stamp
        thisDate =  (datetime.utcfromtimestamp(thisDateTS)).date() # Get the date only from the time stamp
        # if this is a new date (not in the set if event dates), create a new key-value pair 
        if thisDate not in setOfEventDates:
            setOfEventDates.add(thisDate)
            myEvtDict[thisDate] =  [thisEvent]       # Make a list with this event as only element
        # if the date was already there, just append this event
        else:
            myEvtDict[thisDate].append(thisEvent)

    #print time.time() - start_time, "3" 
    # Great, now I should have a dictionary containing 
    # {date : list of events for that date}
    # we'll loop on the date and save in a out root file :
    # hitMean[72], chi2[72], dof[72], probability for poissonian fit [72], readout time
    
    for key, value in myEvtDict.iteritems() :
        print time.time() - start_time
        analyze(key,value,febIndex, originalReadoutTime)

    #print time.time() - start_time, "4" 

__main__()
print time.time() - start_time 





'''

# Declare output file
ourFile = TFile("crt_"+filename,"recreate");

singleTime = TH1D("singleTime", "singleTime",30,-0.5,29.5)
doubleTime = TH1D("doubleTime", "doubleTime",30,-0.5,29.5)


myDic     = {}
emptyList = []
for i in xrange(72):
    myDic[i] = emptyList

# Loop on TTree
for firstEvt in g:
    date = firstEvt.date
    print datetime.utcfromtimestamp(date)
    for i in xrange(72):
        puppa = firstEvt.nCRThits[i]
#        myDic[i].append(puppa)
#        print puppa, i, myDic[i]
    break

#print myDic


# Dates
doubleTime_l = []



for firstEvt in g:
    date_l.add(firstEvt.date)
#    for i in xrange(72):
#        if firstEvt.febIndex[i] == 15:
#            print i
    puppa = firstEvt.nCRThits[46]

    singleTime.Fill(puppa)
    doubleTime_l.append(puppa)

doubleTime_l.append(1)
print len(doubleTime_l), (len(doubleTime_l) % 2)
raw_input()
temp = [sum(doubleTime_l[i:i+2]) for i in range(0, len(doubleTime_l), 2)]
for i in temp:
    doubleTime.Fill(i)

singleTime.Draw()
doubleTime.Draw("sames")
raw_input()





'''


