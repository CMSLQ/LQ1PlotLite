#!/usr/bin/env python

from plot_common import *
import tdrstyle
import math
from ROOT import kOrange, kGray, kBlue


def GetBackgroundSyst(allBkg, zjets, ttbar, qcd):
    # /afs/cern.ch/user/m/mbhat/work/public/Systematics_txtfiles_25_07_2016/pre1_sys.dat
    #  100*(deltaX/X) [rel. change in %]
    systDict = {
      'trig' : 1.16081,
      'pu' : 0.254125,
      'ereco' : 8.58642,
      'ees' : 5.40749,
      'lumi' : 2.7,
      'heepid' : 9.08357,
      'jec' : 2.26787,
      'jer' : 0.0729784,
      'pdf' : 4.7,
    }
    systDictList = systDict.values()
    systDictList = [value/100.0 for value in systDictList]
    preselSyst = 0.0
    for item in systDictList:
      preselSyst+=pow(float(item),2)
    # that is on all background
    ## mine
    #'qcdNorm' : 40,
    qcdTerm = pow(qcd*0.4,2)
    #'ttbarNorm' : 20,
    ttbarNormTerm = pow(ttbar*0.2,2)
    #'zjetsNorm' : 2.6,
    zjetsNormTerm = pow(zjets*0.026,2)
    ##special
    # 'ttshape' : 7.31,
    ttShapeTerm = pow(ttbar*0.0731,2)
    # 'zshape' : 8.28,
    zShapeTerm = pow(zjets*0.0282,2)
    #
    preselSyst += qcdTerm+ttbarNormTerm+zjetsNormTerm+ttShapeTerm+zShapeTerm
    preselSyst = math.sqrt(preselSyst)
    return preselSyst



# set batch
r.gROOT.SetBatch()


mass1 = 650
mass2 = 950

mass_colors = [ 28, 38 ]

vars     = [ 
    "Pt1stEle_PAS",
    "Pt2ndEle_PAS",
    "Pt1stJet_PAS",
    "Pt2ndJet_PAS",
    "sT_PAS",
    "Mej_selected_min_PAS",
    "Mee_PAS"
] 

x_labels = [ 
    "p_{T} (e_{1}) [GeV]",
    "p_{T} (e_{2}) [GeV]",
    "p_{T} (jet_{1}) [GeV]",
    "p_{T} (jet_{2}) [GeV]",
    "S_{T}^{eejj} [GeV]",
    "M_{ej}^{min} [GeV]",
    "M_{ee} [GeV]"
]

x_bins = [ 
    [i*20 for i in range(0,51)],
    [i*20 for i in range(0,51)],
    [i*20 for i in range(0,51)],
    [i*20 for i in range(0,51)],
    [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980]
]

lumiEnergyString = "2.6 fb^{-1} (13 TeV)"

r.gROOT.SetStyle('Plain')
r.gStyle.SetTextFont ( 42 )
r.gStyle.SetTitleFont ( 42, "XYZ" )
r.gStyle.SetLabelFont ( 42, "XYZ" )
r.gStyle.SetOptTitle(0)
r.gStyle.SetOptStat(0)


#set the tdr style
tdrstyle.setTDRStyle()

#r.gStyle.SetPadTopMargin(0.1);
r.gStyle.SetPadTopMargin(0.075);
#r.gStyle.SetPadBottomMargin(0.16);
#r.gStyle.SetPadTopMargin(0.02)
r.gStyle.SetPadBottomMargin(0.02)
r.gStyle.SetPadLeftMargin(0.12)
r.gStyle.SetPadRightMargin(0.1)
#r.gStyle.SetPadTickX(0)
#r.gStyle.SetPadTickY(0)

#print 'GetPreselSyst'
doSystErr = True
doRatio = True

if doSystErr:
  # allbkg, zjets, ttbar, qcd
  backgroundSyst = GetBackgroundSyst(4237.1,3176.7,897.13,2.7)
  #print 'BG: 4237.1 +/- '+str(GetBackgroundSyst(4237.1,3176.7,897.13,2.7))
  backgroundSyst /= 4237.1

#bkgd_file = r.TFile.Open(os.environ["LQDATA"] + "/RunII/eejj_analysis_ttbarRescaleFinalSels_2jun2016/output_cutTable_lq_eejj/analysisClass_lq_eejj_plots.root" )
#qcd_file  = r.TFile.Open(os.environ["LQDATA"] + "/RunII/eejj_analysis_ttbarRescaleFinalSels_2jun2016/output_cutTable_lq_eejj/analysisClass_lq_eejj_QCD_plots.root")
bkgd_file = r.TFile.Open(os.environ["LQDATA"] + "/RunII/eejj_analysis_zJetsStCorrectionFinalSelections_21jul/output_cutTable_lq_eejj/analysisClass_lq_eejj_plots.root" )
qcd_file  = r.TFile.Open(os.environ["LQDATA"] + "/RunII/eejj_analysis_ttbarRescaleFinalSels_updatePlotRanges_29jun2016/output_cutTable_lq_eejj/analysisClass_lq_eejj_QCD_plots.root")

for i_var, var in enumerate(vars):
    print 'examine var:',var
    zjets_hist = bkgd_file.Get( "histo1D__ZJet_Madgraph_HT__"     + var  )
    #ttbar_hist = bkgd_file.Get( "histo1D__TTbar_FromData__"    + var  )
    ttbar_hist = bkgd_file.Get( "histo1D__TTbar_Madgraph__"    + var  )
    other_hist = bkgd_file.Get( "histo1D__OTHERBKG_MG_HT__"    + var  )
    qcd_hist   = qcd_file .Get( "histo1D__QCDFakes_DATA__"     + var  )
    data_hist  = bkgd_file.Get( "histo1D__DATA__"              + var  )
    sig1_hist  = bkgd_file.Get( "histo1D__LQ_M"+str(mass1)+"__" + var )
    sig2_hist  = bkgd_file.Get( "histo1D__LQ_M"+str(mass2)+"__" + var )

    # do not rebin Pt
    zjets_hist = rebin ( zjets_hist, x_bins[i_var] )
    ttbar_hist = rebin ( ttbar_hist, x_bins[i_var] )
    other_hist = rebin ( other_hist, x_bins[i_var] )
    qcd_hist   = rebin ( qcd_hist  , x_bins[i_var] )
    data_hist  = rebin ( data_hist , x_bins[i_var] )
    sig1_hist  = rebin ( sig1_hist , x_bins[i_var] )
    sig2_hist  = rebin ( sig2_hist , x_bins[i_var] )

    setStyle (zjets_hist, 2 , 3004, 1)
    setStyle (ttbar_hist, 4 , 3005, 1)
    setStyle (other_hist, 3 , 3006, 1)
    setStyle (qcd_hist  , 7 , 3013, 1)
    setStyle (sig1_hist , 28,    0, 4)
    setStyle (sig2_hist , 38,    0, 4)
    setStyle (data_hist , 1 ,    0, 1)
    
    data_hist.SetMarkerStyle(20)
    #data_hist.SetMarkerSize (1.5)
    data_hist.SetMarkerSize (1.1)
    
    stack = r.THStack ("stack", "stack")
    stack.Add ( qcd_hist   )
    stack.Add ( other_hist )
    stack.Add ( ttbar_hist )
    stack.Add ( zjets_hist )
    stack.Draw()
    stack.SetMaximum(200000)
    stack.SetMinimum(0.1)
    bkgTotalHist = stack.GetStack().Last() # sum of all TH1 in stack

    stack.GetYaxis().SetTitle( "Events / bin" )
    stack.GetYaxis().CenterTitle()
    stack.GetYaxis().SetTitleFont(42)
    stack.GetYaxis().SetLabelFont(42)
    stack.GetYaxis().SetLabelOffset(0.007)
    stack.GetYaxis().SetLabelSize(0.05)
    stack.GetYaxis().SetTitleOffset(0.92)
    stack.GetYaxis().SetTitleSize(0.06)
    stack.GetYaxis().CenterTitle(1)
    
    if not doRatio:
      stack.GetXaxis().SetTitle( x_labels [i_var] )
      stack.GetXaxis().CenterTitle()
      stack.GetXaxis().SetTitleFont(42)
      stack.GetXaxis().SetLabelFont(42)
      stack.GetXaxis().SetLabelOffset(0.007)
      stack.GetXaxis().SetTitleOffset(0.92)
      stack.GetXaxis().SetLabelSize(0.05)
      stack.GetXaxis().SetTitleSize(0.06)
      stack.GetXaxis().CenterTitle(1)
    else:
      stack.GetXaxis().SetLabelSize(0)
      stack.GetXaxis().SetLabelOffset(0)
      stack.GetXaxis().SetTitleSize(0)
      stack.GetXaxis().SetTitleOffset(0)

    ## reduce x-axis labels for Mej plot
    #if 'Mej' in var:
    #  stack.GetXaxis().SetNdivisions(507)
    
    canv_name = var + "_canv"
    pad_name  = var + "_pad"
    save_name = var 
    #save_name = save_name.replace("PAS", "preselection")
    save_name = save_name + "_eejj.pdf"

    ## WORKS
    #canvas = r.TCanvas(canv_name,canv_name,800,550)
    #canvas.cd()
    #pad1   = r.TPad( pad_name, pad_name , 0.0, 0.0, 1.0, 1.0 )
    #canvas.SetLogy()
    #stack.Draw("HIST")
    ## WORKS

    canvas = r.TCanvas(canv_name,canv_name,800,600)
    canvas.cd()
    canvas.SetLogy()
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

    #r.SetOwnership(pad1, False)
    pad1.cd()
    pad1.SetLogy()
    stack.Draw('hist')
    pad1.Draw()

    #canvas.cd()
    ##canvas.SetLogy()
    #pad1.cd()
    #pad1.SetLogy()
    #stack.Draw("HIST")
    #
    #r.SetOwnership(canvas, False)

    #-- 2nd pad (ratio)
    if doRatio:
        h_bkgTot = copy.deepcopy(bkgTotalHist)
        h_ratio = copy.deepcopy(data_hist)
        h_nsigma = copy.deepcopy(data_hist)
        #h_bkgTot1 = TH1F()
        #h_ratio1 = TH1F()
        #h_nsigma1 = TH1F()
        h_bkgTot1 = h_bkgTot
        h_ratio1 = h_ratio
        h_nsigma1 = h_nsigma

        #if( self.xbins!="" and self.rebin!="var" ): ## Variable binning
        #    xbinsFinal = array( 'd', self.xbins )
        #    length = len(xbinsFinal)-1
        #    h_bkgTot1 = h_bkgTot.Rebin( length , "h_bkgTot1", xbinsFinal)
        #    h_ratio1 = h_ratio.Rebin( length , "h_ratio1" , xbinsFinal)
        #    h_nsigma1 = h_nsigma.Rebin( length, "h_nsigma1", xbinsFinal)
        #else:
        #    h_bkgTot1 = h_bkgTot
        #    h_ratio1 = h_ratio
        #    h_nsigma1 = h_nsigma

        h_ratio1.SetStats(0)
        #if( self.xmin!="" and self.xmax!="" and self.rebin!="var" ):
        #h_bkgTot1.GetXaxis().SetRangeUser(self.xmin,self.xmax-0.000001)
        #h_ratio1.GetXaxis().SetRangeUser(self.xmin,self.xmax-0.000001)
        #h_nsigma1.GetXaxis().SetRangeUser(self.xmin,self.xmax-0.000001)

        pad2.cd()
        # fPads2.SetLogy()
        pad2.SetGridy()
        h_ratio1.Divide(h_bkgTot1)

        #h_ratio1.GetXaxis().SetTitle("")
        #h_ratio1.GetXaxis().SetTitleSize(0.06)
        #h_ratio1.GetXaxis().SetLabelSize(0.1)
        h_ratio1.GetYaxis().SetRangeUser(0.,2)
        #h_ratio1.GetYaxis().SetTitle("Data/MC")
        #h_ratio1.GetYaxis().SetLabelSize(0.1)
        #h_ratio1.GetYaxis().SetTitleSize(0.13)
        #h_ratio1.GetYaxis().SetTitleOffset(0.3)
        h_ratio1.GetYaxis().SetTitle( "data / MC" )
        h_ratio1.GetYaxis().SetTitleFont(42)
        h_ratio1.GetYaxis().SetLabelFont(42)
        h_ratio1.GetYaxis().SetLabelOffset(0.007)
        h_ratio1.GetYaxis().SetLabelSize(0.12)
        h_ratio1.GetYaxis().SetTitleOffset(0.3)
        h_ratio1.GetYaxis().SetTitleSize(0.12)
        h_ratio1.GetYaxis().CenterTitle()
        h_ratio1.GetYaxis().CenterTitle(1)

        h_ratio1.GetXaxis().SetTitle( x_labels [i_var] )
        h_ratio1.GetXaxis().SetTitleFont(42)
        h_ratio1.GetXaxis().SetLabelFont(42)
        h_ratio1.GetXaxis().SetLabelOffset(0.025)
        h_ratio1.GetXaxis().SetTitleOffset(1.1)
        h_ratio1.GetXaxis().SetLabelSize(0.15)
        h_ratio1.GetXaxis().SetTitleSize(0.15)
        #h_ratio1.GetXaxis().CenterTitle()
        #h_ratio1.GetXaxis().CenterTitle(1)
        pad2.SetBottomMargin(0.37)
    
        h_ratio1.SetMarkerStyle ( 20 )
        h_ratio1.SetMarkerSize ( 1 )
        h_ratio1.SetMarkerColor ( kBlue )

        h_ratio1.Draw("p")
        h_ratio1.Draw("p")

        #lineAtOne = TLine(h_ratio.GetXaxis().GetXmin(),1,h_ratio.GetXaxis().GetXmax(),1)
        #lineAtOne.SetLineColor(2)
        #lineAtOne.Draw()
        pad1.cd()


    if doSystErr:
        bgErrs = zjets_hist.Clone()
        bgErrs.Reset()
        bgErrs.SetName('bgErrs')
        for binn in range(0,bgErrs.GetNbinsX()):
            bgErrs.SetBinContent(binn, zjets_hist.GetBinContent(binn)+ttbar_hist.GetBinContent(binn)+other_hist.GetBinContent(binn)+qcd_hist.GetBinContent(binn))
        for binn in range(0,bgErrs.GetNbinsX()):
            bgErrs.SetBinError(binn, bgErrs.GetBinContent(binn)*backgroundSyst)
        #for binn in range(0,bgErrs.GetNbinsX()):
        #    print 'bin=',bgErrs.GetBinContent(binn),'+/-',bgErrs.GetBinError(binn)
        #bgErrs.SetFillColor(kOrange-6)
        bgErrs.SetFillColor(kGray+2)
        bgErrs.SetLineColor(kGray+2)
        bgErrs.SetFillStyle(3001)
        #bgErrs.SetFillStyle(3018)
        #bgErrs.SetFillStyle(3013)
        #bgErrs.SetMarkerSize(1.1)
        bgErrs.SetMarkerSize(0)
        #bgErrs.SetLineColor(kOrange)
        #bgErrs.SetLineWidth(3)
        #bgErrs.Draw('aE2 aE0 same')
        #bgErrs.SetDrawOption('hist')
        #bgErrs.Draw('aE2 E0 same')
        bgErrs.Draw('E2 same')
    
    sig1_hist.Draw("HIST SAME")
    sig2_hist.Draw("HIST SAME")
    # convert to Poisson error bars
    # check if we need to stop error bars before the end
    lastPopBin = getLastPopulatedBin([zjets_hist,ttbar_hist,other_hist,qcd_hist,data_hist,sig1_hist,sig2_hist])
    #print 'last pop bin center = ', data_hist.GetBinCenter(lastPopBin)
    g = poissonErrGraph(data_hist,lastPopBin)
    #g.Draw("ZPSAME")
    g.Draw("ZP0SAME")


    #leg = r.TLegend(0.42,0.52,0.87,0.88,"","brNDC")
    leg = r.TLegend(0.43,0.53,0.89,0.89,"","brNDC") #used for all lq2 data plots
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(.05)
    leg.AddEntry(data_hist ,"Data","lpe")
    leg.AddEntry(zjets_hist,"Z/#gamma* + jets","lf")
    leg.AddEntry(ttbar_hist,"t#bar{t}","lf")
    leg.AddEntry(other_hist,"Other background","lf")
    if doSystErr:
      leg.AddEntry(bgErrs, 'Uncertainty band','f')
    leg.AddEntry(qcd_hist  ,"Multijet","lf")
    leg.AddEntry(sig1_hist  ,"LQ, M = "+str(mass1)+" GeV, #beta = 1.0","l")
    leg.AddEntry(sig2_hist  ,"LQ, M = "+str(mass2)+" GeV, #beta = 1.0","l")
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
    l2 = r.TLatex()
    l2.SetTextAlign(12)
    l2.SetTextFont(62)
    l2.SetNDC()
    l2.SetTextSize(0.08)
    l1.DrawLatex(0.64,0.96,lumiEnergyString)
    l2.DrawLatex(0.15,0.84,"CMS")
    r.gPad.Update()


    #if not r.gROOT.IsBatch():
    #    ## wait for input to keep the GUI (which lives on a ROOT event dispatcher) alive
    #    if __name__ == '__main__':
    #       rep = ''
    #       while not rep in [ 'c', 'C' ]:
    #          rep = raw_input( 'enter "c" to continue: ' )
    #          if 1 < len(rep):
    #             rep = rep[0]
    # FOR TESTING
    #break

    print 'saving the canvas'
    canvas.SaveAs(save_name)


#print 'closing files...',
#bkgd_file.Close()
#qcd_file.Close()
#print 'Done!'

