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
    

masses = [ 450, 650 ]
mass_colors = [ 28, 28 ]

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


r.gStyle.SetPadTopMargin(0.1);
r.gStyle.SetPadBottomMargin(0.16);
r.gStyle.SetPadLeftMargin(0.12);
r.gStyle.SetPadRightMargin(0.1);


bkgd_file = r.TFile(os.environ["LQDATA"] + "/eejj_analysis/eejj/scaled_output_cutTable_lq_eejj/analysisClass_lq_eejj_plots.root" )
qcd_file  = r.TFile(os.environ["LQDATA"] + "/eejj_analysis/eejj_qcd/output_cutTable_lq_eejj/analysisClass_lq_eejj_QCD_plots.root")

for i_mass, mass in enumerate(masses) :
    for i_var, var in enumerate(vars):
        
        zjets_hist = bkgd_file.Get( "histo1D__ZJet_Madgraph__"     + var  + "_LQ" + str(mass))
	ttbar_hist = bkgd_file.Get( "histo1D__TTbar_FromData__"    + var  + "_LQ" + str(mass))
	other_hist = bkgd_file.Get( "histo1D__OTHERBKG__"          + var  + "_LQ" + str(mass))
	qcd_hist   = qcd_file .Get( "histo1D__DATA__"              + var  + "_LQ" + str(mass)) 
	data_hist  = bkgd_file.Get( "histo1D__DATA__"              + var  + "_LQ" + str(mass)) 
	sig_hist   = bkgd_file.Get( "histo1D__LQ_M450__"           + var  + "_LQ" + str(mass)) 
        sig_hist.Scale (  0.01514 )

	# zjets_hist = rebin ( zjets_hist, x_bins[i_var] )
	# ttbar_hist = rebin ( ttbar_hist, x_bins[i_var] )
	# other_hist = rebin ( other_hist, x_bins[i_var] )
	# qcd_hist   = rebin ( qcd_hist  , x_bins[i_var] )
	# data_hist  = rebin ( data_hist , x_bins[i_var] )
        # sig_hist   = rebin ( sig_hist  , x_bins[i_var] )

	zjets_hist .Rebin ( 10 )
	ttbar_hist .Rebin ( 10 )
	other_hist .Rebin ( 10 )
	qcd_hist   .Rebin ( 10 )
	data_hist  .Rebin ( 10 )
        sig_hist   .Rebin ( 10 )

        stack_hist = copy.deepcopy ( zjets_hist )
        stack_hist.Add ( ttbar_hist ) 
        stack_hist.Add ( other_hist ) 
        stack_hist.Add ( qcd_hist ) 
        
	setStyle (zjets_hist, 2 , 3007, 2)
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
	stack.Add ( zjets_hist );
        stack.Add ( sig_hist   );
	stack.Draw();
        stack.SetMaximum(20000);
        stack.SetMinimum(0.1);

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
	
	leg = r.TLegend(0.43,0.52,0.89,0.88,"","brNDC");
	leg.SetTextFont(42);
	leg.SetFillColor(0);
	leg.SetBorderSize(0);
	leg.SetTextSize(.05)
	leg.AddEntry(data_hist ,"Data");
	leg.AddEntry(zjets_hist,"Z + jets");
	leg.AddEntry(ttbar_hist,"t#bar{t} + jets");
	leg.AddEntry(other_hist,"Other background");
	leg.AddEntry(qcd_hist  ,"QCD");
        leg.AddEntry(stack_hist,"Unc. (stat + syst)");
	leg.AddEntry(sig_hist  ,"LQ, M = 450 GeV, best fit");
	
	sqrts = "#sqrt{s} = 8 TeV";
	l1 = r.TLatex()
	l1.SetTextAlign(12)
	l1.SetTextFont(42)
	l1.SetNDC()
	l1.SetTextSize(0.06)
	
        canv_name = var + "_" + str(mass) + "_canv"
        pad_name  = var + "_" + str(mass) + "_pad"
        save_name = var + "_" + str(mass) 
        save_name = save_name.replace("_eejj", "")
        save_name = save_name + "_bestFit_eejj.pdf"

	canvas = r.TCanvas(canv_name,canv_name,800,550)
	canvas.cd()
        pad1   = r.TPad( pad_name, pad_name , 0.0, 0.0, 1.0, 1.0 )
        canvas.SetLogy()

	stack.Draw("HIST");
        # sig_hist.Draw("HIST SAME");
	data_hist.Draw("SAME");
        stack_hist.Draw("E2 SAME");
	leg.Draw()
	l1.DrawLatex(0.18,0.94,"CMS #it{Preliminary}      "+sqrts+", 19.7 fb^{  -1}")
	
        print "Here"
	canvas.SaveAs(save_name)

print "Here final"
