#!/usr/bin/env python

from plot_common import *
import tdrstyle
import math
from ROOT import kOrange, kGray, kBlue, kRed, kCyan, kGreen, TH1F, TGraphAsymmErrors, Double, TLine


def GetBackgroundSyst(background_name, selectionName):
    verbose = False
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
doEEJJ= True
doPrelim = False
doSystErr = True
doRatio = True
blind = False

masses = [ 650, 1200 ]

mass_colors = [ 28, 38 ]

varsEEJJ     = [ 
    "sT_eejj",
    "Mej_selected_min",
    #"Meejj"
] 

x_labelsEEJJ = [ 
    "S_{T} [GeV]",
    "M_{ej}^{min} [GeV]",
    #"M_{eejj} [GeV]"
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
    "S_{T} [GeV]",
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
r.gStyle.SetPadRightMargin(0.04)


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
    setStackHistosStyle([zjets_hist,ttbar_hist,other_hist,qcd_hist,sig_hist,data_hist])
  
    if var=='Mej_selected_min' or var=='Mej':
        nDivs = 507
        xMin = 400
        xMax = 1980
    elif var=='ST':
        nDivs = 507
        xMin = 1000
        xMax = 3000
    else:
        nDivs = 507
        xMin = 800
        xMax = 3000


    stack = r.THStack ("stack", "stack")
    stack.Add ( qcd_hist   )
    stack.Add ( other_hist )
    stack.Add ( ttbar_hist )
    stack.Add ( zjets_hist )
    stack.Draw()
    if doEEJJ:
      stack.SetMaximum(5e3)
      if mass < 1000 and var=='sT_eejj':
          stack.SetMaximum(5e6)
      elif mass < 1000 and var=='Mej_selected_min':
          stack.SetMaximum(1e5)
      elif mass > 1000 and var=='Mej_selected_min':
          stack.SetMaximum(1e4)
    else:
        if var=='Mej' and mass < 1000:
            stack.SetMaximum(1e4);
        elif var=='Mej' and mass > 1000:
            stack.SetMaximum(1e3);
        elif var=='ST' and mass < 1000:
            stack.SetMaximum(1e5);
        elif var=='ST' and mass > 1000:
            stack.SetMaximum(1e4);

    stack.SetMinimum(1e-1)
    bkgTotalHist = stack.GetStack().Last() # sum of all TH1 in stack

    stkSystErrHistos = [ copy.deepcopy(h) for h in [qcd_hist,other_hist,ttbar_hist,zjets_hist] ]
    stkSystStatErrHistos = [ copy.deepcopy(h) for h in [qcd_hist,other_hist,ttbar_hist,zjets_hist] ]

    setStackYAxisStyle(stack)
    
    if not doRatio:
        setStackNoRatioXAxisStyle(stack)
    else:
        setStackWithRatioXAxisStyle(stack)

    stack.GetXaxis().SetTitle( x_labels [i_var] )
    stack.GetXaxis().SetRangeUser(xMin,xMax)

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
  
    canvas = r.TCanvas(canv_name,canv_name,800,600)
    canvas.cd()
    if not doRatio:
        pad1  = r.TPad( pad_name+"1", pad_name+"1" , 0.0, 0.0, 1.0, 1.0 )
        pad1.Draw()
    else:
        pad1 = r.TPad(pad_name+"1", pad_name+"1", 0.00, 0.3, 0.99, 0.99)
        pad2 = r.TPad(pad_name+"2", pad_name+"2", 0.00, 0.00, 0.99, 0.3)
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
    #canvas.SetLogy()
    pad1.Draw()
    r.gPad.Update()

    sig_hist.Draw("HIST SAME")
  
    if doSystErr:
      verbose=False
      bkgUncHisto = copy.deepcopy(stack.GetStack().Last())
      bkgUncHisto.Reset()
      bkgUncHisto.SetNameTitle('bkgUncHisto','bkgUncHisto')
      h_bkgUnc1 = copy.deepcopy(bkgUncHisto)
      for idx,hist in enumerate(stkSystErrHistos):
          syst = systs[idx]
          if verbose:
            print '[',hist.GetName(),']: look at systs['+str(idx)+']'
          for ibin in xrange(0,hist.GetNbinsX()+2):
              #hist.SetBinError(ibin,syst*hist.GetBinContent(ibin))
              hist.SetBinError(ibin,math.sqrt( (syst*hist.GetBinContent(ibin))**2+hist.GetBinError(ibin)**2 ))
              if verbose:
                print '[',hist.GetName(),'] set bin with center',hist.GetBinCenter(ibin),'error to:',syst*hist.GetBinContent(ibin)
          bkgUncHisto.Add(hist)
      ##histoAll = copy.deepcopy(bkgTotalHist)
      #histoAll = thStack.GetStack().Last()
      #bkgUncHisto = copy.deepcopy(histoAll)
      #for bin in range(0,histoAll.GetNbinsX()):
      #    bkgUncHisto.SetBinError(bin+1,self.bkgSyst*histoAll.GetBinContent(bin+1))
      setBkgUncHistStyle(bkgUncHisto)
      bkgUncHisto.Draw("E2same")
      if verbose:
        for ibin in xrange(0,bkgUncHisto.GetNbinsX()+2):
            print '[',bkgUncHisto.GetName(),'] bin with center',bkgUncHisto.GetBinCenter(ibin),'error is:',bkgUncHisto.GetBinError(ibin)

    # convert to Poisson error bars
    # check if we need to stop error bars before the end
    if not blind:
      lastPopBin = getLastPopulatedBin([zjets_hist,ttbar_hist,other_hist,qcd_hist,data_hist,sig_hist])
      #print 'last pop bin center = ', data_hist.GetBinCenter(lastPopBin)
      g = poissonErrGraph(data_hist,lastPopBin)
      #g.Draw("ZPSAME")
      g.Draw("ZP0SAME")

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

        setRatio1NoBGErrStyle(h_ratio1, x_labels[i_var])
        pad2.SetBottomMargin(0.6)
    
        setRatio1MarkerStyle(h_ratio1)
  
        #h_ratio1.Draw("e0")
        # used for th1f
        #h_ratio1.Draw('p')
        h_ratio1.Draw('z0')

        if doSystErr:
            #verbose=True
            # need combined background hists with errors as sqrt[syst^2+stat^2]
            for idx,hist in enumerate(stkSystStatErrHistos):
                syst = systs[idx]
                if verbose:
                  print '[',hist.GetName(),']: look at systs['+str(idx)+']'
                for ibin in xrange(0,hist.GetNbinsX()+2):
                    if verbose:
                        print '[',hist.GetName(),'] set bin with center',hist.GetBinCenter(ibin),'content:',hist.GetBinContent(ibin),'set error to:',syst*hist.GetBinError(ibin),'[syst] (+)',hist.GetBinError(ibin),'[stat]'
                    hist.SetBinError(ibin,math.sqrt( (syst*hist.GetBinContent(ibin))**2+hist.GetBinError(ibin)**2 ))
                h_bkgUnc1.Add(hist)
            if verbose:
              for ibin in xrange(0,h_bkgUnc1.GetNbinsX()+2):
                  print '[h_bkgUnc1 with name',h_bkgUnc1.GetName(),'] bin with center',h_bkgUnc1.GetBinCenter(ibin),'bin content is:',h_bkgUnc1.GetBinContent(ibin),'error is:',h_bkgUnc1.GetBinError(ibin)

            # set bin error to the relative error on the background
            for ibin in xrange(0,h_bkgUnc1.GetNbinsX()+2):
                #print '[h_bkgUnc1 with name',h_bkgUnc1.GetName(),'] bin with center',h_bkgUnc1.GetBinCenter(ibin),'bin content is:',h_bkgUnc1.GetBinContent(ibin),'error is:',h_bkgUnc1.GetBinError(ibin)
                if h_bkgUnc1.GetBinContent(ibin) != 0:
                    if verbose:
                        print '[h_bkgUnc1 with name',h_bkgUnc1.GetName(),'] bin with center',h_bkgUnc1.GetBinCenter(ibin),'bin content is:',h_bkgUnc1.GetBinContent(ibin),'error is:',h_bkgUnc1.GetBinError(ibin),'relative error=',h_bkgUnc1.GetBinError(ibin)/h_bkgUnc1.GetBinContent(ibin)
                    h_bkgUnc1.SetBinError(ibin,h_bkgUnc1.GetBinError(ibin)/h_bkgUnc1.GetBinContent(ibin))
                h_bkgUnc1.SetBinContent(ibin,1.0)
            bgRatioErrs = h_bkgUnc1

            setBGRatioErrStyle(bgRatioErrs, x_labels [i_var])
             
            bgRatioErrs.Draw('E2')
            #bgRatioErrs.Draw('3')
            #h_ratio1.Draw("e0psame")
            # below is for th1f
            #h_ratio1.Draw("e0same")
            h_ratio1.Draw("pz0same")
            bgRatioErrs.GetYaxis().SetRangeUser(0.,2)
            bgRatioErrs.GetXaxis().SetRangeUser(xMin,xMax)


        h_ratio1.GetYaxis().SetRangeUser(0.,2)
        h_ratio1.GetXaxis().SetRangeUser(xMin,xMax)

        # shameless copy of SetRangeUser code
        ifirst = h_ratio1.GetXaxis().FindFixBin(xMin);
        ilast = h_ratio1.GetXaxis().FindFixBin(xMax);
        if h_ratio1.GetXaxis().GetBinUpEdge(ifirst) <= xMin: ifirst += 1
        if h_ratio1.GetXaxis().GetBinLowEdge(ilast) >= xMax: ilast -= 1
        lineAtOne = TLine(pad1.GetUxmin(),1,pad1.GetUxmax(),1)
        lineAtOne.SetLineColor(1)
        lineAtOne.Draw()
        r.gPad.Update()
        pad1.cd()
    
    # redraw stack and data on top
    stack.Draw('histsame')
    sig_hist.Draw("HIST SAME")
    g.Draw("pz0SAME")

    #leg = r.TLegend(0.43,0.53,0.89,0.89,"","brNDC") #used for all lq2 data plots
    #leg = r.TLegend(0.43,0.58,0.67,0.89,"","brNDC")
    leg = r.TLegend(0.49,0.45,0.75,0.88,"","brNDC")
    setLegendStyle(leg)
    if not blind:
      leg.AddEntry(data_hist ,"Data","lpe")
    if doEEJJ:
      leg.AddEntry(zjets_hist,"Z/#gamma* + jets","f")
    else:
      leg.AddEntry(zjets_hist,"W + jets","f")
    leg.AddEntry(ttbar_hist,"t#bar{t}","f")
    leg.AddEntry(other_hist,"Other background","f")
    leg.AddEntry(qcd_hist  ,"Multijet","f")
    if doSystErr:
      leg.AddEntry(bkgUncHisto, 'Stat+syst uncertainty','f')
    if doEEJJ:
      beta = 1.0
    else:
      beta = 0.5
    leg.AddEntry(sig_hist  ,"LQ, M = "+str(mass)+" GeV, #beta = "+str(beta),"l")
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
    drawLumiEnergyAndCMSStrings(l1,l2)

    l3 = r.TLatex()
    if doPrelim:
        drawPrelim(l3)

    r.gPad.Update()


    if not r.gROOT.IsBatch():
        ## wait for input to keep the GUI (which lives on a ROOT event dispatcher) alive
        if __name__ == '__main__':
           rep = ''
           while not rep in [ 'c', 'C' ]:
              rep = raw_input( 'enter "c" to continue: ' )
              if 1 < len(rep):
                 rep = rep[0]
    # FOR TESTING
    #break

    print 'saving the canvas'
    canvas.SaveAs(save_name)
    canvas.SaveAs(save_name_png)


#print 'closing files...',
#bkgd_file.Close()
#qcd_file.Close()
#print 'Done!'

