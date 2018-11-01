#!/usr/bin/env python

from plot_common import *
import tdrstyle
import math
import numpy as np
from ROOT import kOrange, kGray, kBlue, TGraph

# set batch
r.gROOT.SetBatch()

####################################################################################################
# Configurables
####################################################################################################
# number of events after reweighting
totEventsReweightByMassEEJJ = [
47423.1306,
47279.5681,
47181.0387,
47115.7260,
47068.5201,
46761.2718,
46971.9570,
46936.9320,
46931.2954,
46725.6480,
46868.1086,
46853.6011,
46830.3250,
46110.9815,
46811.3028,
46637.5660,
46507.9580,
46564.2580,
46756.8257,
46666.5163,
46740.1270,
46585.7628,
46729.0218,
46549.7251,
46562.9398,
46701.9266,
46703.3963,
46703.7814,
46700.3454,
46698.6226,
46689.8764,
46141.5635,
46692.3428,
46679.7604,
45847.1482,
46537.1704,
46562.4153,
]

totEventsReweightByMassENuJJ = [
48447.5449,
47830.0080,
48477.6935,
48558.1581,
48109.7049,
48743.1205,
48394.9186,
48329.4303,
48263.5633,
48503.1492,
48323.7722,
48306.1478,
48481.9128,
48423.7153,
48504.6809,
47979.9805,
47998.6233,
48614.2211,
47990.1985,
47781.5478,
48612.3775,
48401.6911,
48202.5669,
48183.4783,
47716.3061,
47392.3075,
48102.6313,
47194.8867,
48276.6535,
48260.9144,
47138.9126,
47999.5574,
48070.0958,
47362.9520,
48368.1572,
48213.4266,
47661.7800,
]

# $LQDATA/2016analysis/eejj_psk_mar16_fixMuons/output_cutTable_lq_eejj/
finalSelByMassEEJJ = [
    7166.8374,
    9434.4407,
    10951.2579,
    11708.3233,
    12367.7609,
    12632.9982,
    13221.5823,
    13877.4711,
    14472.9466,
    14973.7709,
    15447.7568,
    15901.1619,
    16409.5430,
    16690.5627,
    17343.9671,
    17832.4659,
    18156.5831,
    18724.5940,
    19638.9420,
    20840.7636,
    21727.8344,
    22208.9565,
    22783.2283,
    23195.3524,
    23665.0129,
    24269.9168,
    24499.9590,
    24639.6820,
    24792.7541,
    25126.9894,
    25363.6985,
    25084.7771,
    25323.7285,
    25508.0440,
    25337.4606,
    25939.8869,
    25752.6859,
]

# $LQDATA/2016analysis/enujj_psk_mar16_fixMuons/output_cutTable_lq_enujj_MT/
finalSelByMassENuJJ = [
     3631.2735,
     5161.6103,
     6085.7790,
     7025.2516,
     7680.5303,
     8482.6190,
     8764.8261,
     9224.5740,
     9726.2068,
    10470.5418,
    11113.1594,
    11637.3956,
    12471.8276,
    12887.0175,
    13505.0193,
    13922.4704,
    14389.7403,
    15409.6046,
    15597.6012,
    16120.1797,
    16882.2912,
    18108.4586,
    18683.7304,
    19631.3953,
    19940.8970,
    20568.6421,
    21440.7690,
    21180.2470,
    22270.9085,
    22645.6978,
    22442.2454,
    23170.2428,
    23465.8467,
    23442.3195,
    24246.7121,
    24257.6362,
    24254.7260,
]

masses = [
    200,
    250,
    300,
    350,
    400,
    450,
    500,
    550,
    600,
    650,
    700,
    750,
    800,
    850,
    900,
    950,
    1000,
    1050,
    1100,
    1150,
    1200,
    1250,
    1300,
    1350,
    1400,
    1450,
    1500,
    1550,
    1600,
    1650,
    1700,
    1750,
    1800,
    1850,
    1900,
    1950,
    2000,
]



#FIXME commandline the eejj/enujj switching
doEEJJ= False
doPrelim = False
doSim = True


lumiEnergyString = "35.9 fb^{-1} (13 TeV)"

r.gROOT.SetStyle('Plain')
r.gStyle.SetTextFont ( 42 )
r.gStyle.SetTitleFont ( 42, "XYZ" )
r.gStyle.SetLabelFont ( 42, "XYZ" )
r.gStyle.SetOptTitle(0)
r.gStyle.SetOptStat(0)

tdrstyle.setTDRStyle()

r.gStyle.SetPadTopMargin(0.075);
r.gStyle.SetPadBottomMargin(0.15)
r.gStyle.SetPadLeftMargin(0.15)
r.gStyle.SetPadRightMargin(0.1)
#r.gStyle.SetPadTickX(0)
#r.gStyle.SetPadTickY(0)

# compute effAccGraph
if doEEJJ:
    denom = totEventsReweightByMassEEJJ
    numer = finalSelByMassEEJJ
    ratio = [n/d for n,d in zip(numer,denom)]
else:
    denom = totEventsReweightByMassENuJJ
    numer = finalSelByMassENuJJ
    ratio = [n/d for n,d in zip(numer,denom)]

effAccHist = TGraph(len(masses),np.array(masses,'d'),np.array(ratio,'d'))

effAccHist.SetLineColor(kBlue)
effAccHist.SetMarkerColor(kBlue)

effAccHist.Draw('ap')
effAccHist.GetYaxis().SetTitle( "Acceptance #times efficiency" )
effAccHist.GetYaxis().SetTitleFont(42)
effAccHist.GetYaxis().SetLabelFont(42)
effAccHist.GetYaxis().SetLabelOffset(0.007)
effAccHist.GetYaxis().SetLabelSize(0.06)
effAccHist.GetYaxis().SetTitleOffset(1.)
effAccHist.GetYaxis().SetTitleSize(0.07)
effAccHist.GetYaxis().CenterTitle(1)
#
effAccHist.GetXaxis().SetTitle( '#it{m}_{LQ} [GeV]' )
effAccHist.GetXaxis().SetTitleFont(42)
effAccHist.GetXaxis().SetLabelFont(42)
effAccHist.GetXaxis().SetLabelOffset(0.01)
effAccHist.GetXaxis().SetTitleOffset(1.)
effAccHist.GetXaxis().SetLabelSize(0.06)
effAccHist.GetXaxis().SetTitleSize(0.07)
effAccHist.GetXaxis().SetNdivisions(505)


canv_name = "effAcc_LQ" + "" + "_canv"
pad_name  = "effAcc_LQ" + "" + "_pad"
save_name = "effAcc_LQ" + "" 
#save_name = save_name.replace("PAS", "preselection")
if doEEJJ:
  save_name = save_name + "_eejj.pdf"
else:
  save_name = save_name + "_enujj.pdf"
save_name_png = save_name.replace('.pdf','.png')

canvas = r.TCanvas(canv_name,canv_name,800,600)
canvas.cd()
pad1  = r.TPad( pad_name+"1", pad_name+"1" , 0.0, 0.0, 1.0, 1.0 )
pad1.Draw()

#r.SetOwnership(pad1, False)
pad1.cd()
effAccHist.Draw('ap')
effAccHist.GetYaxis().SetRangeUser(0,max(ratio)*1.3)
effAccHist.GetXaxis().SetRangeUser(min(masses)-50,max(masses)+50)
pad1.Draw()


##if doEEJJ:
##    leg = r.TLegend(0.1867,0.5,0.4,0.78,"","brNDC")
##else:
##    leg = r.TLegend(0.175,0.47,0.38,0.8,"","brNDC")
#leg = r.TLegend(0.1867,0.5,0.4,0.78,"","brNDC")
#leg.SetTextFont(42)
#leg.SetFillColor(0)
#leg.SetFillStyle(0)
#leg.SetBorderSize(0)
##leg.SetTextSize(.05)
#leg.SetTextSize(.06)
#if not doEEJJ:
#    leg.SetHeader('e#nujj')
#else:
#    leg.SetHeader('eejj')
#header = leg.GetListOfPrimitives().First()
#header.SetTextFont(42)
#header.SetTextSize(0.06)
#leg.AddEntry(effAccHist,"S_{T}","lp")
#leg.Draw()

canvas.RedrawAxis('G')
canvas.RedrawAxis()
canvas.Modified()
# redraw frame
r.gPad.Update()
line = r.TLine(r.gPad.GetUxmin(),r.gPad.GetUymin(),r.gPad.GetUxmax(),r.gPad.GetUymin())
line.Draw()
line = r.TLine(r.gPad.GetUxmax(),r.gPad.GetUymin(),r.gPad.GetUxmax(),r.gPad.GetUymax())
line.Draw()
r.gPad.Update()

# CMS/lumi/energy
l1 = r.TLatex()
l1.SetTextAlign(12)
l1.SetTextFont(42)
l1.SetNDC()
l1.SetTextSize(0.06)
l1.DrawLatex(0.595,0.965,lumiEnergyString)

l2 = r.TLatex()
l2.SetTextAlign(12)
l2.SetTextFont(62)
l2.SetNDC()
l2.SetTextSize(0.07)

l3 = r.TLatex()
l3.SetTextAlign(12)
l3.SetTextFont(42)
l3.SetNDC()
l3.SetTextSize(0.07)
if doPrelim:
  l3.DrawLatex(0.32,0.84,"#it{Preliminary}")
if doSim:
  l3.DrawLatex(0.32,0.84,"#it{Simulation}")
l2.DrawLatex(0.19,0.84,"CMS")
r.gPad.Update()


l4 = r.TLatex()
l4.SetTextAlign(12)
l4.SetTextFont(42)
l4.SetNDC()
l4.SetTextSize(0.05)
if doEEJJ:
  l4.DrawLatex(0.19,0.77,"eejj")
else:
  l4.DrawLatex(0.19,0.77,"e#nujj")

canvas.Draw()
#if not r.gROOT.IsBatch():
#    ## wait for input to keep the GUI (which lives on a ROOT event dispatcher) alive
#    if __name__ == '__main__':
#       rep = ''
#       while not rep in [ 'c', 'C' ]:
#          rep = raw_input( 'enter "c" to continue: ' )
#          if 1 < len(rep):
#             rep = rep[0]
## FOR TESTING
##break

print 'saving the canvas'
canvas.SaveAs(save_name)
canvas.SaveAs(save_name_png)


#print 'closing files...',
#bkgd_file.Close()
#qcd_file.Close()
#print 'Done!'

