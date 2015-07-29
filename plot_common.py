#!/usr/bin/env python

import os , math, copy
import ROOT as r
from numpy import array

def poissonErrGraph(hist):
    alpha = 1 - 0.6827
    g = r.TGraphAsymmErrors(hist)
    g.SetMarkerSize(0.7)
    g.SetMarkerStyle(20)
    seenNonzeroPoint = False
    for i in range(0, g.GetN()):
      N = g.GetY()[i]
      if N > 0:
        seenNonzeroPoint = True
      if not seenNonzeroPoint:
        continue
      L = 0 if N==0 else (r.Math.gamma_quantile(alpha/2,N,1.))
      U = r.Math.gamma_quantile_c(alpha/2,N+1,1)
      g.SetPointEYlow(i, N-L)
      g.SetPointEYhigh(i, U-N)
    return g

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
    


