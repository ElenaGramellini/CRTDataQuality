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
import time 
startTime = time.time()


# I need to re-define an event cause the ROOT memory management is horrific
# So, when looping on the TTree, I'll construct my own event class
class event:
    def __init__(self, date, nTracks, nMatchedTracks):
        self.date             = date
        self.nTracks         = nTracks
        self.nMatchedTracks  = nMatchedTracks



# function that analyzes events in one date
def analyze(date, eventList):

    outFile = TFile("rootFilesTrackMatch/Track_CRT_DQ_"+str(date)+".root","recreate")
    # Declare the final histograms
    histoF  = TH1D("nTracks"       ,"N Tracks; N Tracks; Count ",70,-0.5,69.5)
    histoFM = TH1D("nTracksMatched","N Tracks Matched; N Matched; Count ",70,-0.5,69.5)
    hFMEff  = TH1D("nFMEff"         ,"Track-CRT Matching Efficiency; Efficiency; Count ",50,0,1.0)

    # Fill the Histograms
    for e in eventList:
        print e.nTracks, e.nMatchedTracks, "<--"
        histoF .Fill(e.nTracks)
        histoFM.Fill(e.nMatchedTracks)
        if (e.nTracks > 0):
            hFMEff .Fill(float(e.nMatchedTracks)/float(e.nTracks))


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
    



    # Get the list of dates in this file, which we're going to use as keys to an event dictionary
    # Declare an empty set, dictionary and list
    # I'm going to use the set to check if there's a new date in this set of events
    # in case there's a new date, I'll declare a new key to the dictionary, and use the empty list as my value
    setOfEventDates = Set([])
    myEvtDict = {}    
    sillyCounter = 0


    for evt in myTree:
        thisDateTS         = evt.date # Get the time stamp
        thisDate           = (datetime.utcfromtimestamp(thisDateTS)).date() # Get the date only from the time stamp
        thisEvent          = event(evt.date, evt.nTracks, evt.nMatchedTracks)

        # if this is a new date (not in the set if event dates), create a new key-value pair 
        if thisDate not in setOfEventDates:
            setOfEventDates.add(thisDate)
            myEvtDict[thisDate] =  [thisEvent]       # Make a list with this event as only element
        # if the date was already there, just append this event
        else:
            myEvtDict[thisDate].append(thisEvent)


    # Great, now I should have a dictionary containing 
    # {date : list of events for that date}
    # we'll loop on the date and save in a out root file :
    # hitMean[72], chi2[72], dof[72], probability for poissonian fit [72], readout time

    for key, value in myEvtDict.iteritems() :
        print time.time() - startTime
        analyze(key,value)

    print time.time() - startTime

__main__()





