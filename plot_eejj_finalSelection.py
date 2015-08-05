#!/usr/bin/env python

from plot_common import *
import tdrstyle

# set batch
r.gROOT.SetBatch()


masses = [ 450, 650 ]
mass_colors = [ 28, 38 ]

vars     = [ 
    "sT_eejj",
    "Mej_selected_min",
    "Meejj"
] 

x_labels = [ 
    "S_{T}^{eejj} [GeV]",
    "M_{ej}^{min} [GeV]",
    "M_{eejj} [GeV]"
]

x_bins = [ 
    [300, 330, 370, 420, 480, 550, 630, 720, 820, 930, 1050, 1180, 1320, 1470, 1630, 1800, 1980, 2170, 2370, 2580, 2800, 3000],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980],
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980, 3000]
]

systs = [ 0.0627511898374, 0.119404398191 ]

r.gROOT.SetStyle('Plain')
r.gStyle.SetTextFont ( 42 );
r.gStyle.SetTitleFont ( 42, "XYZ" );
r.gStyle.SetLabelFont ( 42, "XYZ" );
r.gStyle.SetOptTitle(0);
r.gStyle.SetOptStat(0);

#set the tdr style
tdrstyle.setTDRStyle()

r.gStyle.SetPadTopMargin(0.1);
r.gStyle.SetPadBottomMargin(0.16);
r.gStyle.SetPadLeftMargin(0.12);
r.gStyle.SetPadRightMargin(0.1);
r.gStyle.SetPadTickX(0)
r.gStyle.SetPadTickY(0)


bkgd_file = r.TFile(os.environ["LQDATA"] + "/LQPlotFiles_fromEdmund/analysisClass_lq_eejj_plots.root" )
qcd_file  = r.TFile(os.environ["LQDATA"] + "/LQPlotFiles_fromEdmund/analysisClass_lq_eejj_QCD_plots.root")

for i_mass, mass in enumerate(masses) :
  for i_var, var in enumerate(vars):
    zjets_hist = bkgd_file.Get( "histo1D__ZJet_Madgraph__"     + var  + "_LQ" + str(mass))
    ttbar_hist = bkgd_file.Get( "histo1D__TTbar_FromData__"    + var  + "_LQ" + str(mass))
    other_hist = bkgd_file.Get( "histo1D__OTHERBKG__"          + var  + "_LQ" + str(mass))
    qcd_hist   = qcd_file .Get( "histo1D__DATA__"              + var  + "_LQ" + str(mass)) 
    data_hist  = bkgd_file.Get( "histo1D__DATA__"              + var  + "_LQ" + str(mass)) 
    sig_hist   = bkgd_file.Get( "histo1D__LQ_M"+str(mass)+"__" + var  + "_LQ" + str(mass)) 

    zjets_hist = rebin ( zjets_hist, x_bins[i_var] )
    ttbar_hist = rebin ( ttbar_hist, x_bins[i_var] )
    other_hist = rebin ( other_hist, x_bins[i_var] )
    qcd_hist   = rebin ( qcd_hist  , x_bins[i_var] )
    data_hist  = rebin ( data_hist , x_bins[i_var] )
    sig_hist   = rebin ( sig_hist  , x_bins[i_var] )

    stack_hist = copy.deepcopy ( zjets_hist )
    stack_hist.Add ( ttbar_hist ) 
    stack_hist.Add ( other_hist ) 
    stack_hist.Add ( qcd_hist ) 

    setStyle (zjets_hist, 2 , 3004, 1)
    setStyle (ttbar_hist, 4 , 3005, 1)
    setStyle (other_hist, 3 , 3006, 1)
    setStyle (qcd_hist  , 7 , 3013, 1)
    setStyle (sig_hist  , mass_colors[i_mass],    0, 3)
    setStyle (data_hist , 1 ,    0, 1)
    setStyle (stack_hist, 14, 3002, 1 )

    data_hist.SetMarkerStyle(20)
    data_hist.SetMarkerSize (1.5)

    stack = r.THStack ("stack", "stack")
    stack.Add ( qcd_hist   );
    stack.Add ( other_hist );
    stack.Add ( ttbar_hist );
    stack.Add ( zjets_hist );
    stack.Draw();
    stack.SetMaximum(200000);
    stack.SetMinimum(0.1);

    n_err_bins = stack_hist.GetNbinsX()
    for bin in range (0, n_err_bins + 1):
      stat_err = stack_hist.GetBinError(bin)
      content  = stack_hist.GetBinContent(bin)
      syst_err = content * systs[i_mass]
      tot_err  = math.sqrt(stat_err * stat_err + syst_err * syst_err ) 
      stack_hist.SetBinError(bin, tot_err)

    stack.GetXaxis().SetTitle( x_labels [i_var] )
    stack.GetYaxis().SetTitle( "Events / bin" )
    stack.GetXaxis().CenterTitle()
    stack.GetYaxis().CenterTitle()

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

    leg = r.TLegend(0.43,0.53,0.89,0.89,"","brNDC");
    leg.SetTextFont(42);
    leg.SetFillColor(0);
    leg.SetBorderSize(0);
    leg.SetTextSize(.05)
    leg.AddEntry(data_hist ,"Data","lpe");
    leg.AddEntry(zjets_hist,"Z/#gamma* + jets","lf")
    leg.AddEntry(ttbar_hist,"t#bar{t}","lf");
    leg.AddEntry(other_hist,"Other background","lf");
    leg.AddEntry(qcd_hist  ,"Multijet","lf");
    leg.AddEntry(stack_hist,"Unc. (stat + syst)");
    leg.AddEntry(sig_hist  ,"LQ, M = "+str(mass)+" GeV, #beta = 1.0","l");

    canv_name = var + "_LQ" + str(mass) + "_canv"
    pad_name  = var + "_LQ" + str(mass) + "_pad"
    save_name = var + "_LQ" + str(mass) 
    save_name = save_name.replace("_eejj", "")
    save_name = save_name + "_eejj.pdf"

    canvas = r.TCanvas(canv_name,canv_name,800,550)
    canvas.cd()
    pad1   = r.TPad( pad_name, pad_name , 0.0, 0.0, 1.0, 1.0 )
    canvas.SetLogy()

    stack.Draw("HIST");
    sig_hist.Draw("HIST SAME");
    stack_hist.Draw("E2 SAME");
    # convert to Poisson error bars
    # check if we need to stop error bars before the end
    lastPopBin = getLastPopulatedBin([zjets_hist,ttbar_hist,other_hist,qcd_hist,data_hist,sig_hist])
    g = poissonErrGraph(data_hist,lastPopBin)
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
    l1.DrawLatex(0.64,0.94,"19.7 fb^{-1} (8 TeV)")
    l2.DrawLatex(0.15,0.84,"CMS")

    canvas.SaveAs(save_name)

