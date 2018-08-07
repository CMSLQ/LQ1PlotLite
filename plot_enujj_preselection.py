#!/usr/bin/env python

from plot_common import *
import tdrstyle
import math
from ROOT import kOrange, kGray, kBlue

#FIXME
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
    #'ttbarNorm' : 1,
    ttbarNormTerm = pow(ttbar*0.01,2)
    #'zjetsNorm' : 0.75,
    zjetsNormTerm = pow(zjets*0.0075,2)
    ##special
    # 'ttshape' : 7.31,
    #ttShapeTerm = pow(ttbar*0.0731,2)
    ttShapeTerm = 0
    # 'zshape' : 8.28,
    zShapeTerm = pow(zjets*0.08,2)
    #
    preselSyst += qcdTerm+ttbarNormTerm+zjetsNormTerm+ttShapeTerm+zShapeTerm
    preselSyst = math.sqrt(preselSyst)
    return preselSyst



# set batch
r.gROOT.SetBatch()


mass1 = 650
mass2 = 1200

mass_colors = [ 28, 38 ]

vars     = [ 
    "sT_PAS",
    "Mej_PAS",
    "MTenu_PAS"
] 

x_labels = [ 
    "S_{T}^{e#nujj} [GeV]",
    "M_{ej} [GeV]",
    "M_{T} [GeV]"
]

x_bins = [ 
    [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980]
]

lumiEnergyString = "35.9 fb^{-1} (13 TeV)"

r.gROOT.SetStyle('Plain')
r.gStyle.SetTextFont ( 42 );
r.gStyle.SetTitleFont ( 42, "XYZ" );
r.gStyle.SetLabelFont ( 42, "XYZ" );
r.gStyle.SetOptTitle(0);
r.gStyle.SetOptStat(0);


#set the tdr style
tdrstyle.setTDRStyle()

r.gStyle.SetPadTopMargin(0.075);
r.gStyle.SetPadBottomMargin(0.02);
r.gStyle.SetPadLeftMargin(0.12);
r.gStyle.SetPadRightMargin(0.1);
#r.gStyle.SetPadTickX(0)
#r.gStyle.SetPadTickY(0)

doSystErr = False
doRatio = True

#FIXME
if doSystErr:
  # allbkg, zjets, ttbar, qcd
  #backgroundSyst = GetBackgroundSyst(4237.1,3176.7,897.13,2.7)
  backgroundSyst = GetBackgroundSyst(50632.42,42597.24,6262.92,36.85)
  #print 'BG: 4237.1 +/- '+str(GetBackgroundSyst(4237.1,3176.7,897.13,2.7))
  #backgroundSyst /= 4237.1
  backgroundSyst /= 50632.42

#bkgd_file = r.TFile(os.environ["LQDATA"] + "/LQPlotFiles_fromEdmund/analysisClass_lq_enujj_MT_plots.root" )
#qcd_file  = r.TFile(os.environ["LQDATA"] + "/LQPlotFiles_fromEdmund/analysisClass_lq_enujj_MT_QCD_plots.root")
File_preselection     = os.environ["LQDATA"] + "/2016analysis/enujj_psk_oct8_finerBinnedTrigEff_updatedFinalSels/output_cutTable_lq_enujj_MT/analysisClass_lq_enujj_MT_plots.root"
File_QCD_preselection = os.environ["LQDATA"] + "/2016qcd/enujj_psk_oct8_updatedFinalSels/output_cutTable_lq_enujj_MT_QCD/analysisClass_lq_enujj_QCD_plots.root"
bkgd_file = r.TFile(File_preselection)
qcd_file  = r.TFile(File_QCD_preselection)

for i_var, var in enumerate(vars):

    #wjets_hist = bkgd_file.Get( "histo1D__WJet_Madgraph__"     + var  )
    #ttbar_hist = bkgd_file.Get( "histo1D__TTbar_Madgraph__"    + var  )
    #other_hist = bkgd_file.Get( "histo1D__OTHERBKG__"          + var  )
    #qcd_hist   = qcd_file .Get( "histo1D__DATA__"              + var  )
    wjets_hist = bkgd_file.Get( "histo1D__WJet_amcatnlo_ptBinned__"     + var  )
    ttbar_hist = bkgd_file.Get( "histo1D__TTbar_powheg__"    + var  )
    other_hist = bkgd_file.Get( "histo1D__OTHERBKG_ZJetPt__"          + var  )
    qcd_hist   = qcd_file .Get( "histo1D__QCDFakes_DATA__"              + var  )
    data_hist  = bkgd_file.Get( "histo1D__DATA__"              + var  )
    sig1_hist  = bkgd_file.Get( "histo1D__LQ_M"+str(mass1)+"__" + var )
    sig2_hist  = bkgd_file.Get( "histo1D__LQ_M"+str(mass2)+"__" + var )

    wjets_hist = rebin ( wjets_hist, x_bins[i_var] )
    ttbar_hist = rebin ( ttbar_hist, x_bins[i_var] )
    other_hist = rebin ( other_hist, x_bins[i_var] )
    qcd_hist   = rebin ( qcd_hist  , x_bins[i_var] )
    data_hist  = rebin ( data_hist , x_bins[i_var] )
    sig1_hist  = rebin ( sig1_hist  , x_bins[i_var] )
    sig2_hist  = rebin ( sig2_hist  , x_bins[i_var] )

    setStyle (wjets_hist, 6 , 3007, 1)
    setStyle (ttbar_hist, 4 , 3005, 1)
    setStyle (other_hist, 3 , 3006, 1)
    setStyle (qcd_hist  , 7 , 3013, 1)
    setStyle (sig1_hist , 28,    0, 4)
    setStyle (sig2_hist , 38,    0, 4)
    setStyle (data_hist , 1 ,    0, 1)

    data_hist.SetMarkerStyle(20)
    data_hist.SetMarkerSize (1.5)
    
    stack = r.THStack ("stack", "stack")
    stack.Add ( qcd_hist   );
    stack.Add ( other_hist );
    stack.Add ( ttbar_hist );
    stack.Add ( wjets_hist );
    stack.Draw();
    stack.SetMaximum(20000000);
    stack.SetMinimum(0.1);

    stack.GetXaxis().SetTitle( x_labels [i_var] )
    stack.GetYaxis().SetTitle( "Events / bin" )
    stack.GetXaxis().CenterTitle()
    stack.GetYaxis().CenterTitle()

    stack.GetHistogram().GetXaxis().SetLabelOffset(0.007)
    stack.GetHistogram().GetYaxis().SetLabelOffset(0.007)
    stack.GetHistogram().GetXaxis().SetLabelSize(0.05)
    stack.GetHistogram().GetYaxis().SetLabelSize(0.05)
    
    stack.GetHistogram().GetXaxis().SetTitleOffset(0.92)
    stack.GetHistogram().GetYaxis().SetTitleOffset(0.92)
    stack.GetHistogram().GetXaxis().SetTitleSize(0.06)
    stack.GetHistogram().GetYaxis().SetTitleSize(0.06)
    stack.GetHistogram().GetXaxis().CenterTitle(1)
    stack.GetHistogram().GetYaxis().CenterTitle(1)

    
    stack.GetXaxis().SetTitleFont(42)
    stack.GetYaxis().SetTitleFont(42)
    stack.GetXaxis().SetLabelFont(42)
    stack.GetYaxis().SetLabelFont(42)
    stack.GetXaxis().SetLabelOffset(0.007)
    stack.GetYaxis().SetLabelOffset(0.007)
    stack.GetXaxis().SetLabelSize(0.05)
    stack.GetYaxis().SetLabelSize(0.05)
    
    stack.GetXaxis().SetTitleOffset(0.92)
    stack.GetYaxis().SetTitleOffset(0.92)
    stack.GetXaxis().SetTitleSize(0.06)
    stack.GetYaxis().SetTitleSize(0.06)
    stack.GetXaxis().CenterTitle(1)
    stack.GetYaxis().CenterTitle(1)
    
    
    #leg = r.TLegend(0.43,0.52,0.89,0.88,"","brNDC");
    leg = r.TLegend(0.43,0.53,0.89,0.89,"","brNDC"); #used for LQ2 plots
    leg.SetTextFont(42);
    leg.SetFillColor(0);
    leg.SetBorderSize(0);
    leg.SetTextSize(.05)
    leg.AddEntry(data_hist ,"Data","lpe");
    leg.AddEntry(wjets_hist,"W + jets","lf");
    leg.AddEntry(ttbar_hist,"t#bar{t}","lf");
    leg.AddEntry(other_hist,"Other background","lf");
    leg.AddEntry(qcd_hist  ,"Multijet","lf");
    leg.AddEntry(sig1_hist  ,"LQ, M = "+str(mass1)+" GeV, #beta = 0.5","l");
    leg.AddEntry(sig2_hist  ,"LQ, M = "+str(mass2)+" GeV, #beta = 0.5","l");
    
    canv_name = var + "_canv"
    pad_name  = var + "_pad"
    save_name = var + "_enujj.pdf"
    #save_name = save_name.replace("PAS","preselection")

    canvas = r.TCanvas(canv_name,canv_name,800,550)
    canvas.cd()
    pad1   = r.TPad( pad_name, pad_name , 0.0, 0.0, 1.0, 1.0 )
    canvas.SetLogy()

    stack.Draw("HIST");
    sig1_hist.Draw("HIST SAME");
    sig2_hist.Draw("HIST SAME");
    # convert to Poisson error bars
    g = poissonErrGraph(data_hist)
    g.Draw("ZPSAME")
    leg.Draw()
    canvas.RedrawAxis('G')
    canvas.RedrawAxis()
    # redraw frame
    r.gPad.Update()
    line = r.TLine(r.gPad.GetUxmin(),r.gPad.GetUymin(),r.gPad.GetUxmax(),r.gPad.GetUymin())
    line.Draw()
    line = r.TLine(r.gPad.GetUxmax(),r.gPad.GetUymin(),r.gPad.GetUxmax(),r.gPad.GetUymax())
    line.Draw()
    r.gPad.Update()

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
    l1.DrawLatex(0.64,0.94,"35.9 fb^{-1} (13 TeV)")
    l2.DrawLatex(0.15,0.84,"CMS")

    
    canvas.SaveAs(save_name)

