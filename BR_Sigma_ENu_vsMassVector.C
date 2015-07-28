#include "TROOT.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TH2F.h"
#include "TGraph.h"
#include "TF1.h"
#include "TLegend.h"
#include "TPolyLine.h"
#include "TPad.h"
#include "TLatex.h"
#include "TMath.h"
#include "stdio.h"
using namespace std;
void myStyle();
void setTDRStyle();
//void makePlotsBHVector()
void BR_Sigma_ENu_vsMassVector()
{

 // filename for the final plot (NB: changing the name extension changes the file format)
 string fileNamePdf = "BR_Sigma_ENuVector.pdf";
 string fileNamePng = "BR_Sigma_ENuVector.png";
 string fileNameEps = "BR_Sigma_ENuVector.eps";

 // axes labels for the final plot
 string title = ";M_{LQ} [GeV];#sigma#times2#beta(1-#beta) [pb]";

 // integrated luminosity
 string lint = "19.7 fb^{-1}";

bool NoteStyle = false;


Double_t mTh[16] = {300.0 , 400.0 , 500.0 , 600.0 , 700.0 , 800.0 , 900.0 , 1000.0 , 1100.0 , 1200.0 , 1300.0 , 1400.0 , 1500.0 , 1600.0 , 1700.0 , 1800.0 }; 
Double_t mData[16] = {300.0 , 400.0 , 500.0 , 600.0 , 700.0 , 800.0 , 900.0 , 1000.0 , 1100.0 , 1200.0 , 1300.0 , 1400.0 , 1500.0 , 1600.0 , 1700.0 , 1800.0 }; 
Double_t MCx_shademasses[32] = {300.0 , 400.0 , 500.0 , 600.0 , 700.0 , 800.0 , 900.0 , 1000.0 , 1100.0 , 1200.0 , 1300.0 , 1400.0 , 1500.0 , 1600.0 , 1700.0 , 1800.0 , 1800.0 , 1700.0 , 1600.0 , 1500.0 , 1400.0 , 1300.0 , 1200.0 , 1100.0 , 1000.0 , 900.0 , 800.0 , 700.0 , 600.0 , 500.0 , 400.0 , 300.0 }; 


Double_t YMxsTh[16] = { 0.5*104.6, 0.5*17.74, 0.5*4.03, 0.5*1.125, 0.5*0.3519, 0.5*0.1194, 0.5*0.04373, 0.5*0.01731, 0.5*0.006853, 0.5*0.002832, 0.5*0.001203, 0.5*0.0005089, 0.5*0.0002236, 0.5*9.675E-05, 0.5*4.159E-05, 0.5*1.794E-05 };
Double_t MCxsTh[16] = { 0.5*21.19, 0.5*3.354, 0.5*0.7378, 0.5*0.2034, 0.5*0.06362, 0.5*0.02177, 0.5*0.008059, 0.5*0.003231, 0.5*0.001298, 0.5*0.0005442, 0.5*0.0002344, 0.5*0.0001006, 0.5*4.478E-05, 0.5*1.96E-05, 0.5*8.518E-06, 0.5*3.711E-06 };
Double_t MMxsTh[16] = { 0.5*2510, 0.5*242.9, 0.5*40.14, 0.5*9.204, 0.5*2.528, 0.5*0.7827, 0.5*0.2678, 0.5*0.1006, 0.5*0.03822, 0.5*0.01528, 0.5*0.006316, 0.5*0.002614, 0.5*0.001128, 0.5*0.0004799, 0.5*0.0002037, 0.5*8.697E-05 };
Double_t AMxsTh[16] = { 0.5*20.06, 0.5*2.956, 0.5*0.5897, 0.5*0.1458, 0.5*0.04056, 0.5*0.01228, 0.5*0.004027, 0.5*0.001431, 0.5*0.0005108, 0.5*0.0001909, 0.5*7.373E-05, 0.5*2.849E-05, 0.5*1.148E-05, 0.5*4.578E-06, 0.5*1.829E-06, 0.5*7.371E-07 };



// Insert limit information below

 Double_t MCxsUp_expected[16] = {0.087121911565 , 0.013804014198 , 0.0034947346777 , 0.0014848365771 , 0.00074926753165 , 0.000538620158265 , 0.000383136879998 
, 0.000351469348007 , 0.000328165485802 , 0.00031006888706 , 0.000288935181583 , 0.000284485653922 , 0.000274791034062 , 0.000278477719495 , 0.000269413739941 
, 0.000265565039977 }; 
Double_t MCxsUp_observed[16] = {0.09545955146 , 0.016379589369 , 0.0039085202163 , 0.0028719806427 , 0.00093475584057 , 0.000726334073185 , 0.000465632998708 ,
 0.000428242147079 , 0.000398500440899 , 0.000377541761603 , 0.00035126097638 , 0.000346472665267 , 0.000335455237522 , 0.000338180578854 , 0.000327032729224 ,
 0.000322679512606 }; 
Double_t MCy_1sigma[32]={0.06449994434 , 0.010187241714 , 0.0025380231464 , 0.001043538615 , 0.00050420869935 , 0.000349446412455 , 0.000237177615115 , 0.000216772331171 , 0.000202311801043 , 0.000190530832037 , 0.000177833401131 , 0.000175459443545 , 0.000170107039347 , 0.000171679630276 , 0.000166091739328 , 0.000163719052689 , 0.000449753369796 , 0.000456271434858 , 0.000471621934511 , 0.000465378239144 , 0.000481796764752 , 0.000489332376527 , 0.000525123824894 , 0.000555771694511 , 0.000595238462842 , 0.000648869704015 , 0.00085422371244 , 0.0011345405496 , 0.0021418036272 , 0.0048738204774 , 0.018701095686 , 0.11664001596 }; 
Double_t MCy_2sigma[32]={0.04951655891 , 0.007791717648 , 0.0019043573451 , 0.0007743190869 , 0.00036438988019 , 0.00024511424259 , 0.000159390934236 , 0.000146216743461 , 0.000135240069866 , 0.000128993501725 , 0.000119637228498 , 0.000118350475648 , 0.000114317360034 , 0.000114763280867 , 0.000111027928905 , 0.00010944184132 , 0.000726482440475 , 0.000737010994767 , 0.000761806520082 , 0.0007517212061 , 0.000778241845967 , 0.000790414063677 , 0.000848227654018 , 0.000897732885049 , 0.000961483110844 , 0.00104811320873 , 0.00131338863905 , 0.00167519908736 , 0.0029669196267 , 0.0065593157238 , 0.024247065492 , 0.148498110865 };
 

Double_t YMxsUp_observed[15] = {0.1109872944 , 0.0181199021 , 0.002896471125 , 0.0009530127648 , 0.0007254187596 , 0.00047178875775 , 0.00043340298513 , 0.000401914839942 , 0.000368364022944 , 0.00034706527564 , 0.000340356659899 , 0.000334980085014 , 0.000326288309057 , 0.000323290925521 , 0.000319591184966 }; 
Double_t MMxsUp_observed[16] = {0.08665022 , 0.0146973932 , 0.0036585603 , 0.002632288776 , 0.000885721456 , 0.0006801749097 , 0.0004426222502 , 0.0004223432961 , 0.00039106381041 , 0.0003683882322 , 0.000352326732254 , 0.000344644589222 , 0.000334599337104 , 0.000328835723002 , 0.000329587434152 , 0.000322624962032 
}; 
Double_t AMxsUp_observed[16] = {0.09244942873 , 0.015923642406 , 0.0038437442095 , 0.0027603186966 , 0.00091561721784 , 0.0007149188206 , 0.000463587740652 , 0.00043149863133 , 0.000396582520794 , 0.000373413913906 , 0.00036009965079 , 0.000347382555936 , 0.000337547602855 , 0.000333439833984 , 0.000329608759601 , 0.000329282251405 }; 


 Double_t MCxsUp_observed_logY[16], MCxsUp_expected_logY[16], MCxsTh_logY[16],YMxsTh_logY[16],MMxsTh_logY[16],AMxsTh_logY[16];
 for (int ii = 0; ii<16; ++ii) MCxsUp_observed_logY[ii] = log10(MCxsUp_observed[ii]);
 for (int ii = 0; ii<16; ++ii) MCxsUp_expected_logY[ii] = log10(MCxsUp_expected[ii]);
 for (int ii = 0; ii<16; ++ii) MCxsTh_logY[ii] = log10(MCxsTh[ii]);
 for (int ii = 0; ii<16; ++ii) YMxsTh_logY[ii] = log10(YMxsTh[ii]);
 for (int ii = 0; ii<16; ++ii) MMxsTh_logY[ii] = log10(MMxsTh[ii]);
 for (int ii = 0; ii<16; ++ii) AMxsTh_logY[ii] = log10(AMxsTh[ii]);

 TGraph *MCxsData_vs_m_expected_log = new TGraph(16, mData, MCxsUp_expected_logY);
 TGraph *MCxsData_vs_m_observed_log = new TGraph(16, mData, MCxsUp_observed_logY);
 TGraph *MCxsTh_vs_m_log = new TGraph(16, mTh, MCxsTh_logY);
 TGraph *YMxsTh_vs_m_log = new TGraph(16, mTh, YMxsTh_logY);
 TGraph *MMxsTh_vs_m_log = new TGraph(16, mTh, MMxsTh_logY);
 TGraph *AMxsTh_vs_m_log = new TGraph(16, mTh, AMxsTh_logY);
 

 double MCobslim = 0.0;
 double MCexlim = 0.0;
 double YMobslim = 0.0;
 double YMexlim = 0.0;
 double MMobslim = 0.0;
 double MMexlim = 0.0;
 double AMobslim = 0.0;
 double AMexlim = 0.0;   
 for (Double_t mtest=300.10; mtest<1799.90; mtest = mtest+0.10){
   if(( pow(10.0,MCxsData_vs_m_expected_log->Eval(mtest))/pow(10.0,MCxsTh_vs_m_log->Eval(mtest)) ) < 1.0 && ( pow(10.0,MCxsData_vs_m_expected_log->Eval(mtest+0.1))/pow(10.0,MCxsTh_vs_m_log->Eval(mtest+0.10)) ) > 1.0) MCexlim = mtest; 
   if(( pow(10.0,MCxsData_vs_m_observed_log->Eval(mtest))/pow(10.0,MCxsTh_vs_m_log->Eval(mtest)) ) < 1.0 && ( pow(10.0,MCxsData_vs_m_observed_log->Eval(mtest+0.1))/pow(10.0,MCxsTh_vs_m_log->Eval(mtest+0.10)) ) > 1.0) MCobslim = mtest; 
   if(( pow(10.0,MCxsData_vs_m_expected_log->Eval(mtest))/pow(10.0,YMxsTh_vs_m_log->Eval(mtest)) ) < 1.0 && ( pow(10.0,MCxsData_vs_m_expected_log->Eval(mtest+0.1))/pow(10.0,YMxsTh_vs_m_log->Eval(mtest+0.10)) ) > 1.0) YMexlim = mtest; 
   if(( pow(10.0,MCxsData_vs_m_observed_log->Eval(mtest))/pow(10.0,YMxsTh_vs_m_log->Eval(mtest)) ) < 1.0 && ( pow(10.0,MCxsData_vs_m_observed_log->Eval(mtest+0.1))/pow(10.0,YMxsTh_vs_m_log->Eval(mtest+0.10)) ) > 1.0) YMobslim = mtest; 
   if(( pow(10.0,MCxsData_vs_m_expected_log->Eval(mtest))/pow(10.0,MMxsTh_vs_m_log->Eval(mtest)) ) < 1.0 && ( pow(10.0,MCxsData_vs_m_expected_log->Eval(mtest+0.1))/pow(10.0,MMxsTh_vs_m_log->Eval(mtest+0.10)) ) > 1.0) MMexlim = mtest; 
   if(( pow(10.0,MCxsData_vs_m_observed_log->Eval(mtest))/pow(10.0,MMxsTh_vs_m_log->Eval(mtest)) ) < 1.0 && ( pow(10.0,MCxsData_vs_m_observed_log->Eval(mtest+0.1))/pow(10.0,MMxsTh_vs_m_log->Eval(mtest+0.10)) ) > 1.0) MMobslim = mtest; 
   if(( pow(10.0,MCxsData_vs_m_expected_log->Eval(mtest))/pow(10.0,AMxsTh_vs_m_log->Eval(mtest)) ) < 1.0 && ( pow(10.0,MCxsData_vs_m_expected_log->Eval(mtest+0.1))/pow(10.0,AMxsTh_vs_m_log->Eval(mtest+0.10)) ) > 1.0) AMexlim = mtest; 
   if(( pow(10.0,MCxsData_vs_m_observed_log->Eval(mtest))/pow(10.0,AMxsTh_vs_m_log->Eval(mtest)) ) < 1.0 && ( pow(10.0,MCxsData_vs_m_observed_log->Eval(mtest+0.1))/pow(10.0,AMxsTh_vs_m_log->Eval(mtest+0.10)) ) > 1.0) AMobslim = mtest; 

  }
  std::cout<<"## MC LLJJ observed limit: "<<MCobslim<<" GeV"<<std::endl;
  std::cout<<"## MC LLJJ expected limit: "<<MCexlim<<" GeV"<<std::endl;
  std::cout<<"## YM LLJJ observed limit: "<<YMobslim<<" GeV"<<std::endl;
  std::cout<<"## YM LLJJ expected limit: "<<YMexlim<<" GeV"<<std::endl;
  std::cout<<"## MM LLJJ observed limit: "<<MMobslim<<" GeV"<<std::endl;
  std::cout<<"## MM LLJJ expected limit: "<<MMexlim<<" GeV"<<std::endl;
  std::cout<<"## AM LLJJ observed limit: "<<AMobslim<<" GeV"<<std::endl;
  std::cout<<"## AM LLJJ expected limit: "<<AMexlim<<" GeV"<<std::endl;    
  // turn on/off batch mode
 gROOT->SetBatch(kTRUE);


 // set ROOT style
//  myStyle();
 setTDRStyle();
 gStyle->SetPadLeftMargin(0.14);
 gROOT->ForceStyle();
 
 TCanvas *c = new TCanvas("c","",800,800);
 c->cd();
 
 TH2F *bg = new TH2F("bg",title.c_str(), 500, 300., 1800., 500., 0.0000005, 6000.);
 bg->GetXaxis()->CenterTitle();
 bg->GetYaxis()->CenterTitle();
 bg->SetStats(kFALSE);
 bg->SetTitleOffset(1.,"X");
 bg->SetTitleOffset(1.1,"Y");
 
 bg->Draw();



TGraph *MCxsTh_vs_m = new TGraph(16, mTh, MCxsTh);
MCxsTh_vs_m->SetLineWidth(3);
MCxsTh_vs_m->SetLineColor(2);
MCxsTh_vs_m->SetLineStyle(5);
MCxsTh_vs_m->SetFillColor(0);
MCxsTh_vs_m->SetMarkerSize(0.00001);
MCxsTh_vs_m->SetMarkerStyle(22);
MCxsTh_vs_m->SetMarkerColor(kBlue);

TGraph *MMxsTh_vs_m = new TGraph(16, mTh, MMxsTh);
MMxsTh_vs_m->SetLineWidth(3);
MMxsTh_vs_m->SetLineColor(4);
MMxsTh_vs_m->SetLineStyle(2);
MMxsTh_vs_m->SetFillColor(0);
MMxsTh_vs_m->SetMarkerSize(0.00001);
MMxsTh_vs_m->SetMarkerStyle(22);
MMxsTh_vs_m->SetMarkerColor(kBlue);

TGraph *YMxsTh_vs_m = new TGraph(16, mTh, YMxsTh);
YMxsTh_vs_m->SetLineWidth(3);
YMxsTh_vs_m->SetLineColor(6);
YMxsTh_vs_m->SetLineStyle(3);
YMxsTh_vs_m->SetFillColor(0);
YMxsTh_vs_m->SetMarkerSize(0.00001);
YMxsTh_vs_m->SetMarkerStyle(22);
YMxsTh_vs_m->SetMarkerColor(kBlue);

TGraph *AMxsTh_vs_m = new TGraph(16, mTh, AMxsTh);
AMxsTh_vs_m->SetLineWidth(3);
AMxsTh_vs_m->SetLineColor(8);
AMxsTh_vs_m->SetLineStyle(4);
AMxsTh_vs_m->SetFillColor(0);
AMxsTh_vs_m->SetMarkerSize(0.00001);
AMxsTh_vs_m->SetMarkerStyle(22);
AMxsTh_vs_m->SetMarkerColor(kBlue);


TGraph *MCxsData_vs_m_expected = new TGraph(16, mData, MCxsUp_expected);
MCxsData_vs_m_expected->SetMarkerStyle(0);
MCxsData_vs_m_expected->SetMarkerColor(kBlack);
MCxsData_vs_m_expected->SetLineColor(kBlack);
MCxsData_vs_m_expected->SetLineWidth(2);
MCxsData_vs_m_expected->SetLineStyle(7);
MCxsData_vs_m_expected->SetMarkerSize(0.001);

TGraph *MCxsData_vs_m_observed = new TGraph(16, mData, MCxsUp_observed);
MCxsData_vs_m_observed->SetMarkerStyle(21);
MCxsData_vs_m_observed->SetMarkerColor(kBlack);
MCxsData_vs_m_observed->SetLineColor(kBlack);
MCxsData_vs_m_observed->SetLineWidth(2);
MCxsData_vs_m_observed->SetLineStyle(1);
MCxsData_vs_m_observed->SetMarkerSize(1);


 TGraph *MCexshade1 = new TGraph(32,MCx_shademasses,MCy_1sigma);
 MCexshade1->SetFillColor(kGreen);
 TGraph *MCexshade2 = new TGraph(32,MCx_shademasses,MCy_2sigma);
 MCexshade2->SetFillColor(kYellow);



TGraph *YMxsData_vs_m_observed = new TGraph(16, mData, YMxsUp_observed);
YMxsData_vs_m_observed->SetMarkerStyle(5);
YMxsData_vs_m_observed->SetMarkerColor(6);
YMxsData_vs_m_observed->SetLineColor(6);
YMxsData_vs_m_observed->SetLineWidth(2);
YMxsData_vs_m_observed->SetLineStyle(1);
YMxsData_vs_m_observed->SetMarkerSize(2);


TGraph *AMxsData_vs_m_observed = new TGraph(16, mData, AMxsUp_observed);
AMxsData_vs_m_observed->SetMarkerStyle(5);
AMxsData_vs_m_observed->SetMarkerColor(8);
AMxsData_vs_m_observed->SetLineColor(8);
AMxsData_vs_m_observed->SetLineWidth(2);
AMxsData_vs_m_observed->SetLineStyle(1);
AMxsData_vs_m_observed->SetMarkerSize(2);

TGraph *MMxsData_vs_m_observed = new TGraph(16, mData, MMxsUp_observed);
MMxsData_vs_m_observed->SetMarkerStyle(5);
MMxsData_vs_m_observed->SetMarkerColor(4);
MMxsData_vs_m_observed->SetLineColor(4);
MMxsData_vs_m_observed->SetLineWidth(2);
MMxsData_vs_m_observed->SetLineStyle(1);
MMxsData_vs_m_observed->SetMarkerSize(2);





 MCexshade2->Draw("f");
 MCexshade1->Draw("f");

 gPad->RedrawAxis();


 setTDRStyle();
 gStyle->SetPadLeftMargin(0.14);
 gROOT->ForceStyle();


 
 MCxsTh_vs_m->Draw("L");
 MMxsTh_vs_m->Draw("L");
 YMxsTh_vs_m->Draw("L");
 AMxsTh_vs_m->Draw("L");
 

 MCxsData_vs_m_expected->Draw("LP");
 MCxsData_vs_m_observed->Draw("LP");

if (NoteStyle)
{
 AMxsData_vs_m_observed->Draw("LP");
 YMxsData_vs_m_observed->Draw("LP");
 MMxsData_vs_m_observed->Draw("LP");
}
 
 // grshade->SetFillStyle(1001); 


 TLegend *legend = new TLegend(.46,.57,.92,.88);
 legend->SetBorderSize(1);
 legend->SetFillColor(0);
 //legend->SetFillStyle(0);
 legend->SetTextFont(42);
 legend->SetTextSize(.035);
 legend->SetMargin(0.15);
 legend->SetHeader("LQ #bar{LQ} #rightarrow e#nujj");
 // legend->AddEntry(p2,"ATLAS exclusion (1.03 fb^{-1}, 7 TeV)","f");
 // legend->AddEntry(pl,"CMS exclusion (5.0 fb^{-1}, 7TeV)","f");
 // legend->AddEntry(p3,"CMS exclusion (19.7 fb^{-1}, 8 TeV)","f");

legend->AddEntry(MMxsTh_vs_m,"MM, #sigma_{theory}#times 2#beta(1-#beta), (#beta=1/2)","lf");
legend->AddEntry(MCxsTh_vs_m,"MC, #sigma_{theory}#times 2#beta(1-#beta), (#beta=1/2)","lf");
legend->AddEntry(YMxsTh_vs_m,"YM, #sigma_{theory}#times 2#beta(1-#beta), (#beta=1/2)","lf");
legend->AddEntry(AMxsTh_vs_m,"AM, #sigma_{theory}#times 2#beta(1-#beta), (#beta=1/2)","lf");

 legend->AddEntry(MCxsData_vs_m_expected, "Exp. 95% CL upper limit","lp");
 legend->AddEntry(MCxsData_vs_m_observed, "Obs. 95% CL upper limit","lp");
 legend->Draw();


 TLatex l1;
 l1.SetTextAlign(12);
 l1.SetTextFont(42);
 l1.SetNDC();
 l1.SetTextSize(0.046);
 TLatex l2;
 l2.SetTextAlign(12);
 l2.SetTextFont(62);
 l2.SetNDC();
 l2.SetTextSize(0.065);

 l1.DrawLatex(0.651,0.93,"19.7 fb^{-1} (8 TeV)");
 l2.DrawLatex(0.2,0.85,"CMS");


if (NoteStyle)
{
 TLatex l1b;
 l1b.SetTextAlign(12);
 l1b.SetTextFont(42);
 l1b.SetNDC();
 l1b.SetTextSize(0.025);
 l1b.DrawLatex(.17,.215,"The limits are computed with the MC vector sample.");
 l1b.DrawLatex(.17,.19,"X markers indicate observed limits using other vector samples.");
 l1b.DrawLatex(.17,.165,"X markers would be removed for publication.");
}

 c->SetGridx();
 c->SetGridy();
 c->RedrawAxis();
 legend->Draw();

 c->SetLogy();
 c->SaveAs((fileNamePdf).c_str());
 //c->SaveAs((fileNameEps).c_str());
 //c->SaveAs((fileNamePng).c_str());

}


void myStyle()
{
 gStyle->Reset("Default");
 gStyle->SetCanvasColor(0);
 gStyle->SetPadColor(0);
 gStyle->SetTitleFillColor(10);
 gStyle->SetCanvasBorderMode(0);
 gStyle->SetStatColor(0);
 gStyle->SetPadBorderMode(0);
 gStyle->SetPadTickX(1);  // To get tick marks on the opposite side of the frame
 gStyle->SetPadTickY(1);
 gStyle->SetFrameBorderMode(0);
 gStyle->SetPalette(1);

   //gStyle->SetOptStat(kFALSE);
 gStyle->SetOptStat(111110);
 gStyle->SetOptFit(0);
 gStyle->SetStatFont(42);
 gStyle->SetPadLeftMargin(0.13);
 gStyle->SetPadRightMargin(0.07);
 gStyle->SetStatY(.9);
}

void setTDRStyle() {
  TStyle *tdrStyle = new TStyle("tdrStyle","Style for P-TDR");

  // For the canvas:
  tdrStyle->SetCanvasBorderMode(0);
  tdrStyle->SetCanvasColor(kWhite);
  tdrStyle->SetCanvasDefH(600); //Height of canvas
  tdrStyle->SetCanvasDefW(600); //Width of canvas
  tdrStyle->SetCanvasDefX(0);   //POsition on screen
  tdrStyle->SetCanvasDefY(0);

  // For the Pad:
  tdrStyle->SetPadBorderMode(0);
  // tdrStyle->SetPadBorderSize(Width_t size = 1);
  tdrStyle->SetPadColor(kWhite);
  tdrStyle->SetPadGridX(false);
  tdrStyle->SetPadGridY(false);
  tdrStyle->SetGridColor(0);
  tdrStyle->SetGridStyle(3);
  tdrStyle->SetGridWidth(1);

  // For the frame:
  tdrStyle->SetFrameBorderMode(0);
  tdrStyle->SetFrameBorderSize(1);
  tdrStyle->SetFrameFillColor(0);
  tdrStyle->SetFrameFillStyle(0);
  tdrStyle->SetFrameLineColor(1);
  tdrStyle->SetFrameLineStyle(1);
  tdrStyle->SetFrameLineWidth(1);

  // For the histo:
  tdrStyle->SetHistFillColor(63);
  // tdrStyle->SetHistFillStyle(0);
  tdrStyle->SetHistLineColor(1);
  tdrStyle->SetHistLineStyle(0);
  tdrStyle->SetHistLineWidth(1);


  tdrStyle->SetMarkerStyle(20);

  //For the fit/function:
  tdrStyle->SetOptFit(1);
  tdrStyle->SetFitFormat("5.4g");
  tdrStyle->SetFuncColor(2);
  tdrStyle->SetFuncStyle(1);
  tdrStyle->SetFuncWidth(1);

  //For the date:
  tdrStyle->SetOptDate(0);

  // For the statistics box:
  tdrStyle->SetOptFile(0);
  tdrStyle->SetOptStat(0); // To display the mean and RMS:   SetOptStat("mr");
  tdrStyle->SetStatColor(kWhite);
  tdrStyle->SetStatFont(42);
  tdrStyle->SetStatFontSize(0.025);
  tdrStyle->SetStatTextColor(1);
  tdrStyle->SetStatFormat("6.4g");
  tdrStyle->SetStatBorderSize(1);
  tdrStyle->SetStatH(0.1);
  tdrStyle->SetStatW(0.15);


  // Margins:
  tdrStyle->SetPadTopMargin(0.1);
  tdrStyle->SetPadBottomMargin(0.13);
  tdrStyle->SetPadLeftMargin(0.13);
  tdrStyle->SetPadRightMargin(0.05);

  // For the Global title:

  //  tdrStyle->SetOptTitle(0);
  tdrStyle->SetTitleFont(42);
  tdrStyle->SetTitleColor(1);
  tdrStyle->SetTitleTextColor(1);
  tdrStyle->SetTitleFillColor(10);
  tdrStyle->SetTitleFontSize(0.05);

  // For the axis titles:

  tdrStyle->SetTitleColor(1, "XYZ");
  tdrStyle->SetTitleFont(42, "XYZ");
  tdrStyle->SetTitleSize(0.06, "XYZ");
  tdrStyle->SetTitleXOffset(0.9);
  tdrStyle->SetTitleYOffset(1.05);

  // For the axis labels:

  tdrStyle->SetLabelColor(1, "XYZ");
  tdrStyle->SetLabelFont(42, "XYZ");
  tdrStyle->SetLabelOffset(0.007, "XYZ");
  tdrStyle->SetLabelSize(0.04, "XYZ");

  // For the axis:

  tdrStyle->SetAxisColor(1, "XYZ");
  tdrStyle->SetStripDecimals(kTRUE);
  tdrStyle->SetTickLength(0.03, "XYZ");
  tdrStyle->SetNdivisions(510, "XYZ");
  tdrStyle->SetPadTickX(1);  // To get tick marks on the opposite side of the frame
  tdrStyle->SetPadTickY(1);

  // Change for log plots:
  tdrStyle->SetOptLogx(0);
  tdrStyle->SetOptLogy(0);
  tdrStyle->SetOptLogz(0);
  
  tdrStyle->cd();
}
