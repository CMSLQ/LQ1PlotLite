#!/usr/bin/env python

import os , math, copy
import ROOT as r
from numpy import array


def StrToBool(v):
    return v.lower() in ("yes", "true", "t", "1")

# from makeDatacard.py
def GetSystDictFromFile(filename,syst_background_names):
    # go custom text parsing :`(
    # format is like:
    # LQ300  :     0.0152215
    # selection point, 100*(deltaX/X) [rel. change in %]
    systDict = {}
    if not os.path.isfile(filename):
      print "ERROR: file'"+filename+"' not found; cannot proceed"
      exit(-1)
    with open(filename,'r') as thisFile:
        for line in thisFile:
            line = line.strip()
            if len(line)==0:
                continue
            items = line.split(':')
            selectionPoint = items[0].strip()
            if '_' in selectionPoint:
                bkgName = selectionPoint.split('_')[1]
                if not bkgName in syst_background_names:
                    print 'WARN: background named:',bkgName,' was not found in list of systematics background names:',syst_background_names
                    print 'selectionPoint=',selectionPoint,'from',filename
                selectionPoint = selectionPoint.split('_')[0]
                if not bkgName in systDict.keys():
                    systDict[bkgName] = {}
                systDict[bkgName][selectionPoint] = float(items[1].strip())/100.0
            # signal
            systDict[selectionPoint] = float(items[1].strip())/100.0
    return systDict


def FillSystDicts(systNames,syst_background_names,systematics_filepaths,isBackground=True):
    systDict = {}
    for syst in systNames:
        if isBackground:
          filePath = systematics_filepaths[syst]+syst+'_sys.dat'
        else:
          filePath = systematics_filepaths[syst]+'LQ'+syst+'_sys.dat'
        thisSystDict = GetSystDictFromFile(filePath,syst_background_names)
        # this will give the form (for background):
        #   systDict['Trigger'][bkgname]['LQXXXX'] = value
        systDict[syst] = thisSystDict
    return systDict


def GetErrorsGraph(histList,backgroundSyst):
    bgErrsHist = 0
    for hist in histList:
        if not bgErrsHist:
            bgErrsHist = hist.Clone()
        else:
            bgErrsHist.Add(hist)
    bgErrs = r.TGraphAsymmErrors(bgErrsHist)
    #bgErrs.Reset()
    bgErrs.SetName('bgErrs')
    #for binn in range(0,bgErrs.GetNbinsX()):
    #    bgErrs.SetBinContent(binn, zjets_hist.GetBinContent(binn)+ttbar_hist.GetBinContent(binn)+other_hist.GetBinContent(binn)+qcd_hist.GetBinContent(binn))
    for point in range(0,bgErrsHist.GetNbinsX()):
        bgErrs.SetPointEYlow(point, bgErrsHist.GetBinContent(point+1)*backgroundSyst)
        bgErrs.SetPointEYhigh(point, bgErrsHist.GetBinContent(point+1)*backgroundSyst)
    #for binn in range(0,bgErrs.GetNbinsX()):
    #    print 'bin=',bgErrs.GetBinContent(binn),'+/-',bgErrs.GetBinError(binn)
    # set style
    setUncertaintyStyle(bgErrs)
    return bgErrs

def poissonErrGraph(hist,stack,lastPopBin=9999):
    verbose = True
    totBkgHist = stack.GetStack().Last()
    lastPopBinCenter = 9999
    if lastPopBin < 9999:
      lastPopBinCenter = hist.GetBinCenter(lastPopBin)
    alpha = 1 - 0.6827
    g = r.TGraphAsymmErrors(hist)
    g.SetMarkerSize(hist.GetMarkerSize())
    g.SetMarkerStyle(hist.GetMarkerStyle())
    seenNonzeroPoint = False
    i=0
    while i < g.GetN() and g.GetX()[i] <= lastPopBinCenter:
      N = g.GetY()[i]
      if verbose:
          print 'poissonErrGraph(): consider data point x=',g.GetX()[i],'y=',N
      #for n in range(0,g.GetN()):
      #  print g.GetY()[n],
      #print
      # turn off error bars for empty bins at beginning of dist
      if N > 0 or totBkgHist.GetBinContent(totBkgHist.FindBin(g.GetX()[i])) > 0:
        seenNonzeroPoint = True
      if not seenNonzeroPoint:
        if verbose:
          print 'saw zero point; removePoint(',i,') / ',g.GetN(),' and continue'
        g.RemovePoint(i)
        i=0
        continue
      L = 0 if N==0 else (r.Math.gamma_quantile(alpha/2,N,1.))
      U = r.Math.gamma_quantile_c(alpha/2,N+1,1)
      if N==0:
        if verbose:
          print 'set this point to 1e-10'
        g.SetPoint(i,g.GetX()[i],1e-10)
      g.SetPointEYlow(i, N-L)
      g.SetPointEYhigh(i, U-N)
      if verbose:
        print 'current point is',g.GetY()[i],'-',g.GetEYlow()[i],'+',g.GetEYhigh()[i]
      i+=1
    return g


def getLastPopulatedBin(histList,threshold=1e-2):
  n_bins = histList[0].GetNbinsX()
  for bin in reversed(range ( 1, n_bins+1)):
    for hist in histList:
      if hist.GetBinContent(bin) > threshold:
        #print 'found bincontent of:',hist.GetBinContent(bin),'in bin',bin,'with center',hist.GetBinCenter(bin),'in hist:',hist.GetName()
        return bin
    


def rebin ( plot, bins, addOverflow=True ) :
    n_bins    = len ( bins ) - 1
    bin_array = array ( bins, dtype=float ) 
    new_name  = plot.GetName() + "_rebin"
    new_plot  = plot.Rebin ( n_bins, new_name, bin_array ) 
    if addOverflow:
      lastBin = new_plot.GetNbinsX()
      ovflBinContent = new_plot.GetBinContent(lastBin+1)
      lastBinContent = new_plot.GetBinContent(lastBin)
      new_plot.SetBinContent(lastBin, ovflBinContent+lastBinContent)
      ovflBinError = new_plot.GetBinError(lastBin+1)
      lastBinError = new_plot.GetBinError(lastBin)
      new_plot.SetBinError( lastBin, math.sqrt(pow(ovflBinContent,2)+pow(lastBinContent,2)) )
    return new_plot


def makeSafe ( plot ) :
    n_bins = plot.GetNbinsX()
    for i in range ( 1, n_bins + 1 ):
        old_content = plot.GetBinContent(i)
        if old_content > 0. and old_content < 0.0001:
            plot.SetBinContent(i, 0. )
            plot.SetBinError  (i, 0. )
    

def ZeroNegativeBins(plotList):
    verbose=False
    for hist in plotList:
        for binn in range(0,hist.GetNbinsX()+2):
            if hist.GetBinContent(binn) < 0:
                if verbose:
                    print 'INFO: hist',hist.GetName(),'had bin',binn,'with content<0:',hist.GetBinContent(binn),'; set to zero'
                hist.SetBinContent(binn,0)


def setStyle ( plot, color, style, width ) :
    plot.SetLineColor( color ) 
    plot.SetFillColor( color ) 
    plot.SetFillStyle( style ) 
    plot.SetLineWidth( width )

def setStackHistosStyle(plotList):
    setStyle (plotList[0],  r.kRed+1   , 3004, 2)  # Z/W
    setStyle (plotList[1],  4          , 3005, 2)  # ttbar
    setStyle (plotList[2],  r.kGreen+1 , 3006, 2)  # other
    setStyle (plotList[3] , r.kCyan+1  , 3013, 2)  # QCD
    if len(plotList) == 7:
        setStyle (plotList[4] , r.kOrange-6,    0, 4)  # sig1
        setStyle (plotList[5] , r.kAzure-4 ,    0, 4)  # sig2
        setStyle (plotList[6] , 1          ,    0, 2)  # data
        setRatio1MarkerStyle(plotList[6])
        plotList[4].SetLineStyle(2)
        plotList[5].SetLineStyle(2)
    elif len(plotList) == 6:
        setStyle (plotList[4] , r.kAzure-4 ,    0, 4)  # sig
        setStyle (plotList[5] , 1          ,    0, 2)  # data
        setRatio1MarkerStyle(plotList[5])
        plotList[4].SetLineStyle(2)
    
def setStackYAxisStyle(stack):
    stack.GetYaxis().SetTitle( "Events / bin" )
    stack.GetYaxis().CenterTitle()
    stack.GetYaxis().SetTitleFont(42)
    stack.GetYaxis().SetLabelFont(42)
    stack.GetYaxis().SetLabelOffset(0.007)
    stack.GetYaxis().SetLabelSize(0.08)
    stack.GetYaxis().SetTitleOffset(0.65)
    stack.GetYaxis().SetTitleSize(0.1)
    stack.GetYaxis().CenterTitle(1)

def setStackNoRatioXAxisStyle(stack):
    stack.GetXaxis().SetTitle( x_labels [i_var] )
    stack.GetXaxis().CenterTitle()
    stack.GetXaxis().SetTitleFont(42)
    stack.GetXaxis().SetLabelFont(42)
    stack.GetXaxis().SetLabelOffset(0.007)
    stack.GetXaxis().SetTitleOffset(0.92)
    stack.GetXaxis().SetLabelSize(0.05)
    stack.GetXaxis().SetTitleSize(0.06)
    stack.GetXaxis().CenterTitle(1)
    stack.GetXaxis().SetNdivisions(507)

def setStackWithRatioXAxisStyle(stack):
    stack.GetXaxis().SetLabelSize(0)
    stack.GetXaxis().SetLabelOffset(0)
    stack.GetXaxis().SetTitleSize(0)
    stack.GetXaxis().SetTitleOffset(0)
    stack.GetXaxis().SetNdivisions(507)

def setBkgUncHistStyle(bkgUncHisto):
    bkgUncHisto.SetMarkerStyle(0)
    bkgUncHisto.SetLineColor(0)
    setUncertaintyStyle(bkgUncHisto)

def setUncertaintyStyle(hist):
    hist.SetFillColor(r.kGray+1)
    hist.SetLineColor(r.kGray+1)
    hist.SetFillStyle(3001)
    hist.SetMarkerSize(0)

def setRatio1MarkerStyle(h_ratio1):
    h_ratio1.SetMarkerStyle ( 20 )
    h_ratio1.SetMarkerSize ( 1.175 )
    h_ratio1.SetLineWidth ( 2 )

def setBGRatioErrStyle(bgRatioErrs,label):
    setUncertaintyStyle(bgRatioErrs)
    bgRatioErrs.GetYaxis().SetRangeUser(0.,2)
    bgRatioErrs.SetMarkerStyle ( 1 )
    bgRatioErrs.GetXaxis().SetTitle( label )
    bgRatioErrs.GetXaxis().SetTitleFont(42)
    bgRatioErrs.GetXaxis().SetLabelFont(42)
    bgRatioErrs.GetXaxis().SetLabelOffset(0.025)
    bgRatioErrs.GetXaxis().SetTitleOffset(0.9)
    bgRatioErrs.GetXaxis().SetLabelSize(0.18)
    bgRatioErrs.GetXaxis().SetTitleSize(0.25)
    bgRatioErrs.GetXaxis().SetNdivisions(507)
    #
    bgRatioErrs.GetYaxis().SetTitle( "data / bkg." )
    bgRatioErrs.GetYaxis().SetTitleFont(42)
    bgRatioErrs.GetYaxis().SetLabelFont(42)
    bgRatioErrs.GetYaxis().SetLabelOffset(0.01)
    bgRatioErrs.GetYaxis().SetLabelSize(0.17)
    #bgRatioErrs.GetYaxis().SetTitleOffset(0.2)
    #bgRatioErrs.GetYaxis().SetTitleSize(0.175)
    bgRatioErrs.GetYaxis().SetTitleOffset(0.4)
    bgRatioErrs.GetYaxis().SetTitleSize(0.16)
    #bgRatioErrs.GetYaxis().CenterTitle()
    #bgRatioErrs.GetYaxis().CenterTitle(1)
    bgRatioErrs.GetYaxis().SetRangeUser(0.,2)
    bgRatioErrs.GetYaxis().SetNdivisions(502)

def setRatio1NoBGErrStyle(h_ratio1,label):
    h_ratio1.GetYaxis().SetTitle( "data / bkg." )
    h_ratio1.GetYaxis().SetTitleFont(42)
    h_ratio1.GetYaxis().SetLabelFont(42)
    h_ratio1.GetYaxis().SetLabelOffset(0.007)
    h_ratio1.GetYaxis().SetLabelSize(0.12)
    h_ratio1.GetYaxis().SetTitleOffset(0.3)
    h_ratio1.GetYaxis().SetTitleSize(0.12)
    h_ratio1.GetYaxis().CenterTitle()
    h_ratio1.GetYaxis().CenterTitle(1)
    h_ratio1.GetXaxis().SetTitle(label)
    h_ratio1.GetXaxis().SetTitleFont(42)
    h_ratio1.GetXaxis().SetLabelFont(42)
    h_ratio1.GetXaxis().SetLabelOffset(0.025)
    h_ratio1.GetXaxis().SetTitleOffset(1.1)
    h_ratio1.GetXaxis().SetLabelSize(0.15)
    h_ratio1.GetXaxis().SetTitleSize(0.15)

def setLegendStyle(leg):
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(.0625)

def drawLumiEnergyAndCMSStrings(l1,l2,drawCMS=True):
    lumiEnergyString = "35.9 fb^{-1} (13 TeV)"
    l1.SetTextAlign(12)
    l1.SetTextFont(42)
    l1.SetNDC()
    l1.SetTextSize(0.06)
    l1.DrawLatex(0.7375,0.965,lumiEnergyString)
    #
    l2.SetTextAlign(12)
    l2.SetTextFont(62)
    l2.SetNDC()
    l2.SetTextSize(0.08)
    if not drawCMS:
        return
    l2.DrawLatex(0.175,0.84,"CMS")

def drawPrelim(l3):
    l3.SetTextAlign(12)
    l3.SetTextFont(42)
    l3.SetNDC()
    l3.SetTextSize(0.08)
    l3.DrawLatex(0.25,0.83,"#it{Preliminary}")

