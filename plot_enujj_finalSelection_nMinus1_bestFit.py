import os , math, copy
import ROOT as r
from numpy import array

def setStyle ( plot, color, style, width ) :
    plot.SetLineColor( color ) 
    plot.SetFillColor( color ) 
    plot.SetFillStyle( style ) 
    plot.SetLineWidth( width )
    return

def rebin ( plot, bins ) :
    n_bins    = len ( bins ) - 1
    bin_array = array ( bins, dtype=float ) 
    new_name  = plot.GetName() + "_rebin"
    new_plot  = plot.Rebin ( n_bins, new_name, bin_array ) 
    return new_plot

def makeSafe ( plot ) :
    n_bins = plot.GetNbinsX()
    for i in range ( 1, n_bins + 1 ):
        old_content = plot.GetBinContent(i)
        if old_content > 0. and old_content < 0.0001:
            plot.SetBinContent(i, 0. )
            plot.SetBinError  (i, 0. )
    

masses = [ 650 ]
mass_colors = [ 38 ]

vars     = [ 
    "Mej_stAndMtAndMetLQ"
] 

x_labels = [ 
    "M_{ej} [GeV]"
]

line_values = [ 555 ] 

systs = [ 0.142519011037]

r.gROOT.SetStyle('Plain')
r.gStyle.SetTextFont ( 42 );
r.gStyle.SetTitleFont ( 42, "XYZ" );
r.gStyle.SetLabelFont ( 42, "XYZ" );
r.gStyle.SetOptTitle(0);
r.gStyle.SetOptStat(0);

r.gStyle.SetPadTopMargin(0.1);
r.gStyle.SetPadBottomMargin(0.16);
r.gStyle.SetPadLeftMargin(0.12);
r.gStyle.SetPadRightMargin(0.1);

beta = 0.075
lq_scale = 2. * ( 2. * beta * ( 1. - beta ) )


bkgd_file = r.TFile(os.environ["LQDATA"] + "/enujj_analysis/enujj/scaled_output_cutTable_lq_enujj_MT/analysisClass_lq_enujj_MT_plots.root" )
qcd_file  = r.TFile(os.environ["LQDATA"] + "/enujj_analysis/enujj_qcd/output_cutTable_lq_enujj_MT/analysisClass_lq_enujj_MT_QCD_plots.root")

for i_mass, mass in enumerate(masses) :
    for i_var, var in enumerate(vars):

        wjets_hist = bkgd_file.Get( "histo1D__WJet_Madgraph__"     + var  + str(mass))
	ttbar_hist = bkgd_file.Get( "histo1D__TTbar_Madgraph__"    + var  + str(mass))
	other_hist = bkgd_file.Get( "histo1D__OTHERBKG__"          + var  + str(mass))
	qcd_hist   = qcd_file .Get( "histo1D__DATA__"              + var  + str(mass)) 
	data_hist  = bkgd_file.Get( "histo1D__DATA__"              + var  + str(mass)) 
	sig_hist   = bkgd_file.Get( "histo1D__LQ_M600__" + var  + str(mass)) 
        sig_hist.Scale ( 0.1531 ) 

	wjets_hist .Rebin(10)
	ttbar_hist .Rebin(10)
	other_hist .Rebin(10)
	qcd_hist   .Rebin(10)
	data_hist  .Rebin(10)
        sig_hist   .Rebin(10)



        stack_hist = copy.deepcopy ( wjets_hist )
        stack_hist.Add ( ttbar_hist ) 
        stack_hist.Add ( other_hist ) 
        stack_hist.Add ( qcd_hist ) 
        stack_hist.Add ( sig_hist )
        
	setStyle (wjets_hist, 6 , 3007, 2)
	setStyle (ttbar_hist, 4 , 3005, 2)
	setStyle (other_hist, 3 , 3006, 2)
	setStyle (qcd_hist  , 7 , 3004, 2)
	setStyle (sig_hist  , mass_colors[i_mass],    0, 3)
	setStyle (data_hist , 1 ,    0, 1)
        setStyle (stack_hist, 1, 3002, 1 )
	
	data_hist.SetMarkerStyle(20)
	data_hist.SetMarkerSize (0.7)
	
	stack = r.THStack ("stack", "stack")
	stack.Add ( qcd_hist   );
	stack.Add ( other_hist );
	stack.Add ( ttbar_hist );
	stack.Add ( wjets_hist );
        stack.Add ( sig_hist );
	stack.Draw();
        
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
	stack.GetYaxis().SetTitle( "Events/GeV" )
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
	
	leg = r.TLegend(0.4,0.52,0.86,0.88,"","brNDC");
	leg.SetTextFont(42);
	leg.SetFillColor(0);
	leg.SetBorderSize(0);
	leg.SetTextSize(.05)
	leg.AddEntry(data_hist ,"Data");
	leg.AddEntry(wjets_hist,"W + jets");
	leg.AddEntry(ttbar_hist,"t#bar{t} + jets");
	leg.AddEntry(other_hist,"Other background");
	leg.AddEntry(qcd_hist  ,"QCD");
        leg.AddEntry(stack_hist,"Unc. (stat + syst)");
	leg.AddEntry(sig_hist  ,"LQ, M = 600 GeV, best fit")
	
	sqrts = "#sqrt{s} = 8 TeV";
	l1 = r.TLatex()
	l1.SetTextAlign(12)
	l1.SetTextFont(42)
	l1.SetNDC()
	l1.SetTextSize(0.06)
	
        canv_name = var + "_" + str(mass) + "_canv"
        pad_name  = var + "_" + str(mass) + "_pad"
        save_name = var + "_" + str(mass) + "_bestFit_enujj.pdf"

	canvas = r.TCanvas(canv_name,canv_name,800,550)
	canvas.cd()
        pad1   = r.TPad( pad_name, pad_name , 0.0, 0.0, 1.0, 1.0 )
        # canvas.SetLogy()

	stack.Draw("HIST");
	data_hist.Draw("SAME");
        stack_hist.Draw("E2 SAME");
	leg.Draw()
	l1.DrawLatex(0.18,0.94,"CMS #it{Preliminary}      "+sqrts+", 19.7 fb^{  -1}")
        canvas.Update()

        y_min = canvas.GetUymin()
        y_max = canvas.GetUymax()

        line = r.TLine ( line_values[i_mass], y_min, line_values[i_mass], y_max )
        line.SetLineWidth(3)
        line.SetLineColor(r.kRed)
        line.SetLineStyle(r.kDashed)

        line.Draw("SAME")
	
	canvas.SaveAs(save_name)

