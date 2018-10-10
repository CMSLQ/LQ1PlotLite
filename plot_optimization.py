#!/usr/bin/env python

from plot_common import *
import tdrstyle
import math
from ROOT import kOrange, kGray, kBlue, TH1F

#+------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+------+------+------+------+------+------+------+------+--------+
#| Var/LQMass | 200 | 250 | 300 | 350 | 400 | 450 | 500 | 550 | 600 | 650  | 700  | 750  | 800  | 850  | 900  | 950  | 1000 | >=1050 |
#+------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+------+------+------+------+------+------+------+------+--------+
#| sT         | 320 | 395 | 475 | 550 | 630 | 705 | 780 | 855 | 930 | 1000 | 1075 | 1145 | 1215 | 1290 | 1360 | 1425 | 1495 | 1565   |
#| Mej        | 140 | 185 | 230 | 275 | 320 | 365 | 405 | 445 | 480 | 515  | 550  | 585  | 620  | 650  | 680  | 705  | 730  | 755    |
#| Mee        | 120 | 145 | 165 | 185 | 200 | 220 | 235 | 245 | 260 | 270  | 280  | 285  | 290  | 295  | 300  | 300  | 300  | 300    |
#+------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+------+------+------+------+------+------+------+------+--------+

# parse the pretty table and return hists
def ParseTable(isEEJJ,tableFile,verbose=False):
    nBins = 37 # M=200 to M=2000
    histList = []
    histList.append(r.TH1F('var1','var1',37,200,2050))
    histList.append(r.TH1F('var2','var2',37,200,2050))
    histList.append(r.TH1F('var3','var3',37,200,2050))
    histList.append(r.TH1F('var4','var4',37,200,2050))

    with open(tableFile) as myFile:
        histIdx = 0
        for line in myFile:
            ibin = 1
            split = line.split('|')
            if len(split) < 2:
                continue
            if 'Var' in split[0] or 'Var' in split[1]:
                continue
            if verbose:
                print 'consider line:',line
                print 'split=',split
            lastItem = -1
            for item in split:
                try:
                    num = float(item)
                except:
                    continue
                if verbose:
                    print 'item=',item
                if len(item) < 3:
                    continue
                histList[histIdx].SetBinContent(ibin,float(item))
                if verbose:
                    print 'hist:',histIdx,'set bin:',ibin,'to',float(item)
                ibin+=1
                lastItem = float(item)
            for ibin in xrange(ibin,38):
                histList[histIdx].SetBinContent(ibin,lastItem)
            histIdx+=1
    return histList


# set batch
r.gROOT.SetBatch()


####################################################################################################
# Configurables
####################################################################################################
#FIXME commandline the eejj/enujj switching
doEEJJ= True
doPrelim = False

if doEEJJ:
    tableFilePath = os.environ["LQANA"] + '/versionsOfAnalysis_eejj/nov24_muonVeto35GeV/opt/optThresholds.txt'
else:
    tableFilePath = os.environ["LQANA"] + '/versionsOfAnalysis_enujj/jan17/opt_jan19/optThresholds.log'


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


print 'Using table file:',tableFilePath
# parse the table file
histList = ParseTable(doEEJJ,tableFilePath)
st_hist = histList[0]
mej_hist = histList[1]
mee_hist = histList[2] # M_T for enujj
if not doEEJJ:
    met_hist = histList[3]

st_hist.SetLineColor(1)
st_hist.SetMarkerColor(1)
mej_hist.SetLineColor(2)
mej_hist.SetMarkerColor(2)
mee_hist.SetLineColor(4)
mee_hist.SetMarkerColor(4)
if not doEEJJ:
    met_hist.SetLineColor(8)
    met_hist.SetMarkerColor(8)
for hist in histList:
    hist.SetLineWidth(2)

st_hist.Draw('lp')
st_hist.GetYaxis().SetTitle( "Threshold [GeV]" )
#st_hist.GetYaxis().CenterTitle()
st_hist.GetYaxis().SetTitleFont(42)
st_hist.GetYaxis().SetLabelFont(42)
st_hist.GetYaxis().SetLabelOffset(0.007)
st_hist.GetYaxis().SetLabelSize(0.05)
st_hist.GetYaxis().SetTitleOffset(1.1)
st_hist.GetYaxis().SetTitleSize(0.06)
#st_hist.GetYaxis().CenterTitle(1)
#
st_hist.GetXaxis().SetTitle( 'M_{LQ} [GeV]' )
#st_hist.GetXaxis().CenterTitle()
st_hist.GetXaxis().SetTitleFont(42)
st_hist.GetXaxis().SetLabelFont(42)
st_hist.GetXaxis().SetLabelOffset(0.02)
st_hist.GetXaxis().SetTitleOffset(1.1)
st_hist.GetXaxis().SetLabelSize(0.05)
st_hist.GetXaxis().SetTitleSize(0.06)
#st_hist.GetXaxis().CenterTitle(1)

mej_hist.Draw('samelp')
mee_hist.Draw('samelp')
if not doEEJJ:
    met_hist.Draw('samelp')

canv_name = "opt_LQ" + "" + "_canv"
pad_name  = "opt_LQ" + "" + "_pad"
save_name = "opt_LQ" + "" 
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
st_hist.Draw('lp')
st_hist.GetYaxis().SetRangeUser(0,st_hist.GetMaximum()*1.3)
st_hist.GetXaxis().SetTitle( 'M_{LQ} [GeV]' )
pad1.Draw()


mej_hist.Draw('samelp')
mee_hist.Draw('samelp')
if not doEEJJ:
    met_hist.Draw('samelp')

if doEEJJ:
    leg = r.TLegend(0.1867,0.5,0.4,0.78,"","brNDC")
else:
    leg = r.TLegend(0.175,0.47,0.38,0.8,"","brNDC")
leg.SetTextFont(42)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
#leg.SetTextSize(.05)
leg.SetTextSize(.06)
if not doEEJJ:
    leg.SetHeader('e#nujj')
else:
    leg.SetHeader('eejj')
header = leg.GetListOfPrimitives().First()
header.SetTextFont(42)
header.SetTextSize(0.06)
leg.AddEntry(st_hist,"S_{T}","lp")
if doEEJJ:
    leg.AddEntry(mej_hist,"M^{min}_{ej}","lp")
    leg.AddEntry(mee_hist,"M_{ee}","lp")
else:
    leg.AddEntry(mej_hist,"M_{ej}","lp")
    leg.AddEntry(mee_hist,"M_{T}","lp")
    leg.AddEntry(met_hist,"p^{miss}_{T}","lp")
leg.Draw()

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
  l3.DrawLatex(0.30,0.83,"#it{Preliminary}")
l2.DrawLatex(0.19,0.84,"CMS")
r.gPad.Update()


#l4 = r.TLatex()
#l4.SetTextAlign(12)
#l4.SetTextFont(42)
#l4.SetNDC()
#l4.SetTextSize(0.05)
#l4.DrawLatex(0.19,0.77,"eejj")

if not r.gROOT.IsBatch():
    ## wait for input to keep the GUI (which lives on a ROOT event dispatcher) alive
    if __name__ == '__main__':
       rep = ''
       while not rep in [ 'c', 'C' ]:
          rep = raw_input( 'enter "c" to continue: ' )
          if 1 < len(rep):
             rep = rep[0]
## FOR TESTING
##break

print 'saving the canvas'
canvas.SaveAs(save_name)
canvas.SaveAs(save_name_png)


#print 'closing files...',
#bkgd_file.Close()
#qcd_file.Close()
#print 'Done!'

