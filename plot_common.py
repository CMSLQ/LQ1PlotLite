#!/usr/bin/env python

import os , math, copy
import ROOT as r
from numpy import array


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
    bgErrs.SetFillColor(r.kGray+2)
    bgErrs.SetLineColor(r.kGray+2)
    bgErrs.SetFillStyle(3001)
    bgErrs.SetMarkerSize(0)
    return bgErrs

def poissonErrGraph(hist,lastPopBin=9999):
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
      #print 'poissonErrGraph(): consider data point x=',g.GetX()[i],'y=',N
      #for n in range(0,g.GetN()):
      #  print g.GetY()[n],
      #print
      # turn off error bars for empty bins at beginning of dist
      if N > 0:
        seenNonzeroPoint = True
      if not seenNonzeroPoint:
        #print 'removePoint(',i,') / ',g.GetN()
        g.RemovePoint(i)
        i=0
        continue
      L = 0 if N==0 else (r.Math.gamma_quantile(alpha/2,N,1.))
      U = r.Math.gamma_quantile_c(alpha/2,N+1,1)
      if N==0:
        #print 'set this point to 1e-10'
        g.SetPoint(i,g.GetX()[i],1e-10)
      g.SetPointEYlow(i, N-L)
      g.SetPointEYhigh(i, U-N)
      #print 'point is',g.GetY()[i],'-',g.GetEYlow()[i],'+',g.GetEYhigh()[i]
      i+=1
    return g


def getLastPopulatedBin(histList,threshold=1e-2):
  n_bins = histList[0].GetNbinsX()
  for bin in reversed(range ( 1, n_bins+1)):
    for hist in histList:
      if hist.GetBinContent(bin) > threshold:
        #print 'found bincontent of:',hist.GetBinContent(bin),'in bin',bin,'with center',hist.GetBinCenter(bin),'in hist:',hist.GetName()
        return bin
    

def setStyle ( plot, color, style, width ) :
    plot.SetLineColor( color ) 
    plot.SetFillColor( color ) 
    plot.SetFillStyle( style ) 
    plot.SetLineWidth( width )
    return


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
    

