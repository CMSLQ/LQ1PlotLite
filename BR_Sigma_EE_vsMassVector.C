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
//void makePlotsBOVector()
void BR_Sigma_EE_vsMassVector()
{

 // filename for the final plot (NB: changing the name extension changes the file format)
 string fileNamePdf = "BR_Sigma_EEVector.pdf";
 string fileNamePng = "BR_Sigma_EEVector.png";
 string fileNameEps = "BR_Sigma_EEVector.eps";

 // axes labels for the final plot
 string title = ";M_{LQ} [GeV];#sigma#times#beta^{2} [pb]";

 // integrated luminosity
 string lint = "19.7 fb^{-1}";

bool NoteStyle = false;

Double_t mTh[16] = {300.0 , 400.0 , 500.0 , 600.0 , 700.0 , 800.0 , 900.0 , 1000.0 , 1100.0 , 1200.0 , 1300.0 , 1400.0 , 1500.0 , 1600.0 , 1700.0 , 1800.0 }; 
Double_t mData[16] = {300.0 , 400.0 , 500.0 , 600.0 , 700.0 , 800.0 , 900.0 , 1000.0 , 1100.0 , 1200.0 , 1300.0 , 1400.0 , 1500.0 , 1600.0 , 1700.0 , 1800.0 }; 
Double_t MCx_shademasses[32] = {300.0 , 400.0 , 500.0 , 600.0 , 700.0 , 800.0 , 900.0 , 1000.0 , 1100.0 , 1200.0 , 1300.0 , 1400.0 , 1500.0 , 1600.0 , 1700.0 , 1800.0 , 1800.0 , 1700.0 , 1600.0 , 1500.0 , 1400.0 , 1300.0 , 1200.0 , 1100.0 , 1000.0 , 900.0 , 800.0 , 700.0 , 600.0 , 500.0 , 400.0 , 300.0 }; 


Double_t YMxsTh[16] = {104.6,17.74,4.03,1.125,0.3519,0.1194,0.04373,0.01731,0.006853,0.002832,0.001203,0.0005089,0.0002236,9.675E-05,4.159E-05,1.794E-05};
Double_t MCxsTh[16] = {21.19,3.354,0.7378,0.2034,0.06362,0.02177,0.008059,0.003231,0.001298,0.0005442,0.0002344,0.0001006,4.478E-05,1.96E-05,8.518E-06,3.711E-06};
Double_t MMxsTh[16] = {2510,242.9,40.14,9.204,2.528,0.7827,0.2678,0.1006,0.03822,0.01528,0.006316,0.002614,0.001128,0.0004799,0.0002037,8.697E-05};
Double_t AMxsTh[16] = {20.06,2.956,0.5897,0.1458,0.04056,0.01228,0.004027,0.001431,0.0005108,0.0001909,7.373E-05,2.849E-05,1.148E-05,4.578E-06,1.829E-06,7.371E-07};




// Insert limit information below
/*
Double_t MCxsUp_expected[16] = {0.01503839467 , 0.005022604938 , 0.0026718512128 , 0.0014719260672 , 0.000933003205 , 0.00056899140907 , 0.000338587876406 , 0.00024399135594 , 0.000232718338226 , 0.000229119960162 , 0.000224006546952 , 0.000221992709584 , 0.000222843742615 , 0.00021687167397 , 0.0002195750371 , 0.000219359066747 }; 
Double_t MCxsUp_observed[16] = {0.0224917017 , 0.005349569628 , 0.0021869255226 , 0.0014595127686 , 0.0006520964113 , 0.00083868485246 , 0.000501884629169 , 0.000195036287553 , 0.00018691863278 , 0.000182725857679 , 0.000179993854562 , 0.000177461132296 , 0.000178983363726 , 0.000174174610826 , 0.000175495107237 , 0.000175687111222 }; 
Double_t MCy_1sigma[32]={0.01088617179 , 0.003596775936 , 0.0019069591968 , 0.0010380362382 , 0.00065458000886 , 0.00038867248014 , 0.000218816855858 , 0.000146781635346 , 0.000139999957878 , 0.000137244373154 , 0.00013475906808 , 0.000133547565857 , 0.000134059542054 , 0.00013046682721 , 0.000131575486944 , 0.000131963207564 , 0.000378495244514 , 0.000378867898614 , 0.000377661204519 , 0.000388060976753 , 0.000383039501329 , 0.000390085897146 , 0.000395337282821 , 0.000405256656156 , 0.000420997277394 , 0.000541031769681 , 0.00085703049677 , 0.00135324912306 , 0.0020997122346 , 0.0037688122528 , 0.007084694448 , 0.0209728025 }; 
Double_t MCy_2sigma[32]={0.00813600645 , 0.002697685926 , 0.0014246394162 , 0.0007733361564 , 0.0004847242791 , 0.0002822730855 , 0.00015276132683 , 9.673875711e-05 , 9.2269189276e-05 , 8.99474842308e-05 , 8.8815094084e-05 , 8.80166412466e-05 , 8.8354059733e-05 , 8.59862297056e-05 , 8.70580727119e-05 , 8.69724430043e-05 , 0.000628716707198 , 0.000624822776581 , 0.000622046685798 , 0.000639176189857 , 0.00063170249431 , 0.000642511398021 , 0.000651983817184 , 0.000667499182966 , 0.000694301848524 , 0.000842567700513 , 0.00124928348881 , 0.00190390668898 , 0.0028886849694 , 0.0051130144996 , 0.0096115578 , 0.02803235695 }; 

Double_t YMxsUp_observed[16] = {0.0246214802 , 0.00560520136 , 0.00226700799 , 0.001502821125 , 0.0006680832057 , 0.0008444280828 , 0.00050466505921 , 0.00019354260801 , 0.000185063366719 , 0.000181115224512 , 0.000179223347817 , 0.000180467267605 , 0.000176141854772 , 0.000175374453487 , 0.000175860340192 , 0.000173710210793 }; 
Double_t MMxsUp_observed[16] = {0.02081292 , 0.0050144276 , 0.00210080718 , 0.001408773444 , 0.00064701632 , 0.0008187018519 , 0.0004965724348 , 0.0001923861322 , 0.00018532579884 , 0.00018327907712 , 0.00017911174914 , 0.000177300854968 , 0.000176156230488 , 0.000175184522979 , 0.000175274344543 , 0.000175298392083 }; 
Double_t AMxsUp_observed[16] = {0.0221659991 , 0.00519256872 , 0.0021462951183 , 0.0014349675366 , 0.0006444718332 , 0.0008197058412 , 0.000498776915022 , 0.000193865896989 , 0.00018776264786 , 0.000182337121321 , 0.000179475959276 , 0.000178213586259 , 0.000178298192531 , 0.000176073975401 , 0.00017971543089 , 0.00017788406583 }; 
*/

 Double_t YMxsUp_expected[16] = {0.012739234 , 0.00543058654, 0.00543058654 , 0.001512082125 , 0.0009074026539 , 0.0005441653806 , 0.00038900686196 , 0.00027707999292 , 0.000265810860854 , 0.000258692492208 , 0.000256310274141 , 0.000249405897194 , 0.000251404062764 , 0.000252960975974 , 0.000255974976192 , 0.000252886443737 }; 
Double_t YMxsUp_observed[16] = {0.0119715746 , 0.00587254316 , 0.00587254316 , 0.002958696 , 0.0012291289884 , 0.0007953405936 , 0.00050213252372 , 0.00032920263591 , 0.000314860790321 , 0.000306946045296 , 0.000303393538365 , 0.000297300069051 , 0.000299364813613 , 0.000301264978405 , 0.000302950175327 , 0.000300512199024 }; 

/*
Double_t YMy_1sigma[32]={0.0127654886 , 0.00415091164 , 0.00210098005 , 0.001137835125 , 0.0007184728224 , 0.0004332382434 , 0.00022915827527 , 0.00014442911811 , 0.000138370142834 , 0.00013529027568 , 0.000133869349176 , 0.000134629783546 , 0.000131525765493 , 0.000130842987718 , 0.000131165560767 , 0.000129897888649 , 0.000372571514972 , 0.000379683823854 , 0.000378750042166 , 0.000380726496441 , 0.000389711646 , 0.000385615405227 , 0.000389708407632 , 0.000396871545917 , 0.00041807771511 , 0.0005601786762 , 0.0009241538508 , 0.0014488898346 , 0.00226908225 , 0.00411758399 , 0.00812999364 , 0.024635915 }; 
Double_t YMy_2sigma[32]={0.0096120078 , 0.00311331678 , 0.00156787956 , 0.0008466615 , 0.0005346145737 , 0.0003170856846 , 0.00016073980409 , 9.518829585e-05 , 9.1195029695e-05 , 8.8666796304e-05 , 8.7735552702e-05 , 8.87298890093e-05 , 8.66841405092e-05 , 8.62341421702e-05 , 8.64467400347e-05 , 8.56112596349e-05 , 0.000618876757058 , 0.000625378148191 , 0.000623840120325 , 0.000627095552294 , 0.000641894966723 , 0.00063595058769 , 0.00064270076352 , 0.000659241419529 , 0.00068861684757 , 0.00086128762594 , 0.0013268994834 , 0.002000291094 , 0.003110448375 , 0.00554899969 , 0.0109120514 , 0.033016467 }; 
*/
 Double_t AMxsUp_expected[16] = {0.01163433862 , 0.005115029884 , 0.0026596006627 , 0.001470838419 , 0.00089429190552 , 0.00054019405632 , 0.000397589753108 , 0.000275228819217 , 0.000263984142643 , 0.000260475821953 , 0.000259653791402 , 0.000254886459244 , 0.00025289499245 , 0.000246955755363 , 0.000252875520554 , 0.000247402009369 }; 
Double_t AMxsUp_observed[16] = {0.01092339216 , 0.00552780868 , 0.0047383373902 , 0.0028899195876 , 0.00121277364936 , 0.00079185892728 , 0.000511672114017 , 0.000326539364823 , 0.000312682167313 , 0.000309962070889 , 0.000309140948099 , 0.000301778278193 , 0.000300282862503 , 0.000293299037606 , 0.000299510445167 , 0.000294453065477 }; 

/*
Double_t AMy_1sigma[32]={0.01157259394 , 0.003846743304 , 0.0019870737595 , 0.0010868819922 , 0.00069332233776 , 0.00042054080632 , 0.000226248546354 , 0.000144398010015 , 0.000139915610882 , 0.000136035873375 , 0.000134290049973 , 0.000133321973829 , 0.000133157526968 , 0.000131295530789 , 0.000134360947753 , 0.000132736935608 , 0.000384232450342 , 0.000385372415451 , 0.000380060026109 , 0.000383564928435 , 0.000382392451995 , 0.000385169069215 , 0.000393781816165 , 0.000405012511404 , 0.000417987654507 , 0.000555081869269 , 0.00089874442796 , 0.00139817085408 , 0.002163827277 , 0.003904150129 , 0.007509123844 , 0.02222310992 }; 
Double_t AMy_2sigma[32]={0.0086832719 , 0.002896463204 , 0.0014866095223 , 0.0008103667518 , 0.00051589995912 , 0.00030907749356 , 0.000159442315748 , 9.5167790676e-05 , 9.22135956428e-05 , 8.96565946714e-05 , 8.85059838528e-05 , 8.78679586847e-05 , 8.72690303612e-05 , 8.65323974538e-05 , 8.85527111742e-05 , 8.74823799062e-05 , 0.000632870217938 , 0.00064014034372 , 0.000625997770935 , 0.000632569046789 , 0.000635190312245 , 0.000639802535001 , 0.000648599005899 , 0.000667097063934 , 0.000688468504446 , 0.000856616384696 , 0.00129371010808 , 0.00193026982824 , 0.0029661649686 , 0.0052613700361 , 0.010147235604 , 0.02970350398 }; 
*/
 Double_t MMxsUp_expected[16] = {0.01113687 , 0.004986737 , 0.00258003864 , 0.001437876492 , 0.000875967168 , 0.0005432235426 , 0.0003825105232 , 0.000273190366 , 0.0002629117491 , 0.00025602951024 , 0.000254551202652 , 0.00025345951755 , 0.000252381271536 , 0.000251675604977 , 0.000253394389634 , 0.000251425794002 }; 
Double_t MMxsUp_observed[16] = {0.010542 , 0.0053707619 , 0.0046239273 , 0.002817031464 , 0.00118199168 , 0.0007962461889 , 0.0004945253716 , 0.0003236790916 , 0.00031321947384 , 0.0003047749564 , 0.000302937270204 , 0.000300068219746 , 0.000299539984896 , 0.000299820730732 , 0.000299878974889 , 0.000298364562905 }; 

/*
Double_t MMy_1sigma[32]={0.011295 , 0.0036595314 , 0.001950804 , 0.001068372708 , 0.000695581728 , 0.0004210659882 , 0.000225242563 , 0.0001434452382 , 0.00013841652006 , 0.0001368430196 , 0.000133728282724 , 0.000132365604204 , 0.000131510007408 , 0.000130986198962 , 0.000130900679574 , 0.000130605683178 , 0.000378063120876 , 0.000377064012536 , 0.000375693017672 , 0.000380680845432 , 0.000383157537368 , 0.00038710208192 , 0.00039611827688 , 0.00039871367718 , 0.0004152298198 , 0.0005526138696 , 0.000898109115 , 0.001402729056 , 0.002123418024 , 0.00381755484 , 0.0072843281 , 0.02050419 }; 
Double_t MMy_2sigma[32]={0.00874484 , 0.0028482454 , 0.00145660032 , 0.000798152472 , 0.00051758272 , 0.0003073185453 , 0.0001587333618 , 9.4539856e-05 , 9.071570508e-05 , 9.018854976e-05 , 8.8135744076e-05 , 8.7237641518e-05 , 8.6673753552e-05 , 8.63285276224e-05 , 8.57899363398e-05 , 8.60777408517e-05 , 0.000622708711762 , 0.000621847820044 , 0.00062406191153 , 0.000627020347056 , 0.00063109973217 , 0.000637596827256 , 0.00065244741264 , 0.00065755209156 , 0.000683926082 , 0.000852807761 , 0.0012874561857 , 0.00193656176 , 0.002910765 , 0.00515875266 , 0.0097568072 , 0.02803168 }; 
*/

 Double_t MCxsUp_expected[16] = {0.01191939619 , 0.005145046062 , 0.0026756029258 , 0.0014707390248 , 0.00089679031928 , 0.0005362360276 , 0.000386385547518 , 0.000270789392718 , 0.000260969880644 , 0.000260479418225 , 0.000251397294961 , 0.000246156570036 , 0.000249181271525 , 0.00025389498864 , 0.00024725382553 , 0.000252553635016 }; 
Double_t MCxsUp_observed[16] = {0.01120503891 , 0.005568223596 , 0.0047683438516 , 0.0028783087218 , 0.0012134255324 , 0.00078156881922 , 0.000499454195949 , 0.000320804384193 , 0.00031078088635 , 0.000309368421934 , 0.000299468732581 , 0.000293215066312 , 0.000296894773277 , 0.000300674696641 , 0.000294307129053 , 0.000300786536542 }; 
Double_t MCy_1sigma[32]={0.00854997429 , 0.003684459558 , 0.0019096374108 , 0.0010426524012 , 0.00063026145472 , 0.00036351970515 , 0.000255207487951 , 0.000166394406312 , 0.000161551174972 , 0.000161247559828 , 0.000155625345532 , 0.000152381116094 , 0.000154253527316 , 0.000156013159568 , 0.000153060363249 , 0.000156341163849 , 0.000425704237013 , 0.000414799766792 , 0.000425941150656 , 0.000422006283395 , 0.000416883719111 , 0.000425759281902 , 0.000436987363163 , 0.000439890652784 , 0.000454283688825 , 0.000609707174842 , 0.00080769340701 , 0.00130072515088 , 0.0020980187262 , 0.0037741044922 , 0.007175376546 , 0.01662300406 }; 
Double_t MCy_2sigma[32]={0.00642529537 , 0.002763451158 , 0.001426639592 , 0.000772712532 , 0.00046766215854 , 0.00026497601501 , 0.000180363571069 , 0.000112652617887 , 0.000108567545746 , 0.000108363504466 , 0.00010458520355 , 0.000102404984314 , 0.000103663300374 , 0.000105624286653 , 0.000102861452694 , 0.000105066257711 , 0.000685084088242 , 0.000670230295884 , 0.000688232499702 , 0.000676417253495 , 0.000668206518548 , 0.000682432793349 , 0.000706080888904 , 0.00070791422108 , 0.000734028127605 , 0.000923235864754 , 0.00118379451764 , 0.00181886710738 , 0.0028863550224 , 0.0051201947692 , 0.009656806614 , 0.02237168154 }; 


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


 TLegend *legend = new TLegend(.5,.57,.92,.88);
 legend->SetBorderSize(1);
 legend->SetFillColor(0);
 //legend->SetFillStyle(0);
 legend->SetTextFont(42);
 legend->SetTextSize(.035);
 legend->SetMargin(0.15);
 legend->SetHeader("LQ #bar{LQ} #rightarrow eejj");
legend->AddEntry(MMxsTh_vs_m,"MM, #sigma_{theory}#times#beta^{2}, (#beta=1)","lf");
legend->AddEntry(MCxsTh_vs_m,"MC, #sigma_{theory}#times#beta^{2}, (#beta=1)","lf");
legend->AddEntry(YMxsTh_vs_m,"YM, #sigma_{theory}#times#beta^{2}, (#beta=1)","lf");
legend->AddEntry(AMxsTh_vs_m,"AM, #sigma_{theory}#times#beta^{2}, (#beta=1)","lf");

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
