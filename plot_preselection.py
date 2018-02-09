#!/usr/bin/env python

from plot_common import *
import tdrstyle
import math
from ROOT import kOrange, kGray, kBlue, TGraphAsymmErrors


def GetBackgroundSyst(systType, isEEJJ=True):
    verbose = False
    # /afs/cern.ch/user/m/mbhat/work/public/Systematics_4Preselection_02_11_2017/eejj_Preselection_sys.dat
    #  100*(deltaX/X) [rel. change in %]
    systDictEEJJ = {
      'EER'     : 10.6582,
      'JER'     : 0.785142,
      'JEC'     : 3.57184,
      'HEEP'    : 1.32785,
      'E_RECO'  : 2.13808,
      'EES'     : 1.31244,
      'PileUp'  : 7.24591,
      'PDF'     : 1.10962,
      'DYShape' : 9.92748,
      'Lumi'    : 2.6,
      'Trigger' : 1.033228,
    }
    # /afs/cern.ch/user/m/mbhat/work/public/Systematics_4Preselection_02_11_2017/enujj_Preselection_sys.dat
    systDictENuJJ = {
      'EER'     : 4.668,
      'JER'     : 0.98,
      'JEC'     : 4.13745,
      'HEEP'    : 0.652002,
      'RECO'    : 1.01663,
      'EES'     : 1.69524,
      'PileUp'  : 9.99836,
      'PDF'     : 1.61953,
      'TTShape' : 6.4724,
      'WShape'  : 9.7182,
      'MET'     : 6.14723,
      'Lumi'    : 2.6,
      'Trigger' : 2.56837,
    }
    if isEEJJ:
      systDict = systDictEEJJ
    else:
      systDict = systDictENuJJ
    preselSyst = 0.0
    for key in systDict.iterkeys():
      # for QCD, take only QCD uncert
      if 'qcd' in systType.lower():
        break
      # for data-driven ttbar, take only its uncert
      if 'data' in systType.lower():
        break
      if not 'tt' in systType.lower() and 'ttshape' in key.lower():
        continue
      if not 'wjets' in systType.lower() and 'wshape' in key.lower():
        continue
      if not 'zjets' in systType.lower() and not 'dyjets' in systType.lower() and 'dyshape' in key.lower():
        continue
      item = float(systDict[key])/100.0
      preselSyst+=pow(item,2)
    if verbose:
      print 'MC background systematic for systType=',systType,'(relative):',math.sqrt(preselSyst)
    # that is on all MC background
    ## mine
    term = 0
    if isEEJJ:
      #'qcdNorm' : 50,
      if 'qcd' in systType.lower():
        term = pow(0.5,2)
      #'ttbarNorm' : 1,
      elif 'tt' in systType.lower():
        term = pow(0.01,2)
      #'zjetsNorm' : 0.75,
      elif 'zjets' in systType.lower() or 'dyjets' in systType.lower():
        term = pow(0.0075,2)
    else:
      #'qcdNorm' : 25,
      if 'qcd' in systType.lower():
        term = pow(0.25,2)
      #'ttbarNorm' : 1,
      elif 'tt' in systType.lower():
        term = pow(0.01,2)
      #'wjetsNorm' : 1,
      elif 'wjets' in systType.lower():
        term = pow(0.01,2)
    preselSyst += term
    preselSyst = math.sqrt(preselSyst)
    if verbose:
      print 'final background systematic for systType=',systType,'(relative):',preselSyst
    return preselSyst

# set batch
r.gROOT.SetBatch()

####################################################################################################
# Configurables
####################################################################################################
#FIXME commandline the eejj/enujj switching
doEEJJ=False
doSystErr = True
doRatio = True

mass1 = 650
mass2 = 1200

mass_colors = [ 28, 38 ]

varsEEJJ     = [ 
    "Pt1stEle_PAS",
    "Pt2ndEle_PAS",
    "Pt1stJet_PAS",
    "Pt2ndJet_PAS",
    "sT_PAS",
    "Mej_selected_min_PAS",
    "Mee_PAS"
] 

x_labelsEEJJ = [ 
    "p_{T} (e_{1}) [GeV]",
    "p_{T} (e_{2}) [GeV]",
    "p_{T} (jet_{1}) [GeV]",
    "p_{T} (jet_{2}) [GeV]",
    "S_{T}^{eejj} [GeV]",
    "M_{ej}^{min} [GeV]",
    "M_{ee} [GeV]"
]

x_binsEEJJ = [ 
    [i*20 for i in range(0,51)],
    [i*20 for i in range(0,51)],
    [i*20 for i in range(0,51)],
    [i*20 for i in range(0,51)],
    [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980]
]

varsENUJJ     = [ 
    "sT_PAS",
    "Mej_PAS",
    "MTenu_PAS",
    "MET_PAS"
] 

x_labelsENUJJ = [ 
    "S_{T}^{e#nujj} [GeV]",
    "M_{ej} [GeV]",
    "M_{T} [GeV]",
    "E_{T}^{miss} [GeV]"
]

x_binsENUJJ = [ 
    [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980]
]

systTypesEEJJ  = ['qcd', 'mc', 'ttbarfromdata', 'zjets']
systTypesENUJJ = ['qcd', 'mc', 'ttbar', 'wjets']

if doEEJJ:
  vars = varsEEJJ
  x_labels = x_labelsEEJJ
  x_bins = x_binsEEJJ
  systTypes = systTypesEEJJ
  File_preselection = os.environ["LQDATA"]+'/2016analysis/'+   'eejj_psk_jan26_gsfEtaCheck_finalSels/output_cutTable_lq_eejj/analysisClass_lq_eejj_plots.root'
  datFile_preselection = os.environ["LQDATA"]+'/2016analysis/'+'eejj_psk_jan26_gsfEtaCheck_finalSels/output_cutTable_lq_eejj/analysisClass_lq_eejj_tables.dat'
  File_QCD_preselection = os.environ["LQDATA"]+'/2016qcd/'+   'eejj_QCD_jan26_gsfEtaCheck_finalSels/output_cutTable_lq_eejj_QCD/analysisClass_lq_eejj_QCD_plots.root'
  datFile_QCD_preselection = os.environ["LQDATA"]+'/2016qcd/'+'eejj_QCD_jan26_gsfEtaCheck_finalSels/output_cutTable_lq_eejj_QCD/analysisClass_lq_eejj_QCD_tables.dat'
  File_ttbar = os.environ["LQDATA"]+'/2016ttbar/'+ 'feb2_newSkim_emujj_correctTrig_finalSelections/output_cutTable_lq_ttbar_emujj_correctTrig/analysisClass_lq_ttbarEst_plots.root'
  #
  bkgd_file = r.TFile.Open(File_preselection)
  bkgd_dat_file = open(datFile_preselection)
  qcd_file = r.TFile.Open(File_QCD_preselection)
  qcd_dat_file = open(datFile_QCD_preselection)
  ttbar_file = r.TFile.Open(File_ttbar)
else:
  vars = varsENUJJ
  x_labels = x_labelsENUJJ
  x_bins = x_binsENUJJ
  systTypes = systTypesENUJJ
  File_preselection     = os.environ["LQDATA"]+"/2016analysis/"+"enujj_psk_feb4_v237_MET100_PtEMET70/output_cutTable_lq_enujj_MT/analysisClass_lq_enujj_MT_plots.root"
  datFile_preselection  = os.environ["LQDATA"]+"/2016analysis/"+"enujj_psk_feb4_v237_MET100_PtEMET70/output_cutTable_lq_enujj_MT/analysisClass_lq_enujj_MT_tables.dat"
  File_QCD_preselection = os.environ["LQDATA"]+"/2016qcd/"+   "/enujj_newRsk237_feb4_gsfEtaCheck_MET100_PtEMET70/output_cutTable_lq_enujj_MT_QCD/analysisClass_lq_enujj_QCD_plots.root"
  datFile_QCD_preselection = os.environ["LQDATA"]+"/2016qcd/"+"/enujj_newRsk237_feb4_gsfEtaCheck_MET100_PtEMET70/output_cutTable_lq_enujj_MT_QCD/analysisClass_lq_enujj_QCD_tables.dat"
  #
  bkgd_file = r.TFile(File_preselection)
  bkgd_dat_file = open(datFile_preselection)
  qcd_file  = r.TFile(File_QCD_preselection)
  qcd_dat_file  = open(datFile_QCD_preselection)


lumiEnergyString = "35.9 fb^{-1} (13 TeV)"

r.gROOT.SetStyle('Plain')
r.gStyle.SetTextFont ( 42 )
r.gStyle.SetTitleFont ( 42, "XYZ" )
r.gStyle.SetLabelFont ( 42, "XYZ" )
r.gStyle.SetOptTitle(0)
r.gStyle.SetOptStat(0)

tdrstyle.setTDRStyle()

r.gStyle.SetPadTopMargin(0.075);
r.gStyle.SetPadBottomMargin(0.02)
r.gStyle.SetPadLeftMargin(0.12)
r.gStyle.SetPadRightMargin(0.1)


if doSystErr:
  #FIXME parse this from the dat files...
  systs = [GetBackgroundSyst(systType,doEEJJ) for systType in systTypes]

for i_var, var in enumerate(vars):
    print 'examine var:',var
    if doEEJJ:
      zjets_hist = bkgd_file.Get( "histo1D__ZJet_amcatnlo_ptBinned__"     + var  )
      ttbar_hist = ttbar_file.Get( "histo1D__TTBarFromDATA__"    + var  )
      other_hist = bkgd_file.Get( "histo1D__OTHERBKG_WJetPt_amcAtNLODiboson__"    + var  )
    else:
      zjets_hist = bkgd_file.Get( "histo1D__WJet_amcatnlo_ptBinned__"     + var  )
      ttbar_hist = bkgd_file.Get( "histo1D__TTbar_powheg__"    + var  )
      other_hist = bkgd_file.Get( "histo1D__OTHERBKG_ZJetPt_amcAtNLODiboson__"          + var  )
    qcd_hist   = qcd_file .Get( "histo1D__QCDFakes_DATA__"     + var  )
    data_hist  = bkgd_file.Get( "histo1D__DATA__"              + var  )
    sig1_hist  = bkgd_file.Get( "histo1D__LQ_M"+str(mass1)+"__" + var )
    sig2_hist  = bkgd_file.Get( "histo1D__LQ_M"+str(mass2)+"__" + var )

    ## do not rebin Pt
    # rebinning in var bins with overflow in last bin
    zjets_hist = rebin ( zjets_hist, x_bins[i_var])
    ttbar_hist = rebin ( ttbar_hist, x_bins[i_var])
    other_hist = rebin ( other_hist, x_bins[i_var])
    qcd_hist   = rebin ( qcd_hist  , x_bins[i_var])
    data_hist  = rebin ( data_hist , x_bins[i_var])
    sig1_hist  = rebin ( sig1_hist , x_bins[i_var])
    sig2_hist  = rebin ( sig2_hist , x_bins[i_var])
    #zjets_hist.Rebin (2)
    #ttbar_hist.Rebin (2)
    #other_hist.Rebin (2)
    #qcd_hist  .Rebin (2)
    #data_hist .Rebin (2)
    #sig1_hist .Rebin (2)
    #sig2_hist .Rebin (2)

    setStyle (zjets_hist, 2 , 3004, 1)
    setStyle (ttbar_hist, 4 , 3005, 1)
    setStyle (other_hist, 3 , 3006, 1)
    setStyle (qcd_hist  , 7 , 3013, 1)
    setStyle (sig1_hist , 28,    0, 4)
    setStyle (sig2_hist , 38,    0, 4)
    setStyle (data_hist , 1 ,    0, 1)
    
    data_hist.SetMarkerStyle(20)
    data_hist.SetMarkerSize (1.1)
    
    stack = r.THStack ("stack", "stack")
    stack.Add ( qcd_hist   )
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
    if doEEJJ:
      save_name = save_name + "_eejj.pdf"
    else:
      save_name = save_name + "_enujj.pdf"

    save_namePNG = save_name.replace('.pdf','.png')

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

    sig1_hist.Draw("HIST SAME")
    sig2_hist.Draw("HIST SAME")
    # convert to Poisson error bars
    # check if we need to stop error bars before the end
    lastPopBin = getLastPopulatedBin([zjets_hist,ttbar_hist,other_hist,qcd_hist,data_hist,sig1_hist,sig2_hist])
    #print 'last pop bin center = ', data_hist.GetBinCenter(lastPopBin)
    g = poissonErrGraph(data_hist,lastPopBin)
    #g.Draw("ZPSAME")
    g.Draw("ZP0SAME")

    if doSystErr:
      bkgUncHisto = copy.deepcopy(stack.GetStack().Last())
      bkgUncHisto.Reset()
      for idx,hist in enumerate(stkSystErrHistos):
          syst = systs[idx]
          for ibin in xrange(0,hist.GetNbinsX()+2):
              hist.SetBinError(ibin,syst*hist.GetBinContent(ibin))
              #print '[',hist.GetName(),'] set bin',ibin,'error to:',syst*hist.GetBinContent(ibin)
          bkgUncHisto.Add(hist)
      ##histoAll = copy.deepcopy(bkgTotalHist)
      #histoAll = thStack.GetStack().Last()
      #bkgUncHisto = copy.deepcopy(histoAll)
      #for bin in range(0,histoAll.GetNbinsX()):
      #    bkgUncHisto.SetBinError(bin+1,self.bkgSyst*histoAll.GetBinContent(bin+1))
      bkgUncHisto.SetMarkerStyle(0)
      bkgUncHisto.SetLineColor(0)
      bkgUncHisto.SetFillColor(kGray+2)
      bkgUncHisto.SetLineColor(kGray+2)
      bkgUncHisto.SetFillStyle(3001)
      bkgUncHisto.SetMarkerSize(0)
      bkgUncHisto.Draw("E2same")
      #for ibin in xrange(0,bkgUncHisto.GetNbinsX()+2):
      #    print '[',bkgUncHisto.GetName(),'] bin',ibin,'error is:',bkgUncHisto.GetBinError(ibin)
      

    #-- 2nd pad (ratio)
    if doRatio:
        pad2.cd()
        h_bkgTot = copy.deepcopy(bkgTotalHist)
        h_ratio = copy.deepcopy(data_hist)
        h_nsigma = copy.deepcopy(data_hist)
        #h_bkgTot1 = TH1F()
        #h_ratio1 = TH1F()
        #h_nsigma1 = TH1F()
        h_bkgTot1 = h_bkgTot
        h_bkgUnc1 = copy.deepcopy(bkgUncHisto)
        h_ratio1 = h_ratio
        h_nsigma1 = h_nsigma
        h_ratioSyst = copy.deepcopy(h_ratio1)

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

        #h_ratio1.SetStats(0)

        #if( self.xmin!="" and self.xmax!="" and self.rebin!="var" ):
        #h_bkgTot1.GetXaxis().SetRangeUser(self.xmin,self.xmax-0.000001)
        #h_ratio1.GetXaxis().SetRangeUser(self.xmin,self.xmax-0.000001)
        #h_nsigma1.GetXaxis().SetRangeUser(self.xmin,self.xmax-0.000001)

        #pad2.cd()
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

        h_ratio1.Draw("e0p")

        if doSystErr:
            h_ratioSyst.Divide(h_bkgUnc1) # just divide by the bkgTotal hist with the systs as errors
            bgRatioErrs = h_ratioSyst
            # set bin contents to 1
            for binn in range(0,bgRatioErrs.GetNbinsX()):
                bgRatioErrs.SetBinContent(binn,1.0)
                #print 'ratio hist bin:',binn,'binError=',bgRatioErrs.GetBinError(binn)
            bgRatioErrs.SetFillColor(kGray+1)
            bgRatioErrs.SetLineColor(kGray+1)
            bgRatioErrs.SetFillStyle(3001)
            #bgRatioErrs.SetFillStyle(3018)
            #bgRatioErrs.SetFillStyle(3013)
            #bgRatioErrs.SetMarkerSize(1.1)
            bgRatioErrs.SetMarkerSize(0)
            #bgRatioErrs.SetLineColor(kOrange)
            #bgRatioErrs.SetLineWidth(3)
            #bgRatioErrs.Draw('aE2 aE0 same')
            #bgRatioErrs.SetDrawOption('hist')
            #bgRatioErrs.Draw('aE2 E0 same')
            bgRatioErrs.GetXaxis().SetTitle("")
            bgRatioErrs.GetXaxis().SetTitleSize(0.06)
            bgRatioErrs.GetXaxis().SetLabelSize(0.1)
            bgRatioErrs.GetYaxis().SetRangeUser(0.,2)
            bgRatioErrs.GetYaxis().SetTitle("Data/MC")
            bgRatioErrs.GetYaxis().SetLabelSize(0.1)
            bgRatioErrs.GetYaxis().SetTitleSize(0.13)
            bgRatioErrs.GetYaxis().SetTitleOffset(0.3)
            bgRatioErrs.SetMarkerStyle ( 1 )
            bgRatioErrs.Draw('E2')
            h_ratio1.Draw("e0psame")

            ## need to make hist with "1" in all bins
            #bgRatioErrs = h_ratio1.Clone()
            #bgRatioErrs.Reset()
            #bgRatioErrs.SetName('bgRatioErrs')
            #for binn in range(0,bgRatioErrs.GetNbinsX()):
            #    bgRatioErrs.SetBinContent(binn,1.0)
            #bgRatioErrsGraph = GetErrorsGraph([bgRatioErrs],backgroundSyst)
            #bgRatioErrsGraph.Draw('E2 same')

        #lineAtOne = TLine(h_ratio.GetXaxis().GetXmin(),1,h_ratio.GetXaxis().GetXmax(),1)
        #lineAtOne.SetLineColor(2)
        #lineAtOne.Draw()
        pad1.cd()

    
    #leg = r.TLegend(0.42,0.52,0.87,0.88,"","brNDC")
    #leg = r.TLegend(0.43,0.53,0.89,0.89,"","brNDC") #used for all lq2 data plots
    leg = r.TLegend(0.43,0.58,0.67,0.89,"","brNDC")
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(.05)
    leg.AddEntry(data_hist ,"Data","lpe")
    if doEEJJ:
      leg.AddEntry(zjets_hist,"Z/#gamma* + jets","lf")
    else:
      leg.AddEntry(zjets_hist,"W + jets","lf")
    leg.AddEntry(ttbar_hist,"t#bar{t}","lf")
    leg.AddEntry(other_hist,"Other background","lf")
    if doSystErr:
      leg.AddEntry(bkgUncHisto, 'Uncertainty band','f')
    leg.AddEntry(qcd_hist  ,"Multijet","lf")
    if doEEJJ:
      beta = 1.0
    else:
      beta = 0.5
    leg.AddEntry(sig1_hist  ,"LQ, M = "+str(mass1)+" GeV, #beta = "+str(beta),"l")
    leg.AddEntry(sig2_hist  ,"LQ, M = "+str(mass2)+" GeV, #beta = "+str(beta),"l")
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
    l1.DrawLatex(0.675,0.965,lumiEnergyString)
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
    canvas.SaveAs(save_namePNG)


#print 'closing files...',
#bkgd_file.Close()
#qcd_file.Close()
#print 'Done!'
