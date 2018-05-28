#!/usr/bin/env python

from plot_common import *
import tdrstyle
import math
from ROOT import kOrange, kGray, kBlue, TH1F


# from makeDatacard.py
#def GetBackgroundSyst(background_name, selectionName):
#    verbose = False
#    #if selectionName=='preselection':
#    #  verbose=True
#    if verbose:
#      print 'INFO: GetBackgroundSyst('+background_name+','+selectionName+')'
#    firstSyst = 0
#    secondSyst = 0
#    thirdSyst = 0
#    if not 'QCD' in background_name and not 'data' in background_name.lower():
#      for syst in signalSystDict.keys():
#          if selectionName not in backgroundSystDict[syst][background_name].keys():
#              if 'LQ' in selectionName:
#                selectionNameBkgSyst = maxLQselectionBkg
#              else:
#                selectionNameBkgSyst = minLQselectionBkg
#              #print 'selectionName=',selectionName,'not found in',backgroundSystDict[syst][background_name].keys()
#          else:
#              selectionNameBkgSyst = selectionName
#          try:
#            firstSyst += pow(backgroundSystDict[syst][background_name][selectionNameBkgSyst],2) # deltaX/X
#            if verbose:
#              print 'INFO: add',syst,'for',background_name,'at selection',selectionNameBkgSyst,'to firstSyst=',backgroundSystDict[syst][background_name][selectionNameBkgSyst]
#          except KeyError:
#              print 'Got a KeyError with: backgroundSystDict['+syst+']['+background_name+']['+selectionNameBkgSyst+']'
#
#    if verbose:
#      print 'INFO: firstSyst=',math.sqrt(firstSyst)
#
#    # background-only special systs: "DYShape", "TTShape", "WShape"
#    specialSysts = ["DYShape"] if doEEJJ else ["WShape","TTShape"]
#    for syst in specialSysts:
#        if syst=='DYShape' and not 'DY' in background_name or syst=='TTShape' and not 'TT' in background_name or 'TTBarFromDATA' in background_name or syst=='WShape' and not 'W' in background_name:
#            continue
#        if verbose:
#          print 'INFO: background_name=',background_name
#          print 'INFO: babackgroundSystDict['+syst+'].keys()=',backgroundSystDict[syst].keys()
#        if background_name not in backgroundSystDict[syst].keys():
#          print 'WARNING: could not find',background_name,'in backgroundSystDict['+syst+']=',backgroundSystDict[syst].keys()
#          continue
#        if selectionName not in backgroundSystDict[syst][background_name].keys():
#            selectionNameBkgSyst = maxLQselectionBkg
#        else:
#            selectionNameBkgSyst = selectionName
#        try:
#          secondSyst = pow(backgroundSystDict[syst][background_name][selectionNameBkgSyst],2)
#          #print 'backgroundSystDict['+syst+']['+background_name+']['+selectionNameBkgSyst+']=',secondSyst
#        except KeyError:
#            print 'ERROR: Got a KeyError with: backgroundSystDict['+syst+']['+background_name+']['+selectionNameBkgSyst+']'
#
#    if verbose:
#      print 'INFO: secondSyst (TT/DYShape)=',math.sqrt(secondSyst)
#
#    # XXX WARNING: hardcoded background name (ick); some checking is done at least
#    if 'TTbar' in background_name:
#        thirdSyst = pow(ttBarNormDeltaXOverX,2)
#    elif doEEJJ and 'DY' in background_name:
#        thirdSyst = pow(zJetNormDeltaXOverX,2)
#    elif not doEEJJ and 'W' in background_name:
#        thirdSyst = pow(zJetNormDeltaXOverX,2)
#    elif 'QCD' in background_name:
#        thirdSyst = pow(qcdNormDeltaXOverX,2)
#
#    if verbose:
#      print 'INFO: thirdSyst (extra norm uncertainty)=',math.sqrt(thirdSyst)
#
#    # now get the total deltaX/X
#    totalSyst = math.sqrt(firstSyst+secondSyst+thirdSyst)
#    return totalSyst

def GetBackgroundSyst(background_name, selectionName):
    verbose = True
    #if selectionName=='preselection':
    #  verbose=True
    if verbose:
      print 'GetBackgroundSyst('+background_name+','+selectionName+')'
    firstSyst = 0
    secondSyst = 0
    thirdSyst = 0
    if not 'QCD' in background_name and not 'data' in background_name.lower():
      for syst in signalSystDict.keys():
          if selectionName not in backgroundSystDict[syst][background_name].keys():
              if 'LQ' in selectionName:
                selectionNameBkgSyst = maxLQselectionBkg
              else:
                selectionNameBkgSyst = minLQselectionBkg
              #print 'selectionName=',selectionName,'not found in',backgroundSystDict[syst][background_name].keys()
          else:
              selectionNameBkgSyst = selectionName
          try:
            firstSyst += pow(backgroundSystDict[syst][background_name][selectionNameBkgSyst],2) # deltaX/X
            if verbose:
                print 'add',syst,'for',background_name,'at selection',selectionNameBkgSyst,'to firstSyst=',backgroundSystDict[syst][background_name][selectionNameBkgSyst]
          except KeyError:
              print 'Got a KeyError with: backgroundSystDict['+syst+']['+background_name+']['+selectionNameBkgSyst+']'

    if verbose:
      print 'firstSyst=',math.sqrt(firstSyst)

    # background-only special systs: "DYShape", "TTShape", "WShape"
    specialSysts = ["DYShape",'DY_Norm','Diboson_shape'] if doEEJJ else ["WShape","TTShape",'W_Norm','W_btag_Norm','W_RMt_Norm','TT_Norm','TTbar_btag_Norm','Diboson_shape']
    for syst in specialSysts:
        if 'TTBarFromDATA' in background_name or 'DY' in syst and not 'DY' in background_name or 'TT' in syst and not 'TT' in background_name or 'W' in syst and not 'W' in background_name or 'Diboson' in syst and not 'Diboson' in background_name:
            continue
        if verbose:
            print 'consider systematic:',syst,'for background_name=',background_name
        if background_name not in backgroundSystDict[syst].keys():
          print 'WARNING: could not find',background_name,'in backgroundSystDict['+syst+']=',backgroundSystDict[syst].keys()
          continue
        if selectionName not in backgroundSystDict[syst][background_name].keys():
            selectionNameBkgSyst = maxLQselectionBkg
        else:
            selectionNameBkgSyst = selectionName
        try:
          secondSyst = pow(backgroundSystDict[syst][background_name][selectionNameBkgSyst],2)
          if verbose:
            print 'backgroundSystDict['+syst+']['+background_name+']['+selectionNameBkgSyst+']=',secondSyst
        except KeyError:
            print 'ERROR: Got a KeyError with: backgroundSystDict['+syst+']['+background_name+']['+selectionNameBkgSyst+']'

    if verbose:
      print 'secondSyst (TT/DYShape)=',math.sqrt(secondSyst)
        
    ## XXX WARNING: hardcoded background name (ick); some checking is done at least
    if doEEJJ and 'TTbar' in background_name:
        thirdSyst = pow(ttBarNormDeltaXOverX,2)
    #elif not doEEJJ and 'W' in background_name:
    #    thirdSyst = pow(zJetNormDeltaXOverX,2)
    if 'QCD' in background_name:
        thirdSyst = pow(qcdNormDeltaXOverX,2)

    if verbose:
      print 'thirdSyst (extra norm uncertainty)=',math.sqrt(thirdSyst)

    # now get the total deltaX/X
    totalSyst = math.sqrt(firstSyst+secondSyst+thirdSyst)
    return totalSyst




# set batch
r.gROOT.SetBatch()

####################################################################################################
# Configurables
####################################################################################################
#FIXME commandline the eejj/enujj switching
doEEJJ= False
doSystErr = True
doRatio = True
blind = False

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
  #File_preselection = os.environ["LQDATA"]+'/2016analysis/'+   'eejj_psk_jan26_gsfEtaCheck_finalSels/output_cutTable_lq_eejj/analysisClass_lq_eejj_plots.root'
  #datFile_preselection = os.environ["LQDATA"]+'/2016analysis/'+'eejj_psk_jan26_gsfEtaCheck_finalSels/output_cutTable_lq_eejj/analysisClass_lq_eejj_tables.dat'
  #File_QCD_preselection = os.environ["LQDATA"]+'/2016qcd/'+   'eejj_QCD_jan26_gsfEtaCheck_finalSels/output_cutTable_lq_eejj_QCD/analysisClass_lq_eejj_QCD_plots.root'
  #datFile_QCD_preselection = os.environ["LQDATA"]+'/2016qcd/'+'eejj_QCD_jan26_gsfEtaCheck_finalSels/output_cutTable_lq_eejj_QCD/analysisClass_lq_eejj_QCD_tables.dat'
  #File_ttbar = os.environ["LQDATA"]+'/2016ttbar/'+ 'feb2_newSkim_emujj_correctTrig_finalSelections/output_cutTable_lq_ttbar_emujj_correctTrig/analysisClass_lq_ttbarEst_plots.root'
  #
  #filePath = os.environ["LQDATA"] + '/2016analysis/eejj_psk_feb10_bugfix/output_cutTable_lq_eejj/'
  #qcdFilePath = os.environ["LQDATA"] + '/2016qcd/eejj_QCD_feb10_bugfix/output_cutTable_lq_eejj_QCD/'
  #ttbarFilePath = os.environ["LQDATA"] + '/2016ttbar/feb11_emujj_correctTrig/output_cutTable_lq_ttbar_emujj_correctTrig/'
  #
  #qcdFilePath = os.environ["LQDATA"] + '/2016qcd/eejj_QCD_feb10_bugfix/output_cutTable_lq_eejj_QCD/'
  #filePath = os.environ["LQDATA"] + '/2016analysis/eejj_psk_feb20_newSingTop/output_cutTable_lq_eejj/'
  #ttbarFilePath = os.environ["LQDATA"] + '/2016ttbar/mar1_emujj_RedoRTrig/output_cutTable_lq_ttbar_emujj_correctTrig/'
  #
  qcdFilePath = os.environ["LQDATA"] + '/2016qcd/eejj_QCD_mar16_fixMuons/output_cutTable_lq_eejj_QCD/'
  filePath = os.environ["LQDATA"] + '/2016analysis/eejj_psk_mar16_fixMuons/output_cutTable_lq_eejj/'
  ttbarFilePath = os.environ["LQDATA"] + '/2016ttbar/mar17_emujj_fixMuons/output_cutTable_lq_ttbar_emujj_correctTrig/'
  #
  bkgd_file = r.TFile.Open(filePath+'analysisClass_lq_eejj_plots.root')
  bkgd_dat_file = open(filePath+'analysisClass_lq_eejj_tables.dat')
  qcd_file = r.TFile.Open(qcdFilePath+'analysisClass_lq_eejj_QCD_plots.root')
  qcd_dat_file = open(qcdFilePath+'analysisClass_lq_eejj_QCD_tables.dat')
  ttbar_file = r.TFile.Open(ttbarFilePath+'analysisClass_lq_ttbarEst_plots.root')
  #
  systematicsNamesBackground = [ "Trigger", "Reco", "PU", "PDF", "Lumi", "JER", "JEC", "HEEP", "E_scale", "EER", "DYShape", 'DY_Norm', "Diboson_shape" ]
  syst_background_names = ['GJets', 'QCDFakes_DATA', 'TTBarFromDATA', 'DY', 'WJets', 'Diboson', 'Singletop']
  systematicsNamesSignal =  [ "Trigger", "Reco", "PU", "PDF", "Lumi", "JER", "JEC", "HEEP", "E_scale", "EER"]
  # allBkg, zjets, ttbar, qcd
  #FIXME must update by hand at the moment; should extract from dat files
  #yields = {650: [30.34,15.54,5.52,0.075], 1200: [2.6,1.73,0.21,0.0069]}
  #statUncerts = {650: [], 1200: []}
  # systs
  #zjetsSF = 0.9742
  #zjetsSFerr = 0.0076
  #zJetNormDeltaXOverX=zjetsSFerr/zjetsSF
  ttBarNormDeltaXOverX = 0.01
  qcdNormDeltaXOverX = 0.50
else:
  vars = varsENUJJ
  x_labels = x_labelsENUJJ
  x_bins = x_binsENUJJ
  #File_preselection     = os.environ["LQDATA"]+"/2016analysis/"+"enujj_psk_feb4_v237_MET100_PtEMET70/output_cutTable_lq_enujj_MT/analysisClass_lq_enujj_MT_plots.root"
  #datFile_preselection  = os.environ["LQDATA"]+"/2016analysis/"+"enujj_psk_feb4_v237_MET100_PtEMET70/output_cutTable_lq_enujj_MT/analysisClass_lq_enujj_MT_tables.dat"
  #File_QCD_preselection = os.environ["LQDATA"]+"/2016qcd/"+   "/enujj_newRsk237_feb4_gsfEtaCheck_MET100_PtEMET70/output_cutTable_lq_enujj_MT_QCD/analysisClass_lq_enujj_QCD_plots.root"
  #datFile_QCD_preselection = os.environ["LQDATA"]+"/2016qcd/"+"/enujj_newRsk237_feb4_gsfEtaCheck_MET100_PtEMET70/output_cutTable_lq_enujj_MT_QCD/analysisClass_lq_enujj_QCD_tables.dat"
  #
  #filePath = os.environ["LQDATA"] + '/2016analysis/enujj_psk_feb10_v237_bugfix/output_cutTable_lq_enujj_MT/'
  #qcdFilePath = os.environ["LQDATA"] + '/2016qcd/enujj_feb10_bugfix/output_cutTable_lq_enujj_MT_QCD/'
  #
  #filePath = os.environ["LQDATA"] + '/2016analysis/enujj_psk_feb20_dPhiEleMet0p8_newSingTop/output_cutTable_lq_enujj_MT/'
  #qcdFilePath = os.environ["LQDATA"] + '/2016qcd/enujj_feb14_dPhiEleMET0p8/output_cutTable_lq_enujj_MT_QCD/'
  #
  filePath = os.environ["LQDATA"] + '/2016analysis/enujj_psk_mar16_fixMuons/output_cutTable_lq_enujj_MT/'
  qcdFilePath = os.environ["LQDATA"] + '/2016qcd/enujj_mar16_fixMuons/output_cutTable_lq_enujj_MT_QCD/'
  #
  ttbarFilePath = filePath
  #
  bkgd_file = r.TFile(filePath+'analysisClass_lq_enujj_MT_plots.root')
  bkgd_dat_file = open(filePath+'analysisClass_lq_enujj_MT_tables.dat')
  qcd_file  = r.TFile(qcdFilePath+'analysisClass_lq_enujj_QCD_plots.root')
  qcd_dat_file  = open(qcdFilePath+'analysisClass_lq_enujj_QCD_tables.dat')
  #
  systematicsNamesBackground = [ "Trigger", "Reco", "PU", "PDF", "Lumi", "JER", "JEC", "HEEP", "E_scale", "EER", "MET", "WShape", 'W_Norm', 'W_btag_Norm', 'W_RMt_Norm', "TTShape", 'TT_Norm', 'TTbar_btag_Norm', "Diboson_shape" ]
  syst_background_names = ['GJets', 'QCDFakes_DATA', 'TTbar', 'DY', 'WJets', 'Diboson', 'Singletop']
  systematicsNamesSignal =  [ "Trigger", "Reco", "PU", "PDF", "Lumi", "JER", "JEC", "HEEP", "E_scale", "EER", "MET" ]
  # allBkg, zjets, ttbar, qcd
  #FIXME must update by hand at the moment; should extract from dat files
  #yields = {650: [74.37,32.23,13.55,4.88], 1200: [9.13,4.93,0.53,0.37]}
  #statUncerts = {650: [], 1200: [5.19]}
  # systs
  # W scale factor
  #zjetsSF = 0.8782
  #zjetsSFerr = 0.0067
  #zJetNormDeltaXOverX=zjetsSFerr/zjetsSF
  #ttBarNormDeltaXOverX = 0.01
  qcdNormDeltaXOverX = 0.25
if doSystErr:
  systematics_filepaths = {}
  for systName in systematicsNamesBackground:
    if doEEJJ:
      systematics_filepaths[systName] = '/afs/cern.ch/user/m/mbhat/work/public/Systematics_4eejj_DibosonAMCATNLO_18_02_2018/'
    else:
      systematics_filepaths[systName] = '/afs/cern.ch/user/m/mbhat/work/public/Systematics_4enujj_DibosonamcATnlo_18_02_2018/'
  backgroundSystDict = FillSystDicts(systematicsNamesBackground,syst_background_names,systematics_filepaths)
  signalSystDict     = FillSystDicts(systematicsNamesSignal,syst_background_names,systematics_filepaths,False)


lumiEnergyString = "35.9 fb^{-1} (13 TeV)"


print 'Using tables:'
print '\t Data/MC:',bkgd_file.GetName()
print '\t QCD(data):',qcd_file.GetName()
print 'Using systematics files:',systematics_filepaths


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
#r.gStyle.SetPadTickX(0)
#r.gStyle.SetPadTickY(0)


for i_mass, mass in enumerate(masses):

  if doSystErr:
    #systs = [GetBackgroundSyst(systType,'LQ'+str(mass)) for systType in syst_background_names]
    #print 'syst_background_names=',syst_background_names
    #print 'systs=',systs
    # need to combine some systs and put in order
    systs = [GetBackgroundSyst('QCDFakes_DATA','LQ'+str(mass))]
    gjetsSyst = GetBackgroundSyst('GJets','LQ'+str(mass))
    dibosonSyst = GetBackgroundSyst('Diboson','LQ'+str(mass))
    singleTopSyst = GetBackgroundSyst('Singletop','LQ'+str(mass))
    systs.append(math.sqrt(pow(gjetsSyst,2)+pow(dibosonSyst,2)+pow(singleTopSyst,2)))
    if doEEJJ:
        systs.append(GetBackgroundSyst('TTBarFromDATA','LQ'+str(mass)))
        systs.append(GetBackgroundSyst('DY','LQ'+str(mass)))
    else:
        systs.append(GetBackgroundSyst('TTbar','LQ'+str(mass)))
        systs.append(GetBackgroundSyst('WJets','LQ'+str(mass)))

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
    ZeroNegativeBins([qcd_hist,other_hist,ttbar_hist,zjets_hist])
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
    
    canv_name = var + "_LQ" + str(mass) + "_canv"
    pad_name  = var + "_LQ" + str(mass) + "_pad"
    save_name = var + "_LQ" + str(mass) 
    #save_name = save_name.replace("PAS", "preselection")
    if doEEJJ:
      save_name = save_name + "_eejj.pdf"
    else:
      save_name = save_name + "_enujj.pdf"
    save_name_png = save_name.replace('.pdf','.png')
  
    ## WORKS
    #canvas = r.TCanvas(canv_name,canv_name,800,550)
    #canvas.cd()
    #pad1   = r.TPad( pad_name, pad_name , 0.0, 0.0, 1.0, 1.0 )
    #canvas.SetLogy()
    #stack.Draw("HIST")
    ## WORKS
  
    canvas = r.TCanvas(canv_name,canv_name,800,600)
    canvas.cd()
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
    stack.Draw('hist')
    stack.GetYaxis().SetRangeUser(1e-1,stack.GetMaximum()*1.1)
    stack.GetXaxis().SetTitle( x_labels [i_var] )
    #canvas.SetLogy()
    pad1.SetLogy()
    pad1.Draw()
  
    sig_hist.Draw("HIST SAME")
    # convert to Poisson error bars
    # check if we need to stop error bars before the end
    if not blind:
      lastPopBin = getLastPopulatedBin([zjets_hist,ttbar_hist,other_hist,qcd_hist,data_hist,sig_hist])
      #print 'last pop bin center = ', data_hist.GetBinCenter(lastPopBin)
      g = poissonErrGraph(data_hist,lastPopBin)
      #g.Draw("ZPSAME")
      g.Draw("ZP0SAME")
  
    if doSystErr:
      verbose=False
      bkgUncHisto = copy.deepcopy(stack.GetStack().Last())
      bkgUncHisto.Reset()
      bkgUncHisto.SetNameTitle('bkgUncHisto','bkgUncHisto')
      for idx,hist in enumerate(stkSystErrHistos):
          syst = systs[idx]
          if verbose:
            print '[',hist.GetName(),']: look at systs['+str(idx)+']'
          for ibin in xrange(0,hist.GetNbinsX()+2):
              hist.SetBinError(ibin,syst*hist.GetBinContent(ibin))
              if verbose:
                print '[',hist.GetName(),'] set bin with center',hist.GetBinCenter(ibin),'error to:',syst*hist.GetBinContent(ibin)
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
      if verbose:
        for ibin in xrange(0,bkgUncHisto.GetNbinsX()+2):
            print '[',bkgUncHisto.GetName(),'] bin with center',bkgUncHisto.GetBinCenter(ibin),'error is:',bkgUncHisto.GetBinError(ibin)

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
  
        pad2.cd()
        # fPads2.SetLogy()
        pad2.SetGridy()
        
        h_ratio1.Divide(h_bkgTot1)

        oldRatioHist = copy.deepcopy(h_ratio1)
        h_ratio1.Delete()
        del h_ratio1
        #h_ratio1.Reset()
        h_ratio1 = TH1F('ratio','ratio',oldRatioHist.GetNbinsX(),oldRatioHist.GetXaxis().GetXbins().GetArray())
        for ibin in range(0,oldRatioHist.GetNbinsX()+1):
            oldBinContent = oldRatioHist.GetBinContent(ibin)
            if oldBinContent > 0:
                print '1) set bin content for bin:',ibin,'to:',oldBinContent
                h_ratio1.SetBinContent(ibin,oldBinContent)
                h_ratio1.SetBinError(ibin,oldRatioHist.GetBinError(ibin))
            #elif h_bkgTot1.GetBinContent(ibin) > 0:
            #    print '2) set bin content for bin:',ibin,'to:',oldBinContent
            #    h_ratio1.SetBinContent(ibin,oldBinContent)
            #    h_ratio1.SetBinError(ibin,oldRatioHist.GetBinError(ibin))
            else:
                print '3) set bin content for bin:',ibin,'to -1'
                h_ratio1.SetBinContent(ibin,-1)
                h_ratio1.SetBinError(ibin,-1)

        #h_ratio1.GetXaxis().SetTitle("")
        #h_ratio1.GetXaxis().SetTitleSize(0.06)
        #h_ratio1.GetXaxis().SetLabelSize(0.1)
        #h_ratio1.GetYaxis().SetRangeUser(0.,2)
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
  
        #h_ratio1.Draw("e0")
        h_ratio1.Draw('p')

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
            #bgRatioErrs.GetXaxis().SetTitle('')
            bgRatioErrs.GetXaxis().SetTitle( x_labels [i_var] )
            bgRatioErrs.GetXaxis().SetTitleSize(0.15)
            bgRatioErrs.GetXaxis().SetLabelSize(0.1)
            bgRatioErrs.GetYaxis().SetTitle("Data/MC")
            bgRatioErrs.GetYaxis().SetLabelSize(0.1)
            bgRatioErrs.GetYaxis().SetTitleSize(0.13)
            bgRatioErrs.GetYaxis().SetTitleOffset(0.3)
            bgRatioErrs.SetMarkerStyle ( 1 )
            bgRatioErrs.Draw('E2')
            #h_ratio1.Draw("e0psame")
            h_ratio1.Draw("e0same")
            bgRatioErrs.GetYaxis().SetRangeUser(0.,2)

            ## need to make hist with "1" in all bins
            #bgRatioErrs = h_ratio1.Clone()
            #bgRatioErrs.Reset()
            #bgRatioErrs.SetName('bgRatioErrs')
            #for binn in range(0,bgRatioErrs.GetNbinsX()):
            #    bgRatioErrs.SetBinContent(binn,1.0)
            #bgRatioErrsGraph = GetErrorsGraph([bgRatioErrs],backgroundSyst)
            #bgRatioErrsGraph.Draw('E2 same')

        h_ratio1.GetYaxis().SetRangeUser(0.,2)

        #lineAtOne = TLine(h_ratio.GetXaxis().GetXmin(),1,h_ratio.GetXaxis().GetXmax(),1)
        #lineAtOne.SetLineColor(2)
        #lineAtOne.Draw()
        pad1.cd()
    

    #leg = r.TLegend(0.43,0.53,0.89,0.89,"","brNDC") #used for all lq2 data plots
    #leg = r.TLegend(0.43,0.58,0.67,0.89,"","brNDC")
    leg = r.TLegend(0.52,0.53,0.74,0.88,"","brNDC")
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
      leg.AddEntry(bkgUncHisto, 'Uncertainty band','f')
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
    canvas.SaveAs(save_name_png)


#print 'closing files...',
#bkgd_file.Close()
#qcd_file.Close()
#print 'Done!'

