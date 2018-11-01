#!/usr/bin/env python

from plot_common import *
import tdrstyle
import math
from ROOT import kOrange, kGray, kBlue, kRed, kCyan, kGreen, TH1F, TGraphAsymmErrors, Double, TLine
from optparse import OptionParser


def GetBackgroundSyst(systType, isEEJJ=True):
    verbose = False
    # /afs/cern.ch/user/m/mbhat/work/public/Systematics_4Preselection_02_11_2017/eejj_Preselection_sys.dat
    # /afs/cern.ch/user/m/mbhat/work/public/Systematics_4Preselection_02_11_2017/eejj_Preselection_sys_05_03_2018.dat
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
    # /afs/cern.ch/user/m/mbhat/work/public/Systematics_4Preselection_02_11_2017/enujj_Preselection_sys_05_03_2018.dat
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


####################################################################################################
# Configurables
####################################################################################################
#---Option Parser
usage = "usage: %prog [options] \nExample: \n./plot_preselection.py --eejj=True --prelim=True --systErr=True --ratio=True --batch=False"

parser = OptionParser(usage=usage)

parser.add_option("-e", "--eejj", dest="doEEJJ",
                  help="do EEJJ channel plots",
                  metavar="EEJJ",default='True')

parser.add_option("-p", "--prelim", dest="doPrelim",
                  help="do prelim style plots",
                  metavar="PRELIMI",default='False')

parser.add_option("-s", "--systErr", dest="doSystErr",
                  help="add syst. err. to plots",
                  metavar="SYSTERR",default='True')

parser.add_option("-r", "--ratio", dest="doRatio",
                  help="add data/bkg. ratio to plots",
                  metavar="RATIO",default='True')

parser.add_option("-b", "--batch", dest="doBatch",
                  help="use ROOT batch mode",
                  metavar="BATCH",default='True')

(options, args) = parser.parse_args()
doEEJJ = StrToBool(options.doEEJJ)
doPrelim = StrToBool(options.doPrelim)
doSystErr = StrToBool(options.doSystErr)
doRatio = StrToBool(options.doRatio)
doBatch = StrToBool(options.doBatch)

print 'Doing:',
if doEEJJ:
    print 'EEJJ',
else:
    print 'ENuJJ',
if doPrelim:
    print 'prelim.',
if not doSystErr:
    print 'without syst. err.',
if not doRatio:
    print 'without data/bkg ratio',
if doBatch:
    print '\nUsing ROOT batch mode',
else:
    print '\nNot using ROOT batch mode'
print

# set batch
if doBatch:
    r.gROOT.SetBatch()

mass1 = 650
mass2 = 1200

mass_colors = [ 28, 38 ]

varsEEJJ     = [ 
#    "Pt1stEle_PAS",
#    "Pt2ndEle_PAS",
#    "Pt1stJet_PAS",
#    "Pt2ndJet_PAS",
    "sT_PAS",
    "Mej_selected_min_PAS",
    "Mee_PAS"
] 

x_labelsEEJJ = [ 
#    "p_{T} (e_{1}) [GeV]",
#    "p_{T} (e_{2}) [GeV]",
#    "p_{T} (jet_{1}) [GeV]",
#    "p_{T} (jet_{2}) [GeV]",
    "#it{S}_{T} [GeV]",
    "#it{m}_{ej}^{min} [GeV]",
    "#it{m}_{ee} [GeV]"
]

x_binsEEJJ = [ 
#    [i*20 for i in range(0,51)],
#    [i*20 for i in range(0,51)],
#    [i*20 for i in range(0,51)],
#    [i*20 for i in range(0,51)],
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
    "#it{S}_{T} [GeV]",
    "#it{m}_{ej} [GeV]",
    "#it{m}_{T} [GeV]",
    "#it{p}_{T}^{miss} [GeV]"
]

x_binsENUJJ = [ 
    [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980],
    #[0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980]
    # 25  30  35  40  45    50   55  60   65   70    75   80   85   90   95   100    105   110   115   120   125   130   135   140
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1100, 1205, 1310, 1430, 1550, 1680, 1820, 1980]
    # 25  30  35  40  45    50   55  60   65   70    75   80   85   90   95   100   100   105   110   120   120   130   140   160
]

systTypesEEJJ  = ['qcd', 'mc', 'ttbarfromdata', 'zjets']
systTypesENUJJ = ['qcd', 'mc', 'ttbar', 'wjets']

if doEEJJ:
  vars = varsEEJJ
  x_labels = x_labelsEEJJ
  x_bins = x_binsEEJJ
  systTypes = systTypesEEJJ
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
  #filePath = os.environ["LQDATA"] + '/2016analysis/enujj_psk_feb20_dPhiEleMet0p8_newSingTop/output_cutTable_lq_enujj_MT/'
  #qcdFilePath = os.environ["LQDATA"] + '/2016qcd/enujj_feb14_dPhiEleMET0p8/output_cutTable_lq_enujj_MT_QCD/'
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
else:
  vars = varsENUJJ
  x_labels = x_labelsENUJJ
  x_bins = x_binsENUJJ
  systTypes = systTypesENUJJ
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
    ZeroNegativeBins([qcd_hist,other_hist,ttbar_hist,zjets_hist])
    #zjets_hist.Rebin (2)
    #ttbar_hist.Rebin (2)
    #other_hist.Rebin (2)
    #qcd_hist  .Rebin (2)
    #data_hist .Rebin (2)
    #sig1_hist .Rebin (2)
    #sig2_hist .Rebin (2)
    setStackHistosStyle([zjets_hist,ttbar_hist,other_hist,qcd_hist,sig1_hist,sig2_hist,data_hist])

    stack = r.THStack ("stack", "stack")
    stack.Add ( qcd_hist   )
    stack.Add ( other_hist )
    stack.Add ( ttbar_hist )
    stack.Add ( zjets_hist )
    stack.Draw()
    stack.SetMaximum(5e7)
    if var=="MET_PAS":
        stack.SetMaximum(5e6)
    stack.SetMinimum(1e-1)
    bkgTotalHist = stack.GetStack().Last() # sum of all TH1 in stack

    stkSystErrHistos = [ copy.deepcopy(h) for h in [qcd_hist,other_hist,ttbar_hist,zjets_hist] ]
    stkSystStatErrHistos = [ copy.deepcopy(h) for h in [qcd_hist,other_hist,ttbar_hist,zjets_hist] ]

    setStackYAxisStyle(stack)
    
    if not doRatio:
        setStackNoRatioXAxisStyle(stack)
    else:
        setStackWithRatioXAxisStyle(stack)

    ## reduce x-axis labels for Mej plot
    #if 'Mej' in var:
    #  stack.GetXaxis().SetNdivisions(507)
    #stack.GetXaxis().SetNdivisions(515)
    
    canv_name = var + "_canv"
    pad_name  = var + "_pad"
    save_name = var 
    #save_name = save_name.replace("PAS", "preselection")
    if doEEJJ:
      save_name = save_name + "_eejj.pdf"
    else:
      save_name = save_name + "_enujj.pdf"

    save_namePNG = save_name.replace('.pdf','.png')

    canvas = r.TCanvas(canv_name,canv_name,800,600)
    canvas.cd()
    canvas.SetLogy()
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
    pad1.Draw()

    sig1_hist.Draw("HIST SAME")
    sig2_hist.Draw("HIST SAME")
    if doSystErr:
      bkgUncHisto = copy.deepcopy(stack.GetStack().Last())
      bkgUncHisto.Reset()
      bkgUncHisto.SetNameTitle('bkgUncHisto','bkgUncHisto')
      h_bkgUnc1 = copy.deepcopy(bkgUncHisto)
      for idx,hist in enumerate(stkSystErrHistos):
          syst = systs[idx]
          for ibin in xrange(0,hist.GetNbinsX()+2):
              #hist.SetBinError(ibin,syst*hist.GetBinContent(ibin))
              hist.SetBinError(ibin,math.sqrt( (syst*hist.GetBinContent(ibin))**2+hist.GetBinError(ibin)**2 ))
              #print '[',hist.GetName(),'] set bin',ibin,'error to:',syst*hist.GetBinContent(ibin)
          bkgUncHisto.Add(hist)
      ##histoAll = copy.deepcopy(bkgTotalHist)
      #histoAll = thStack.GetStack().Last()
      #bkgUncHisto = copy.deepcopy(histoAll)
      #for bin in range(0,histoAll.GetNbinsX()):
      #    bkgUncHisto.SetBinError(bin+1,self.bkgSyst*histoAll.GetBinContent(bin+1))
      setBkgUncHistStyle(bkgUncHisto)
      bkgUncHisto.Draw("E2same")
      #for ibin in xrange(0,bkgUncHisto.GetNbinsX()+2):
      #    print '[',bkgUncHisto.GetName(),'] bin',ibin,'error is:',bkgUncHisto.GetBinError(ibin)
      
    # convert to Poisson error bars
    # check if we need to stop error bars before the end
    lastPopBin = getLastPopulatedBin([zjets_hist,ttbar_hist,other_hist,qcd_hist,data_hist,sig1_hist,sig2_hist])
    #print 'last pop bin center = ', data_hist.GetBinCenter(lastPopBin)
    g = poissonErrGraph(data_hist,lastPopBin)
    #g.Draw("ZPSAME")
    g.Draw("ZP0SAME")


    #-- 2nd pad (ratio)
    if doRatio:
        pad2.cd()
        h_bkgTot = copy.deepcopy(bkgTotalHist)
        h_ratio = copy.deepcopy(data_hist)
        h_nsigma = copy.deepcopy(data_hist)
        dataCopy = copy.deepcopy(data_hist)
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
        #h_ratio1.Divide(h_bkgTot1)
        h_ratio1 = TGraphAsymmErrors()
        #print 'doing h_ratio1.Divide()'
        #print 'Nbins dataCopy=',dataCopy.GetNbinsX()
        #print 'Nbins h_bkgTot1=',h_bkgTot1.GetNbinsX()
        h_ratio1.Divide(dataCopy,h_bkgTot1,'poiscp')
        #print '2ndlast bin of data plot has:',dataCopy.GetBinContent(dataCopy.GetNbinsX()-1),'entries and error=',dataCopy.GetBinError(dataCopy.GetNbinsX()-1)
        #print 'last bin of data plot has:',dataCopy.GetBinContent(dataCopy.GetNbinsX()),'entries and error=',dataCopy.GetBinError(dataCopy.GetNbinsX())
        #print '2ndlast bin of bkg plot has:',h_bkgTot1.GetBinContent(h_bkgTot1.GetNbinsX()-1),'entries and error=',h_bkgTot1.GetBinError(h_bkgTot1.GetNbinsX()-1)
        #print '2ndlast bin of zjets plot has:',zjets_hist.GetBinContent(zjets_hist.GetNbinsX()-1),'entries and error=',zjets_hist.GetBinError(zjets_hist.GetNbinsX()-1)
        #print '2ndlast bin of ttbar plot has:',ttbar_hist.GetBinContent(ttbar_hist.GetNbinsX()-1),'entries and error=',ttbar_hist.GetBinError(ttbar_hist.GetNbinsX()-1)
        #print '2ndlast bin of other plot has:',other_hist.GetBinContent(other_hist.GetNbinsX()-1),'entries and error=',other_hist.GetBinError(other_hist.GetNbinsX()-1)
        #print '2ndlast bin of qcd plot has:',qcd_hist.GetBinContent(qcd_hist.GetNbinsX()-1),'entries and error=',qcd_hist.GetBinError(qcd_hist.GetNbinsX()-1)
        #print 'last bin of bkg plot has:',h_bkgTot1.GetBinContent(h_bkgTot1.GetNbinsX()),'entries and error=',h_bkgTot1.GetBinError(h_bkgTot1.GetNbinsX())
        #print '2ndlast bin of bkg plot center:',h_bkgTot1.GetBinCenter(h_bkgTot1.GetNbinsX()-1)
        #print 'last bin of bkg plot center:',h_bkgTot1.GetBinCenter(h_bkgTot1.GetNbinsX())
        ##print '2ndlast bin of ratio plot has:',h_ratio1.GetBinContent(h_ratio1.GetNbinsX()-1),'entries and error=',h_ratio1.GetBinError(h_ratio1.GetNbinsX()-1)
        ##print 'last bin of ratio plot has:',h_ratio1.GetBinContent(h_ratio1.GetNbinsX()),'entries and error=',h_ratio1.GetBinError(h_ratio1.GetNbinsX())

        #h_ratio1.GetXaxis().SetTitle("")
        #h_ratio1.GetXaxis().SetTitleSize(0.06)
        #h_ratio1.GetXaxis().SetLabelSize(0.1)
        h_ratio1.GetYaxis().SetRangeUser(0.,2)
        #h_ratio1.GetYaxis().SetNdivisions(505)

        #h_ratio1.GetYaxis().SetTitle("Data/MC")
        #h_ratio1.GetYaxis().SetLabelSize(0.1)
        #h_ratio1.GetYaxis().SetTitleSize(0.13)
        #h_ratio1.GetYaxis().SetTitleOffset(0.3)
        #h_ratio1.GetXaxis().CenterTitle()
        #h_ratio1.GetXaxis().CenterTitle(1)
        #pad2.SetBottomMargin(0.37)
        pad2.SetBottomMargin(0.55)
        pad2.SetTopMargin(0.075)
    
        setRatio1MarkerStyle(h_ratio1)

        # make bins with zero data have no marker ("empty" them)
        #h_ratio2 = copy.deepcopy(h_ratio1)
        #h_ratio2.Reset()
        #for binn in range(0,h_ratio1.GetNbinsX()):
        #    #if h_ratio1.GetBinContent(binn)<1e-1:
        #    #    h_ratio1.SetBinContent(binn,0.0)
        #    #    h_ratio1.SetBinError(binn,0.0)
        #    #    print 'bin content was:',h_ratio1.GetBinContent(binn),'for bin:',binn,'in plot',h_ratio1.GetName(),'set bin content/error to zero'
        #    if h_ratio1.GetBinContent(binn) > 0:
        #        h_ratio2.SetBinContent(binn,h_ratio1.GetBinContent(binn))
        #        h_ratio2.SetBinError(binn,h_ratio1.GetBinError(binn))
        #        print 'bin content was:',h_ratio1.GetBinContent(binn),'for bin:',binn,'of',h_ratio1.GetNbinsX(),'in plot',h_ratio1.GetName(),'set bin content/error'
        #print 'last bin of ratio plot has:',h_ratio2.GetBinContent(h_ratio2.GetNbinsX()),'entries and error=',h_ratio2.GetBinError(h_ratio2.GetNbinsX())
        ##h_ratio1.Draw("pe0")

        if doSystErr:
            verbose=False
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

            ## need to make hist with "1" in all bins
            #bgRatioErrs = h_ratio1.Clone()
            #bgRatioErrs.Reset()
            #bgRatioErrs.SetName('bgRatioErrs')
            #for binn in range(0,bgRatioErrs.GetNbinsX()):
            #    bgRatioErrs.SetBinContent(binn,1.0)
            #bgRatioErrsGraph = GetErrorsGraph([bgRatioErrs],backgroundSyst)
            #bgRatioErrsGraph.Draw('E2 same')
            h_ratio1.Draw("zp0same")
        else:
            setRatio1NoBGErrStyle(h_ratio1)
            h_ratio1.Draw("zp0a")
        #h_ratio1.Draw("esame")
        #h_ratio2.Draw("samee0")
        #h_ratio2.Draw("ZP0SAME")

        lineAtOne = TLine(h_ratio.GetXaxis().GetXmin(),1,h_ratio.GetXaxis().GetXmax(),1)
        lineAtOne.SetLineColor(1)
        lineAtOne.Draw()
        pad1.cd()
        pad1.SetBottomMargin(0.05)

    # redraw stack and data on top
    stack.Draw('histsame')
    sig1_hist.Draw("HIST SAME")
    sig2_hist.Draw("HIST SAME")
    g.Draw("ZP0SAME")
    
    #leg = r.TLegend(0.43,0.53,0.89,0.89,"","brNDC") #used for all lq2 data plots
    #leg = r.TLegend(0.52,0.53,0.76,0.88,"","brNDC")
    leg = r.TLegend(0.52,0.45,0.75,0.9,"","brNDC")
    setLegendStyle(leg)
    leg.AddEntry(data_hist ,"Data","lpe")
    if doEEJJ:
      leg.AddEntry(zjets_hist,"Z/#gamma* + jets","f")
    else:
      leg.AddEntry(zjets_hist,"W + jets","f")
    leg.AddEntry(ttbar_hist,"t#bar{t}","f")
    leg.AddEntry(other_hist,"Other background","f")
    leg.AddEntry(qcd_hist  ,"Multijet","f")
    if doSystErr:
      leg.AddEntry(bkgUncHisto, 'Stat#oplussyst uncertainty','f')
    if doEEJJ:
      beta = 1.0
    else:
      beta = 0.5
    leg.AddEntry(sig1_hist  ,"#it{m}_{LQ} = "+str(mass1)+" GeV, #beta = "+str(beta),"l")
    leg.AddEntry(sig2_hist  ,"#it{m}_{LQ} = "+str(mass2)+" GeV, #beta = "+str(beta),"l")
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

    #print 'saving the canvas'
    canvas.SaveAs(save_name)
    canvas.SaveAs(save_namePNG)


#print 'closing files...',
#bkgd_file.Close()
#qcd_file.Close()
#print 'Done!'

