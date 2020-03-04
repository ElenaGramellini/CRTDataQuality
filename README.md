# Uncorrected rate
To produce plots for the uncorrected rate:
> python AnaCRTDataQualityUncorrectedRates.py ../run3/CRTDataQualityAll_BNBExtRun3_crthitcorr.root >> uncorrected.log &
to produce the sumary plots
> python FinalPlotsCRTDataQualityUncorrectedRate.py
the root file will end up in the "perDatePlots" folder

# CRT-Flash match
To produce plots for the CRT-Flash matching efficiency
> python FlashCRTDataQuality.py ../run3/CRTDataQualityAll_BNBExtRun3_crthitcorr.root >> flashMatch.log &
to produce the sumary plots
> python FlashFinalPlotsCRTDataQuality.py
the root file will end up in the "perDatePlots" folder


# CRT-Track match
To produce plots for the CRT-Track matching efficiency
> python TrackCRTDataQuality.py ../run3/CRTDataQualityAll_BNBExtRun3_crthitcorr.root >> trackMatch.log &


# Study of the PE
