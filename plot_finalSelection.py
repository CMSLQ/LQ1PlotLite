#!/usr/bin/env python

from plot_common import *
import tdrstyle
import math
from ROOT import kOrange, kGray, kBlue


def GetBackgroundSyst(syst_background_names, selection_name, backgroundSystDict, allBkg, zjets, ttbar, qcd, isEEJJ):
  systDictValsNames = {}
  for syst in backgroundSystDict.keys():
    for ibkg,background_name in enumerate(syst_background_names):
      if background_name=='' or 'QCD' in background_name or 'TTBarFromDATA' in background_name:
        continue
      #if selectionName not in backgroundSystDict[syst][background_name].keys():
      #    selectionNameBkgSyst = maxLQselectionBkg
      #else:
      #    selectionNameBkgSyst = selectionName
      selectionNameBkgSyst = selection_name
      try:
          # deltaX/X
          systVal = backgroundSystDict[syst][background_name][selectionNameBkgSyst]
          systDictValsNames[systVal] = '['+syst+']['+background_name+']['+selectionNameBkgSyst+']'
          print 'taking into account systVal of',systVal,'(*allBkg=',systVal*allBkg,') for systematic:',syst,'on background:',background_name,'for selection:',selectionNameBkgSyst
      except KeyError:
          print 'Got a KeyError with: backgroundSystDict['+syst+']['+background_name+']['+selectionNameBkgSyst+']'
  totalSyst = 0.0
  for val,item in systDictValsNames.iteritems():
    totalSyst+=pow(float(val)*allBkg,2)
    print 'add',pow(float(val)*allBkg,2),'to totalSyst','total is now:',math.sqrt(totalSyst),'compared to allBkg=',allBkg,'item is:',item
  # that is on all background
  ## mine
  if isEEJJ:
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
    totalSyst += qcdTerm+ttbarNormTerm+zjetsNormTerm+ttShapeTerm+zShapeTerm
  else:
    #'qcdNorm' : 20,
    qcdTerm = pow(qcd*0.2,2)
    #'ttbarNorm' : 1,
    ttbarNormTerm = pow(ttbar*0.01,2)
    #'wjetsNorm' : 1,
    wjetsNormTerm = pow(zjets*0.01,2)
    ##special
    # 'ttshape' : 7.31,
    #ttShapeTerm = pow(ttbar*0.0731,2)
    #ttShapeTerm = 0
    # 'wshape' : 8.28,
    #wShapeTerm = pow(zjets*0.08,2)
    #
    totalSyst += qcdTerm+ttbarNormTerm+wjetsNormTerm
  print 'added norm terms to totalSyst, which is now:',math.sqrt(totalSyst),'allBkg=',allBkg
  totalSyst = math.sqrt(totalSyst)
  return totalSyst


# set batch
r.gROOT.SetBatch()

####################################################################################################
# Configurables
####################################################################################################
#FIXME commandline the eejj/enujj switching
doEEJJ=False
doSystErr = True
doRatio = False
blind = True

masses = [ 650, 1200 ]

mass_colors = [ 28, 38 ]

varsEEJJ     = [ 
    "sT_eejj",
    "Mej_selected_min",
    "Meejj"
] 

x_labelsEEJJ = [ 
    "S_{T}^{eejj} [GeV]",
    "M_{ej}^{min} [GeV]",
    "M_{eejj} [GeV]"
]

x_binsEEJJ = [ 
    [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980, 3000]
]

varsENUJJ     = [ 
    "ST",
    "Mej"
] 

x_labelsENUJJ = [ 
    "S_{T}^{e#nujj} [GeV]",
    "M_{ej} [GeV]",
]

x_binsENUJJ = [ 
    [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980]
]

if doEEJJ:
  vars = varsEEJJ
  x_labels = x_labelsEEJJ
  x_bins = x_binsEEJJ
  File_preselection = os.environ["LQDATA"]+'/2016analysis/'+   'eejj_psk_nov24_fixTrigEff_finalSels_muonVetoDef35GeV_nEleGte2/output_cutTable_lq_eejj/analysisClass_lq_eejj_plots.root'
  datFile_preselection = os.environ["LQDATA"]+'/2016analysis/'+'eejj_psk_nov24_fixTrigEff_finalSels_muonVetoDef35GeV_nEleGte2/output_cutTable_lq_eejj/analysisClass_lq_eejj_tables.dat'
  File_QCD_preselection = os.environ["LQDATA"]+'/2016qcd/'+   'eejj_psk_nov27_finalSels_muonVeto35GeV_nEleGte2/output_cutTable_lq_eejj_QCD/analysisClass_lq_eejj_QCD_plots.root'
  datFile_QCD_preselection = os.environ["LQDATA"]+'/2016qcd/'+'eejj_psk_nov27_finalSels_muonVeto35GeV_nEleGte2/output_cutTable_lq_eejj_QCD/analysisClass_lq_eejj_QCD_tables.dat'
  File_ttbar = os.environ["LQDATA"]+'/2016ttbar/'+ 'nov19_emujj/output_cutTable_lq_ttbar_emujj_correctTrig/analysisClass_lq_ttbarEst_plots.root'
  #
  bkgd_file = r.TFile.Open(File_preselection)
  bkgd_dat_file = open(datFile_preselection)
  qcd_file = r.TFile.Open(File_QCD_preselection)
  qcd_dat_file = open(datFile_QCD_preselection)
  ttbar_file = r.TFile.Open(File_ttbar)
  #
  systematicsNamesBackground = [ "Trigger", "Reco", "PU", "PDF", "Lumi", "JER", "JEC", "HEEP", "E_scale", "EER", "DYShape" ]
  syst_background_names = ['GJets', 'QCDFakes_DATA', 'TTBarFromDATA', 'DY', 'WJets', 'Diboson', 'Singletop']
  # allBkg, zjets, ttbar, qcd
  #FIXME must update by hand at the moment; should extract from dat files
  yields = {650: [32.71,15.14,8.05,0.08], 1200: [2.33,1.59,0.0,0.01]}
  statUncerts = {650: [], 1200: []}
else:
  vars = varsENUJJ
  x_labels = x_labelsENUJJ
  x_bins = x_binsENUJJ
  File_preselection     = os.environ["LQDATA"]+"/2016analysis/"+"enujj_psk_jan20_usePtHeep_finalSels/output_cutTable_lq_enujj_MT/analysisClass_lq_enujj_MT_plots.root"
  datFile_preselection  = os.environ["LQDATA"]+"/2016analysis/"+"enujj_psk_jan20_usePtHeep_finalSels/output_cutTable_lq_enujj_MT/analysisClass_lq_enujj_MT_tables.dat"
  File_QCD_preselection = os.environ["LQDATA"]+"/2016qcd/"+   "enujj_newRsk237_jan20_finalSels/output_cutTable_lq_enujj_MT_QCD/analysisClass_lq_enujj_QCD_plots.root"
  datFile_QCD_preselection = os.environ["LQDATA"]+"/2016qcd/"+"enujj_newRsk237_jan20_finalSels/output_cutTable_lq_enujj_MT_QCD/analysisClass_lq_enujj_QCD_tables.dat"
  #
  bkgd_file = r.TFile(File_preselection)
  bkgd_dat_file = open(datFile_preselection)
  qcd_file  = r.TFile(File_QCD_preselection)
  qcd_dat_file  = open(datFile_QCD_preselection)
  #
  systematicsNamesBackground = [ "Trigger", "Reco", "PU", "PDF", "Lumi", "JER", "JEC", "HEEP", "E_scale", "EER", "MET", "WShape", "TTShape" ]
  syst_background_names = ['GJets', 'QCDFakes_DATA', 'TTbar', 'DY', 'WJets', 'Diboson', 'Singletop']
  # allBkg, zjets, ttbar, qcd
  #FIXME must update by hand at the moment; should extract from dat files
  yields = {650: [73.25,27.9,14.41,4.93], 1200: [8.39,4.33,0.53,0.38]}
  statUncerts = {650: [], 1200: [5.19]}


lumiEnergyString = "35.9 fb^{-1} (13 TeV)"

systematics_filepaths = {}
for systName in systematicsNamesBackground:
  if doEEJJ:
    systematics_filepaths[systName] = '/afs/cern.ch/user/m/mbhat/work/public/Systematics_4eejj_05_09_2017/'
  else:
    systematics_filepaths[systName] = '/afs/cern.ch/user/m/mbhat/work/public/Systematics_4enujj_1_09_2017/'
backgroundSystDict = FillSystDicts(systematicsNamesBackground,syst_background_names,systematics_filepaths)

r.gROOT.SetStyle('Plain')
r.gStyle.SetTextFont ( 42 )
r.gStyle.SetTitleFont ( 42, "XYZ" )
r.gStyle.SetLabelFont ( 42, "XYZ" )
r.gStyle.SetOptTitle(0)
r.gStyle.SetOptStat(0)

tdrstyle.setTDRStyle()

r.gStyle.SetPadTopMargin(0.1);
r.gStyle.SetPadBottomMargin(0.16)
r.gStyle.SetPadLeftMargin(0.12)
r.gStyle.SetPadRightMargin(0.1)
r.gStyle.SetPadTickX(0)
r.gStyle.SetPadTickY(0)


for i_mass, mass in enumerate(masses):
  if doSystErr:
    backgroundSyst = GetBackgroundSyst(syst_background_names,'LQ'+str(mass),backgroundSystDict,
            yields[mass][0],yields[mass][1],yields[mass][2],yields[mass][3],doEEJJ)
    backgroundSyst /= yields[mass][0]

  for i_var, var in enumerate(vars):
    print 'examine var:',var
    if doEEJJ:
      zjets_hist = bkgd_file.Get( "histo1D__ZJet_amcatnlo_ptBinned__"          + var + "_LQ" + str(mass) )
      ttbar_hist = ttbar_file.Get( "histo1D__TTBarFromDATA__"                  + var + "_LQ" + str(mass) )
      other_hist = bkgd_file.Get( "histo1D__OTHERBKG_WJetPt_amcAtNLODiboson__" + var + "_LQ" + str(mass) )
    else:
      zjets_hist = bkgd_file.Get( "histo1D__WJet_amcatnlo_ptBinned__"          + var + "_LQ" + str(mass) )
      ttbar_hist = bkgd_file.Get( "histo1D__TTbar_powheg__"                    + var + "_LQ" + str(mass) )
      other_hist = bkgd_file.Get( "histo1D__OTHERBKG_ZJetPt_amcAtNLODiboson__" + var + "_LQ" + str(mass) )
    qcd_hist   = qcd_file .Get( "histo1D__QCDFakes_DATA__"                     + var + "_LQ" + str(mass) )
    if not blind:
      data_hist  = bkgd_file.Get( "histo1D__DATA__"                              + var + "_LQ" + str(mass) )
    sig_hist  = bkgd_file.Get( "histo1D__LQ_M"+str(mass)+"__"                  + var + "_LQ" + str(mass) )
  
    ## do not rebin Pt
    zjets_hist = rebin ( zjets_hist, x_bins[i_var] )
    ttbar_hist = rebin ( ttbar_hist, x_bins[i_var] )
    other_hist = rebin ( other_hist, x_bins[i_var] )
    qcd_hist   = rebin ( qcd_hist  , x_bins[i_var] )
    if not blind:
      data_hist  = rebin ( data_hist , x_bins[i_var] )
    sig_hist   = rebin ( sig_hist , x_bins[i_var] )
    #zjets_hist.Rebin (2)
    #ttbar_hist.Rebin (2)
    #other_hist.Rebin (2)
    #qcd_hist  .Rebin (2)
    #data_hist .Rebin (2)
    #sig_hist .Rebin (2)
  
    setStyle (zjets_hist, 2 , 3004, 1)
    setStyle (ttbar_hist, 4 , 3005, 1)
    setStyle (other_hist, 3 , 3006, 1)
    setStyle (qcd_hist  , 7 , 3013, 1)
    setStyle (sig_hist  , mass_colors[i_mass],    0, 3)
    if not blind:
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
    
    canv_name = var + "_LQ" + str(mass) + "_canv"
    pad_name  = var + "_LQ" + str(mass) + "_pad"
    save_name = var + "_LQ" + str(mass) 
    #save_name = save_name.replace("PAS", "preselection")
    if doEEJJ:
      save_name = save_name + "_eejj.pdf"
      save_name_png = save_name + '_eejj.png'
    else:
      save_name = save_name + "_enujj.pdf"
      save_name_png = save_name + '_enujj.png'
  
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
        if blind:
            print 'ERROR: cannot do data/background ratio when blinded...'
            exit(-1)
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
        if doSystErr:
            bgRatioErrs = h_ratio1.Clone()
            bgRatioErrs.Reset()
            bgRatioErrs.SetName('bgRatioErrs')
            for binn in range(0,bgRatioErrs.GetNbinsX()):
                #bgRatioErrs.SetBinContent(binn, zjets_hist.GetBinContent(binn)+ttbar_hist.GetBinContent(binn)+other_hist.GetBinContent(binn)+qcd_hist.GetBinContent(binn))
                bgRatioErrs.SetBinContent(binn,1.0)
            for binn in range(0,bgRatioErrs.GetNbinsX()):
                bgRatioErrs.SetBinError(binn, bgRatioErrs.GetBinContent(binn)*backgroundSyst)
            #for binn in range(0,bgRatioErrs.GetNbinsX()):
            #    print 'bin=',bgRatioErrs.GetBinContent(binn),'+/-',bgRatioErrs.GetBinError(binn)
            #bgRatioErrs.SetFillColor(kOrange-6)
            bgRatioErrs.SetFillColor(kGray+2)
            bgRatioErrs.SetLineColor(kGray+2)
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
            bgRatioErrs.Draw('E2 same')
  
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
        for binn in range(0,bgErrs.GetNbinsX()):
            print 'bin=',bgErrs.GetBinContent(binn),'+/-',bgErrs.GetBinError(binn)
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
    
    sig_hist.Draw("HIST SAME")
    # convert to Poisson error bars
    # check if we need to stop error bars before the end
    if not blind:
      lastPopBin = getLastPopulatedBin([zjets_hist,ttbar_hist,other_hist,qcd_hist,data_hist,sig_hist])
      #print 'last pop bin center = ', data_hist.GetBinCenter(lastPopBin)
      g = poissonErrGraph(data_hist,lastPopBin)
      #g.Draw("ZPSAME")
      g.Draw("ZP0SAME")
  
  
    #leg = r.TLegend(0.42,0.52,0.87,0.88,"","brNDC")
    #leg = r.TLegend(0.43,0.53,0.89,0.89,"","brNDC") #used for all lq2 data plots
    leg = r.TLegend(0.43,0.58,0.67,0.89,"","brNDC")
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(.05)
    if not blind:
      leg.AddEntry(data_hist ,"Data","lpe")
    if doEEJJ:
      leg.AddEntry(zjets_hist,"Z/#gamma* + jets","lf")
    else:
      leg.AddEntry(zjets_hist,"W + jets","lf")
    leg.AddEntry(ttbar_hist,"t#bar{t}","lf")
    leg.AddEntry(other_hist,"Other background","lf")
    if doSystErr:
      leg.AddEntry(bgErrs, 'Uncertainty band','f')
    leg.AddEntry(qcd_hist  ,"Multijet","lf")
    if doEEJJ:
      beta = 1.0
    else:
      beta = 0.5
    leg.AddEntry(sig_hist  ,"LQ, M = "+str(mass)+" GeV, #beta = "+str(beta),"l")
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
    l1.DrawLatex(0.59,0.94,lumiEnergyString)
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
    canvas.SaveAs(save_name_png)


#print 'closing files...',
#bkgd_file.Close()
#qcd_file.Close()
#print 'Done!'

