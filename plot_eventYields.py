#!/usr/bin/env python

from plot_common import *
import tdrstyle
import math
from ROOT import kOrange, kGray, kBlue, TH1F


## return lists of masses, vjets, ttbar, qcd, vv, other, data
#def ParseDatacard(cardFilePath):
#    masses = []
#    vjets = []
#    ttbar = []
#    qcd = []
#    vv = []
#    other = []
#    data = []
#    with open(cardFilePath) as myFile:
#        for line in myFile:
#            if '.txt' in line:
#                masses.append(int(line.split('_')[1].split('.')[0][1:]))
#            elif 'observation' in line:
#                data.append(float(line.split()[1]))
#            elif 'rate' in line:

# parse the pretty table and return hists
def ParseTable(isEEJJ,tableFile,verbose=False):
    nBins = 37 # M=200 to M=2000
    vjets = r.TH1F('vjets','vjets',37,200,2050)
    ttbar = r.TH1F('ttbar','ttbar',37,200,2050)
    qcd = r.TH1F('qcd','qcd',37,200,2050)
    vv = r.TH1F('vv','vv',37,200,2050)
    singletop = r.TH1F('singletop','singletop',37,200,2050)
    smallVJets = r.TH1F('smallVJets','smallVJets',37,200,2050)
    gammajets = r.TH1F('gammajets','gammajets',37,200,2050)
    bkgUnc = r.TH1F('bkgUnc','bkgUnc',37,200,2050)
    data = r.TH1F('data','data',37,200,2050)
    signal = r.TH1F('signal','signal',37,200,2050)
    histList = [signal,vjets,ttbar,qcd,vv,singletop,smallVJets,gammajets,bkgUnc,data]
    # order for eejj
    #|       MLQ        |         signal        |       Z+jets       |    ttbar(data)     |   QCD(data)    |     DIBOSON      |     SingleTop      |       W+Jets      |     PhotonJets     |              Total BG              |   Data  |
    with open(tableFile) as myFile:
        ibin = 0
        for line in myFile:
            split = line.split('|')
            if len(split) < 2:
                continue
            if not 'LQ_' in split[1] or 'presel' in split[1]:
                continue
            if verbose:
                print 'consider line:',line
                print 'split=',split
            ibin+=1
            histIdx = -1
            for item in split:
                if verbose:
                    print 'item=',item
                # split the "item" which is the event yield per category, into yield, stat (and/or syst)
                yieldList = item.strip().split()
                if len(yieldList) < 1:
                    continue
                if verbose:
                    print yieldList
                if 'presel' in yieldList[0]:
                    break # ignore preselection line
                elif 'LQ' in yieldList[0]:
                    continue # skip first column for regular LQ mass points
                else:
                    histIdx+=1
                    if histIdx==8: #bkgUnc
                        # need to deal with yieldList like ['1329.54^{+24.2}_{-23.85}', '\\pm', '24.44'] or ['2543.44', '+/-', '34.41', '+/-', '68.87']
                        if '^' in yieldList[0]:
                            stat1 = float(yieldList[0][yieldList[0].find('+')+1:yieldList[0].find('}')])
                            stat2 = float(yieldList[0][yieldList[0].find('-')+1:-2])
                            stat = max(stat1,stat2)
                            if verbose:
                                print 'found stat=',stat
                            syst = float(yieldList[2])
                            if verbose:
                                print 'found syst=',syst
                            statSyst = math.sqrt(stat**2+syst**2)
                            histList[histIdx].SetBinContent(ibin,statSyst)
                        elif '+/-' in yieldList[1]:
                            stat = float(yieldList[2])
                            if verbose:
                                print 'found stat=',stat
                            syst = float(yieldList[4])
                            if verbose:
                                print 'found syst=',syst
                            statSyst = math.sqrt(stat**2+syst**2)
                            histList[histIdx].SetBinContent(ibin,statSyst)
                        if verbose:
                            print 'hist:',histIdx,'set bin:',ibin,'to',statSyst
                    else:
                        histList[histIdx].SetBinContent(ibin,float(yieldList[0]))
                        if verbose:
                            print 'hist:',histIdx,'set bin:',ibin,'to',float(yieldList[0])
    return histList


# set batch
r.gROOT.SetBatch()


####################################################################################################
# Configurables
####################################################################################################
#FIXME commandline the eejj/enujj switching
doEEJJ= False
doPrelim = True
doSystErr = True
doRatio = True
blind = False

if doEEJJ:
    tableFilePath = os.environ["LQANA"] + '/versionsOfAnalysis_eejj/mar17/scaled/table_mar19.txt'
else:
    tableFilePath = os.environ["LQANA"] + '/versionsOfAnalysis_enujj/mar17/scaled/table_mar19.txt'


lumiEnergyString = "35.9 fb^{-1} (13 TeV)"

r.gROOT.SetStyle('Plain')
r.gStyle.SetTextFont ( 42 )
r.gStyle.SetTitleFont ( 42, "XYZ" )
r.gStyle.SetLabelFont ( 42, "XYZ" )
r.gStyle.SetOptTitle(0)
r.gStyle.SetOptStat(0)

tdrstyle.setTDRStyle()

r.gStyle.SetPadTopMargin(0.075);
r.gStyle.SetPadBottomMargin(0.125)
r.gStyle.SetPadLeftMargin(0.12)
r.gStyle.SetPadRightMargin(0.1)
#r.gStyle.SetPadTickX(0)
#r.gStyle.SetPadTickY(0)


print 'Using table file:',tableFilePath
# parse the table file
histList = ParseTable(doEEJJ,tableFilePath)
sig_hist = histList[0]
zjets_hist = histList[1]
ttbar_hist = histList[2]
qcd_hist = histList[3]

#vv_hist = histList[4]
other_hist = histList[5]
other_hist.Add(histList[6])
other_hist.Add(histList[7])
other_hist.Add(histList[4])

bkgUncHisto = histList[8]
data_hist = histList[9]
# combine 'other' bkg components into 'other' hist

setStyle (zjets_hist, 2 , 3004, 1)
setStyle (ttbar_hist, 4 , 3005, 1)
#setStyle (vv_hist   , 4 , 3005, 1)
setStyle (other_hist, 3 , 3006, 1)
setStyle (qcd_hist  , 7 , 3013, 1)
setStyle (sig_hist  , 28,    2, 3)
sig_hist.SetLineStyle(2)

if not blind:
  setStyle (data_hist , 1 ,    0, 1)
  data_hist.SetMarkerStyle(20)
  data_hist.SetMarkerSize (1.1)

stack = r.THStack ("stack", "stack")
stack.Add ( qcd_hist   )
#stack.Add ( vv_hist    )
stack.Add ( other_hist )
stack.Add ( ttbar_hist )
stack.Add ( zjets_hist )
stack.Draw()
if doEEJJ:
  stack.SetMaximum(200000)
else:
  stack.SetMaximum(20000000);
stack.SetMinimum(0.1)
bkgTotalHist = stack.GetStack().Last() # sum of all TH1 in stack

stkSystErrHistos = [ copy.deepcopy(h) for h in [qcd_hist,other_hist,ttbar_hist,zjets_hist] ]

for ibin in xrange(0,bkgUncHisto.GetNbinsX()+2):
    bkgUncHisto.SetBinError(ibin,bkgUncHisto.GetBinContent(ibin))
    bkgUncHisto.SetBinContent(ibin,bkgTotalHist.GetBinContent(ibin))
    #print 'set bkgUncHist bin:',ibin,'to',bkgUncHisto.GetBinContent(ibin),'with error:',bkgUncHisto.GetBinError(ibin)
bkgUncHisto.SetMarkerStyle(0)
bkgUncHisto.SetLineColor(0)
bkgUncHisto.SetFillColor(kGray+2)
bkgUncHisto.SetLineColor(kGray+2)
bkgUncHisto.SetFillStyle(3001)
bkgUncHisto.SetMarkerSize(0)

stack.GetYaxis().SetTitle( "Events / bin" )
stack.GetYaxis().CenterTitle()
stack.GetYaxis().SetTitleFont(42)
stack.GetYaxis().SetLabelFont(42)
stack.GetYaxis().SetLabelOffset(0.007)
stack.GetYaxis().SetLabelSize(0.05)
stack.GetYaxis().SetTitleOffset(0.92)
stack.GetYaxis().SetTitleSize(0.06)
stack.GetYaxis().CenterTitle(1)

stack.GetXaxis().SetTitle( 'M_{LQ} [GeV]' )
stack.GetXaxis().CenterTitle()
stack.GetXaxis().SetTitleFont(42)
stack.GetXaxis().SetLabelFont(42)
stack.GetXaxis().SetLabelOffset(0.007)
stack.GetXaxis().SetTitleOffset(0.92)
stack.GetXaxis().SetLabelSize(0.05)
stack.GetXaxis().SetTitleSize(0.06)
stack.GetXaxis().CenterTitle(1)

canv_name = "eventYield_LQ" + "FinalSelections" + "_canv"
pad_name  = "eventYield_LQ" + "FinalSelections" + "_pad"
save_name = "eventYield_LQ" + "FinalSelections" 
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
stack.Draw('hist')
stack.GetYaxis().SetRangeUser(1e-1,stack.GetMaximum()*1.1)
stack.GetXaxis().SetTitle( 'M_{LQ} [GeV]' )
#canvas.SetLogy()
pad1.SetLogy()
pad1.Draw()

bkgUncHisto.Draw("E2same")

sig_hist.Draw("HIST SAME")
## convert to Poisson error bars
## check if we need to stop error bars before the end
#if not blind:
#  lastPopBin = getLastPopulatedBin([zjets_hist,ttbar_hist,other_hist,qcd_hist,data_hist,sig_hist])
#  #print 'last pop bin center = ', data_hist.GetBinCenter(lastPopBin)
#  g = poissonErrGraph(data_hist,lastPopBin)
#  #g.Draw("ZPSAME")
#  g.Draw("ZP0SAME")
data_hist.Draw('pesame')

#if doSystErr:
#  verbose=False
#  bkgUncHisto = copy.deepcopy(stack.GetStack().Last())
#  bkgUncHisto.Reset()
#  bkgUncHisto.SetNameTitle('bkgUncHisto','bkgUncHisto')
#  for idx,hist in enumerate(stkSystErrHistos):
#      syst = systs[idx]
#      if verbose:
#        print '[',hist.GetName(),']: look at systs['+str(idx)+']'
#      for ibin in xrange(0,hist.GetNbinsX()+2):
#          hist.SetBinError(ibin,syst*hist.GetBinContent(ibin))
#          if verbose:
#            print '[',hist.GetName(),'] set bin with center',hist.GetBinCenter(ibin),'error to:',syst*hist.GetBinContent(ibin)
#      bkgUncHisto.Add(hist)
#  ##histoAll = copy.deepcopy(bkgTotalHist)
#  #histoAll = thStack.GetStack().Last()
#  #bkgUncHisto = copy.deepcopy(histoAll)
#  #for bin in range(0,histoAll.GetNbinsX()):
#  #    bkgUncHisto.SetBinError(bin+1,self.bkgSyst*histoAll.GetBinContent(bin+1))
#  bkgUncHisto.SetMarkerStyle(0)
#  bkgUncHisto.SetLineColor(0)
#  bkgUncHisto.SetFillColor(kGray+2)
#  bkgUncHisto.SetLineColor(kGray+2)
#  bkgUncHisto.SetFillStyle(3001)
#  bkgUncHisto.SetMarkerSize(0)
#  bkgUncHisto.Draw("E2same")
#  if verbose:
#    for ibin in xrange(0,bkgUncHisto.GetNbinsX()+2):
#        print '[',bkgUncHisto.GetName(),'] bin with center',bkgUncHisto.GetBinCenter(ibin),'error is:',bkgUncHisto.GetBinError(ibin)


#leg = r.TLegend(0.43,0.53,0.89,0.89,"","brNDC") #used for all lq2 data plots
#leg = r.TLegend(0.43,0.58,0.67,0.89,"","brNDC")
leg = r.TLegend(0.56,0.53,0.75,0.88,"","brNDC")
leg.SetTextFont(42)
leg.SetFillColor(0)
leg.SetBorderSize(0)
#leg.SetTextSize(.05)
leg.SetTextSize(.04)
if not blind:
  leg.AddEntry(data_hist ,"Data","lpe")
if doEEJJ:
  leg.AddEntry(zjets_hist,"Z/#gamma* + jets","lf")
else:
  leg.AddEntry(zjets_hist,"W + jets","lf")
leg.AddEntry(ttbar_hist,"t#bar{t}","lf")
leg.AddEntry(qcd_hist  ,"Multijet","lf")
leg.AddEntry(other_hist,"Other background","lf")
if doSystErr:
  leg.AddEntry(bkgUncHisto, 'stat + syst uncertainty','f')
if doEEJJ:
  beta = 1.0
else:
  beta = 0.5
leg.AddEntry(sig_hist  ,"LQ signal, #beta = "+str(beta),"l")
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

