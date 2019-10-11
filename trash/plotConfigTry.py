from ROOT import *
import os
import math
import argparse
import numpy as np
from array import array
import argparse
import re


class configPlot:	
      def __init__(self, name1, name2, histoName1, histoName2, histoTitle, legend1, legend2):
      	  self.name1       = name1
	  self.name2       = name2
	  self.histoName1  = histoName1 
	  self.histoName2  = histoName2 
	  self.histoTitle  = histoTitle
	  self.legend1     = legend1
	  self.legend2     = legend2


      def plot(self):
            gStyle.SetOptStat(0)
            fileName1   = self.name1
            fileName2   = self.name2
            histoName1  = self.histoName1
            histoName2  = self.histoName2


            inFile1   = TFile.Open(fileName1)
            inFile2   = TFile.Open(fileName2)

            print histoName1, histoName2
            h1  = inFile1.Get(histoName1)
            h2  = inFile2.Get(histoName2)
            print h1, h2

            h1.SetLineColor(kRed)
            h2.SetLineColor(kRed)

            h1.SetLineWidth(2)
            h2.SetLineWidth(2)


            maxY = h1.GetMaximum() 
            if maxY < h2.GetMaximum():
                  maxY = h2.GetMaximum()



            drawOption1 = "pe"
            drawOption2 = "pesames"
            if re.search('data', fileName1, re.IGNORECASE):
                  h1.SetLineColor(kBlack)
                  h1.SetMarkerStyle(8)
                  h1.SetMarkerSize(0.8)
                  drawOption1 = "pe"


            # Let's draw
            c = TCanvas("c","c",600,600);
            c.SetGrid()
            h1.SetTitle(self.histoTitle)
            h1.GetYaxis().SetRangeUser(0,maxY+maxY*0.2)
            h1.Draw(drawOption1)
            h2.Draw(drawOption2)


            legend = TLegend(.14,.12,.44,.30)
            legend.AddEntry(h1 ,self.legend1)
            legend.AddEntry(h2 ,self.legend2)
            legend.Draw("same")

            print self.histoName1+".png", " <-------------- "
            c.SaveAs(self.histoName1+".png")




