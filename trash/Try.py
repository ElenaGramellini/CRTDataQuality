
import plotConfigTry


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


with open("short") as f:
    for fLine in f:
        print fLine.rstrip('\n')
        w = fLine.split("_")
        print w[len(w) - 1]
        conf = plotConfigTry.configPlot("ExtUnbiased/CRTDataQuality_RatePerDate_ExtUn.root",
                                        "BNBExt/CRTDataQuality_RatePerDate.root",
                                        fLine.rstrip('\n'),
                                        fLine.rstrip('\n'),
                                        "; ;  "+ str(w[len(w) - 1]) +" Rate",
                                        "External Unbiased",
                                        "BNB External")


        conf.plot()


