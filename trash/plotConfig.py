class configPlot:	
      def __init__(self, name1, name2, histoName1, histoName2, histoTitle, legend1, legend2):
      	  self.name1       = name1
	  self.name2       = name2
	  self.histoName1  = histoName1 
	  self.histoName2  = histoName2 
	  self.histoTitle  = histoTitle
	  self.legend1     = legend1
	  self.legend2     = legend2

conf = configPlot("ExtUnbiased/CRTDataQuality_RatePerDate_ExtUn.root",
                  "BNBExt/CRTDataQuality_RatePerDate.root",
                  "hHitsOverEvt_FEB_51",
                  "hHitsOverEvt_FEB_51",
                  "; ; Module 51 Rate",
                  "External Unbiased",
                  "BNB External")
