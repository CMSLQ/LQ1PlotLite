#!/usr/bin/env python

from plot_common import *
import tdrstyle
import math
from ROOT import kOrange, kGray, kBlue, kRed, kCyan, kGreen, TH1F, TGraphAsymmErrors, Double, TLine


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
doPrelim = False
doSystErr = True
doRatio = True
blind = False

if doEEJJ:
    tableFilePath = os.environ["LQANA"] + '/versionsOfAnalysis_eejj/mar17/scaled/table_mar19.txt'
else:
    tableFilePath = os.environ["LQANA"] + '/versionsOfAnalysis_enujj/mar17/scaled/table_mar19.txt'


r.gROOT.SetStyle('Plain')
r.gStyle.SetTextFont ( 42 )
r.gStyle.SetTitleFont ( 42, "XYZ" )
r.gStyle.SetLabelFont ( 42, "XYZ" )
r.gStyle.SetOptTitle(0)
r.gStyle.SetOptStat(0)

tdrstyle.setTDRStyle()

r.gStyle.SetPadTopMargin(0.075);
r.gStyle.SetPadBottomMargin(0.02)
r.gStyle.SetPadLeftMargin(0.14)
r.gStyle.SetPadRightMargin(0.04)


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

setStackHistosStyle([zjets_hist,ttbar_hist,other_hist,qcd_hist,sig_hist,data_hist])

stack = r.THStack ("stack", "stack")
stack.Add ( qcd_hist   )
#stack.Add ( vv_hist    )
stack.Add ( other_hist )
stack.Add ( ttbar_hist )
stack.Add ( zjets_hist )
stack.Draw()
if doEEJJ:
  stack.SetMaximum(2000000)
else:
  stack.SetMaximum(20000000);
stack.SetMinimum(0.1)
bkgTotalHist = stack.GetStack().Last() # sum of all TH1 in stack

stkSystErrHistos = [ copy.deepcopy(h) for h in [qcd_hist,other_hist,ttbar_hist,zjets_hist] ]

setStackYAxisStyle(stack)

if not doRatio:
    setStackNoRatioXAxisStyle(stack)
else:
    setStackWithRatioXAxisStyle(stack)

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
#pad1  = r.TPad( pad_name+"1", pad_name+"1" , 0.0, 0.0, 1.0, 1.0 )
#pad1.Draw()
#
##r.SetOwnership(pad1, False)
#pad1.cd()
#stack.Draw('hist')
#stack.GetYaxis().SetRangeUser(1e-1,stack.GetMaximum()*1.1)
#stack.GetXaxis().SetTitle( 'M_{LQ} [GeV]' )
##canvas.SetLogy()
#pad1.SetLogy()
#pad1.Draw()
if not doRatio:
    pad1  = r.TPad( pad_name+"1", pad_name+"1" , 0.0, 0.0, 1.0, 1.0 )
    pad1.Draw()
else:
    pad1 = r.TPad(pad_name+"1", pad_name+"1", 0.00, 0.275, 0.99, 0.99)
    pad2 = r.TPad(pad_name+"2", pad_name+"2", 0.00, 0.00, 0.99, 0.275)
    pad1.SetFillColor(0)
    pad1.SetLineColor(0)
    pad2.SetFillColor(0)
    pad2.SetLineColor(0)
    #r.SetOwnership(pad2, False)
    pad1.Draw()
    pad2.Draw()

pad1.cd()
stack.Draw('hist')
stack.GetYaxis().SetRangeUser(1e-1,stack.GetMaximum()*1.1)
#stack.GetXaxis().SetTitle( 'M_{LQ} [GeV]' )
#canvas.SetLogy()
pad1.SetLogy()
pad1.Draw()

#sig_hist.Draw("HIST SAME")
sig_hist.Draw("SAME")

if doSystErr:
    for ibin in xrange(0,bkgUncHisto.GetNbinsX()+2):
        bkgUncHisto.SetBinError(ibin,bkgUncHisto.GetBinContent(ibin))
        bkgUncHisto.SetBinContent(ibin,bkgTotalHist.GetBinContent(ibin))
        #print 'set bkgUncHist bin:',ibin,'to',bkgUncHisto.GetBinContent(ibin),'with error:',bkgUncHisto.GetBinError(ibin)
        if bkgUncHisto.GetBinContent(ibin) == 0:
            bkgUncHisto.SetBinContent(ibin,1e-10)
            bkgUncHisto.SetBinError(ibin,1e-10)
    setBkgUncHistStyle(bkgUncHisto)
    bkgUncHisto.SetMinimum(0.1)
    bkgUncHisto.SetMaximum(stack.GetMaximum())
    #bkgUncHisto.GetYaxis().SetRangeUser(1e-1,stack.GetMaximum()*1.1)
    bkgUncHisto.Draw("E2same")

# convert to Poisson error bars
# check if we need to stop error bars before the end
if not blind:
    lastPopBin = getLastPopulatedBin([zjets_hist,ttbar_hist,other_hist,qcd_hist,data_hist,sig_hist])
    #print 'last pop bin center = ', data_hist.GetBinCenter(lastPopBin)
    g = poissonErrGraph(data_hist,lastPopBin)
    # for constant width plots, no horizontal error bars
    for iPoint in range(0,g.GetN()):
      g.SetPointEXlow(iPoint, 0)
      g.SetPointEXhigh(iPoint, 0)
    #g.Draw("ZPSAME")
    g.Draw("ZP0SAME")
#data_hist.Draw('pesame')

#-- 2nd pad (ratio)
if doRatio:
    if blind:
        print 'ERROR: cannot do data/background ratio when blinded...'
        exit(-1)
    h_bkgTot = copy.deepcopy(bkgTotalHist)
    h_ratio = copy.deepcopy(data_hist)
    h_nsigma = copy.deepcopy(data_hist)
    #h_bkgTot1 = TH1F()
    #h_ratio1 = TH1F()
    #h_nsigma1 = TH1F()
    #h_bkgTot1 = h_bkgTot
    h_bkgTot1 = bkgUncHisto # for ratio, divide using bkgTot with error=sqrt[stat^2+syst^2]
    #h_ratio1 = h_ratio
    h_ratio1 = TGraphAsymmErrors()
    h_nsigma1 = h_nsigma
    h_ratioSyst = copy.deepcopy(h_ratio)

    pad2.cd()
    # fPads2.SetLogy()
    #pad2.SetGridy()
    
    h_ratio1.Divide(h_ratio,h_bkgTot1,'pois')
    # for constant width plots, no horizontal error bars
    for iPoint in range(0,h_ratio1.GetN()):
      h_ratio1.SetPointEXlow(iPoint, 0)
      h_ratio1.SetPointEXhigh(iPoint, 0)

    # this part resets bin error/content to -1 if the ratio is zero or negative for some reason so that the point in such a bin isn't drawn
    #oldRatioHist = copy.deepcopy(h_ratio1)
    #h_ratio1.Delete()
    #del h_ratio1
    ##h_ratio1.Reset()
    #h_ratio1 = TH1F('ratio','ratio',oldRatioHist.GetNbinsX(),oldRatioHist.GetXaxis().GetXbins().GetArray())
    #for ibin in range(0,oldRatioHist.GetNbinsX()+1):
    #    oldBinContent = oldRatioHist.GetBinContent(ibin)
    #    if oldBinContent > 0:
    #        #print '1) set bin content for bin:',ibin,'to:',oldBinContent
    #        h_ratio1.SetBinContent(ibin,oldBinContent)
    #        h_ratio1.SetBinError(ibin,oldRatioHist.GetBinError(ibin))
    #    #elif h_bkgTot1.GetBinContent(ibin) > 0:
    #    #    print '2) set bin content for bin:',ibin,'to:',oldBinContent
    #    #    h_ratio1.SetBinContent(ibin,oldBinContent)
    #    #    h_ratio1.SetBinError(ibin,oldRatioHist.GetBinError(ibin))
    #    else:
    #        #print '3) set bin content for bin:',ibin,'to -1'
    #        h_ratio1.SetBinContent(ibin,-1)
    #        h_ratio1.SetBinError(ibin,-1)

    setRatio1NoBGErrStyle(h_ratio1, '#it{M}_{LQ} [GeV]')
    pad2.SetBottomMargin(0.6)
    
    setRatio1MarkerStyle(h_ratio1)

    #h_ratio1.Draw("e0")
    # used for th1f
    #h_ratio1.Draw('p')
    h_ratio1.Draw('z0')

    if doSystErr:
        h_bkgUnc1 = copy.deepcopy(bkgUncHisto)
        # set bin error to the relative error on the background
        for ibin in xrange(0,h_bkgUnc1.GetNbinsX()+2):
            #print '[h_bkgUnc1 with name',h_bkgUnc1.GetName(),'] bin with center',h_bkgUnc1.GetBinCenter(ibin),'bin content is:',h_bkgUnc1.GetBinContent(ibin),'error is:',h_bkgUnc1.GetBinError(ibin)
            if h_bkgUnc1.GetBinContent(ibin) != 0:
                print '[h_bkgUnc1 with name',h_bkgUnc1.GetName(),'] bin with center',h_bkgUnc1.GetBinCenter(ibin),'bin content is:',h_bkgUnc1.GetBinContent(ibin),'error is:',h_bkgUnc1.GetBinError(ibin),'relative error=',h_bkgUnc1.GetBinError(ibin)/h_bkgUnc1.GetBinContent(ibin)
                h_bkgUnc1.SetBinError(ibin,h_bkgUnc1.GetBinError(ibin)/h_bkgUnc1.GetBinContent(ibin))
            h_bkgUnc1.SetBinContent(ibin,1.0)
        bgRatioErrs = h_bkgUnc1

        setBGRatioErrStyle(bgRatioErrs, '#it{M}_{LQ} [GeV]')
        bgRatioErrs.GetXaxis().SetLabelOffset(0.07)
        bgRatioErrs.GetXaxis().SetTitleOffset(1.1)

        bgRatioErrs.Draw('E2')
        h_ratio1.Draw("pz0same")
        bgRatioErrs.GetYaxis().SetRangeUser(0.,2)


    h_ratio1.GetYaxis().SetRangeUser(0.,2)

    lineAtOne = TLine(pad1.GetUxmin(),1,pad1.GetUxmax(),1)
    lineAtOne.SetLineColor(1)
    lineAtOne.Draw()
    pad1.cd()


# redraw stack and data on top
stack.Draw('histsame')
sig_hist.Draw("HIST SAME")
g.Draw("pz0SAME")

#leg = r.TLegend(0.43,0.53,0.89,0.89,"","brNDC") #used for all lq2 data plots
#leg = r.TLegend(0.43,0.58,0.67,0.89,"","brNDC")
leg = r.TLegend(0.5430,0.4073,0.8924,0.897,"","brNDC")
setLegendStyle(leg)
if not blind:
  leg.AddEntry(data_hist ,"Data","lpe")
if doEEJJ:
  leg.AddEntry(zjets_hist,"Z/#gamma* + jets","f")
else:
  leg.AddEntry(zjets_hist,"W + jets","f")
leg.AddEntry(ttbar_hist,"t#bar{t}","f")
leg.AddEntry(qcd_hist  ,"Multijet","f")
leg.AddEntry(other_hist,"Other background","f")
if doSystErr:
  leg.AddEntry(bkgUncHisto, 'Stat#oplussyst uncertainty','f')
if doEEJJ:
  beta = 1.0
else:
  beta = 0.5
leg.AddEntry(sig_hist  ,"LQ signal, #beta = "+str(beta),"l")
leg.Draw()

pad1.RedrawAxis('G')
pad1.RedrawAxis()
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
l2 = r.TLatex()
drawLumiEnergyAndCMSStrings(l1,l2,False)
l2.DrawLatex(0.18,0.84,"CMS")

l3 = r.TLatex()
if doPrelim:
    drawPrelim(l3)

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

