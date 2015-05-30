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
mass_colors = [ 28 ]

vars     = [ 
    "Mej_selected_min_StAndMeeLQ"
] 

x_labels = [ 
    "M_{ej}^{min} [GeV]"
]

x_bins = [ 
    [0, 25, 55, 90, 130, 175, 225, 280, 340, 405, 475, 550, 630, 715, 805, 900, 1000, 1105, 1215, 1330, 1450, 1575, 1705, 1840, 1980]
    # [50, 150, 250, 350, 450, 550, 650, 750, 850, 950, 1050, 1150, 1250, 1350, 1450, 1550, 1650, 1750 ]
]


line_values = [ 360 ] 


systs = [ 0.119404398191 ]

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
lq_scale = beta * beta 


bkgd_file = r.TFile(os.environ["LQDATA"] + "/eejj_analysis/eejj/scaled_output_cutTable_lq_eejj/analysisClass_lq_eejj_plots.root" )
qcd_file  = r.TFile(os.environ["LQDATA"] + "/eejj_analysis/eejj_qcd/output_cutTable_lq_eejj/analysisClass_lq_eejj_QCD_plots.root")

for i_mass, mass in enumerate(masses) :
    for i_var, var in enumerate(vars):
        
        zjets_hist = bkgd_file.Get( "histo1D__ZJet_Madgraph__"     + var  + str(mass))
	ttbar_hist = bkgd_file.Get( "histo1D__TTbar_FromData__"    + var  + str(mass))
	other_hist = bkgd_file.Get( "histo1D__OTHERBKG__"          + var  + str(mass))
	qcd_hist   = qcd_file .Get( "histo1D__DATA__"              + var  + str(mass)) 
	data_hist  = bkgd_file.Get( "histo1D__DATA__"              + var  + str(mass)) 
	sig_hist   = bkgd_file.Get( "histo1D__LQ_M450__"           + var  + str(mass)) 
        sig_hist.Scale (  0.01514 )
	# zjets_hist.Rebin(10)
	# ttbar_hist.Rebin(10)
	# other_hist.Rebin(10)
	# qcd_hist  .Rebin(10)
	# data_hist .Rebin(10)
        # sig_hist  .Rebin(10)
        
        stack_hist = copy.deepcopy ( zjets_hist )
        stack_hist.Add ( ttbar_hist ) 
        stack_hist.Add ( other_hist ) 
        stack_hist.Add ( qcd_hist ) 
        stack_hist.Add ( sig_hist ) 
        
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
        stack.Add ( sig_hist ) 
	stack.Draw();
        # stack.SetMaximum(200000);
        # stack.SetMinimum(0.1);

        stack.SetMaximum(22);

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
	
	leg = r.TLegend(0.4,0.52,0.86,0.88,"","brNDC");
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
	leg.AddEntry(sig_hist  ,"LQ, M = 450 GeV, best fit")
	
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
        # canvas.SetLogy()

	stack.Draw("HIST");
        # sig_hist.Draw("HIST SAME");
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

