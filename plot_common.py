#!/usr/bin/env python

import os , math, copy
import ROOT as r
from numpy import array

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
    

