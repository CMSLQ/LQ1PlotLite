#!/usr/bin/env python

from plot_common import *
import tdrstyle

# set batch
r.gROOT.SetBatch()


masses = [ 650 ]
mass_colors = [ 38 ]

vars     = [ 
    "Mej_stAndMtAndMetLQ"
] 

x_labels = [ 
    "M_{ej} [GeV]"
]

x_bins = [ 
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980]
]

line_values = [ 555 ] 

systs = [ 0.142519011037]

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

beta = 0.075
lq_scale = 2. * ( 2. * beta * ( 1. - beta ) )


bkgd_file = r.TFile(os.environ["LQDATA"] + "/LQPlotFiles_fromEdmund/analysisClass_lq_enujj_MT_plots.root" )
qcd_file  = r.TFile(os.environ["LQDATA"] + "/LQPlotFiles_fromEdmund/analysisClass_lq_enujj_MT_QCD_plots.root")

for i_mass, mass in enumerate(masses) :
  for i_var, var in enumerate(vars):

    wjets_hist = bkgd_file.Get( "histo1D__WJet_Madgraph__"     + var  + str(mass))
    ttbar_hist = bkgd_file.Get( "histo1D__TTbar_Madgraph__"    + var  + str(mass))
    other_hist = bkgd_file.Get( "histo1D__OTHERBKG__"          + var  + str(mass))
    qcd_hist   = qcd_file .Get( "histo1D__DATA__"              + var  + str(mass)) 
    data_hist  = bkgd_file.Get( "histo1D__DATA__"              + var  + str(mass)) 
    sig_hist   = bkgd_file.Get( "histo1D__LQ_M"+str(mass)+"__" + var  + str(mass)) 

    wjets_hist = rebin ( wjets_hist, x_bins[i_var] )
    ttbar_hist = rebin ( ttbar_hist, x_bins[i_var] )
    other_hist = rebin ( other_hist, x_bins[i_var] )
    qcd_hist   = rebin ( qcd_hist  , x_bins[i_var] )
    data_hist  = rebin ( data_hist , x_bins[i_var] )
    sig_hist   = rebin ( sig_hist  , x_bins[i_var] )

    sig_hist.Scale ( lq_scale ) 

    stack_hist = copy.deepcopy ( wjets_hist )
    stack_hist.Add ( ttbar_hist ) 
    stack_hist.Add ( other_hist ) 
    stack_hist.Add ( qcd_hist ) 
        
    setStyle (wjets_hist, 6 , 3007, 1)
    setStyle (ttbar_hist, 4 , 3005, 1)
    setStyle (other_hist, 3 , 3006, 1)
    setStyle (qcd_hist  , 7 , 3013, 1)
    setStyle (sig_hist  , mass_colors[i_mass],    0, 4)
    setStyle (data_hist , 1 ,    0, 1)
    setStyle (stack_hist, 14, 3002, 1 )
  
    data_hist.SetMarkerStyle(20)
    data_hist.SetMarkerSize (1.5)
  
    stack = r.THStack ("stack", "stack")
    stack.Add ( qcd_hist   )
    stack.Add ( other_hist )
    stack.Add ( ttbar_hist )
    stack.Add ( wjets_hist )
    stack.Draw()
        
    stack.SetMaximum(200000);
    stack.SetMinimum(0.1);

    stack.SetMaximum(10)
    stack.SetMinimum(0.0);

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
  
    leg = r.TLegend(0.41,0.57,0.73,0.87,"","brNDC")
    leg.SetTextFont(42);
    leg.SetFillColor(0);
    leg.SetBorderSize(0);
    leg.SetTextSize(.05)
    leg.AddEntry(data_hist ,"Data","lpe");
    leg.AddEntry(wjets_hist,"W + jets","lf");
    leg.AddEntry(ttbar_hist,"t#bar{t}","lf");
    leg.AddEntry(other_hist,"Other background","lf");
    leg.AddEntry(qcd_hist  ,"Multijet","lf");
    leg.AddEntry(stack_hist,"Unc. (stat + syst)");
    leg.AddEntry(sig_hist  ,"LQ, M = "+str(mass)+" GeV, #beta = 0.075","l");
  
    canv_name = var + str(mass) + "_canv"
    pad_name  = var + str(mass) + "_pad"
    save_name = var + str(mass) + "_enujj.pdf"

    canvas = r.TCanvas(canv_name,canv_name,800,550)
    canvas.cd()
    pad1   = r.TPad( pad_name, pad_name , 0.0, 0.0, 1.0, 1.0 )

    stack.Draw("HIST")
    sig_hist.Draw("HIST SAME")
    # set range?
    #sig_hist.SetRangeUser(50,1600)
    #sig_hist.GetXaxis().SetRange(sig_hist.FindBin(50),sig_hist.FindBin(1600))
    #for bin in sig_hist.GetNbinsX():
    #  if sig_hist.GetBinContent(bin)==0:
    #    sig_hist.SetBinEntries(bin)
    #
    sig_hist.Draw("HIST SAME")
    stack_hist.Draw("E2 SAME")
    data_hist.Draw("HIST P SAME")
    # convert to Poisson error bars
    # check if we need to stop error bars before the end
    lastPopBin = getLastPopulatedBin([wjets_hist,ttbar_hist,other_hist,qcd_hist,data_hist,sig_hist],0.1)
    g = poissonErrGraph(data_hist,lastPopBin)
    setStyle (g , 1 ,    0, 1)
    g.Draw("same z")
    sig_hist.Draw("HIST SAME")
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

    ## TESTING
    #canvas.SetLogy()
    #data_hist.Draw('pe0')
    #for bin in range(1,data_hist.GetNbinsX()):
    #  print 'bin:',bin,'bin center:',data_hist.GetBinCenter(bin),'bin content:',data_hist.GetBinContent(bin)
    ## convert to Poisson error bars
    ## check if we need to stop error bars before the end
    #lastPopBin = getLastPopulatedBin([wjets_hist,ttbar_hist,other_hist,qcd_hist,data_hist,sig_hist])
    #g = poissonErrGraph(data_hist,lastPopBin)
    #setStyle (g , 1 ,    0, 1)
    #g.Draw("same z")
        
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

    canvas.Update()

    y_min = canvas.GetUymin()
    y_max = canvas.GetUymax()

    #line = r.TLine ( line_values[i_mass], y_min, line_values[i_mass], y_max )
    #line.SetLineWidth(3)
    #line.SetLineColor(r.kRed)
    #line.SetLineStyle(r.kDashed)
    #line.Draw("SAME")
  
    canvas.SaveAs(save_name)

    ### wait for input to keep the GUI (which lives on a ROOT event dispatcher) alive
    #if __name__ == '__main__':
    #   rep = ''
    #   while not rep in [ 'q', 'Q' ]:
    #      rep = raw_input( 'enter "q" to quit: ' )
    #      if 1 < len(rep):
    #         rep = rep[0]

