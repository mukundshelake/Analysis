import os, ROOT
import numpy as np


def isFloat( myFloat ):
    try:
        float(myFloat)
        return True
    except:
        return False

def getSFs(etabin, ptbin):
    fileWithSFs = open("CrossTrigger_systCombined_SFs.txt", 'r')
    for line in fileWithSFs :
        modifiedLine = line.lstrip(' ').rstrip(' ').rstrip('\n')
        numbers = modifiedLine.split('\t')

        if len(numbers) > 0 and isFloat(numbers[0]):
            etaKey = ( float(numbers[0]), float(numbers[1]))
            ptKey  = ( float(numbers[2]), float(numbers[3]))
            if (etaKey == etabin ) and (ptKey == ptbin):
                return [float(numbers[-6]),float(numbers[-5]),float(numbers[-4] ),float(numbers[-3]),float(numbers[-2]),float(numbers[-1])]

ptbins = [(10.0, 20.0), (20.0, 35.0), (35.0, 50.0), (50.0, 100.0), (100.0, 200.0), (200.0, 500)]
etabins = [(-2.1, -1.566), (-1.566, -1.444), (-1.444, -0.8), (-0.8, 0.0), 
           (0.0, 0.8), (0.8, 1.444), (1.444, 1.566), (1.566, 2.1)]

xbins = []
ybins = []
for ptBin in ptbins:
    if not ptBin[0] in ybins:
         ybins.append(ptBin[0])                
    if not ptBin[1] in ybins:
         ybins.append(ptBin[1])

for etaBin in etabins:
    if not etaBin[0] in xbins:
        xbins.append(etaBin[0])                
    if not etaBin[1] in xbins:
        xbins.append(etaBin[1])

xbins.sort()
ybins.sort()
## transform to numpy array for ROOT
xbinsTab = np.array(xbins)
ybinsTab = np.array(ybins)
htitle = 'e/#gamma scale factors'
hname  = 'h2_scaleFactorsEGamma' 

herrtitle = 'e/#gamma uncertainties'
herrname  = 'h2_uncertaintiesEGamma'

h2 = ROOT.TH2F(hname,htitle,xbinsTab.size-1,xbinsTab,ybinsTab.size-1,ybinsTab)
h2err  = ROOT.TH2F(herrname,herrtitle,xbinsTab.size-1,xbinsTab,ybinsTab.size-1,ybinsTab)

for ix in range(1,h2.GetXaxis().GetNbins()+1):
       for iy in range(1,h2.GetYaxis().GetNbins()+1):
                h2.SetBinContent(ix,iy, 1)
                h2.SetBinError  (ix,iy, 1)
                h2.SetBinContent(ix,iy, 1)
                h2.SetBinError  (ix,iy, 1)


for ix in range(1,h2.GetXaxis().GetNbins()+1):
       for iy in range(1,h2.GetYaxis().GetNbins()+1):
              for ptBin in ptbins:
                if h2.GetYaxis().GetBinLowEdge(iy) < ptBin[0] or h2.GetYaxis().GetBinUpEdge(iy) > ptBin[1]:
                    continue
                for etaBin in etabins:
                    if h2.GetXaxis().GetBinLowEdge(ix) < etaBin[0] or h2.GetXaxis().GetBinUpEdge(ix) > etaBin[1]:
                        continue

                    ## For Plotting SF1
                    # h2.SetBinContent(ix,iy, getSFs(etaBin, ptBin)[0])
                    # h2.SetBinError(ix,iy, getSFs(etaBin, ptBin)[1])
                    # h2err.SetBinContent(ix,iy, getSFs(etaBin, ptBin)[1])
                    ## For Plotting SF2
                    # h2.SetBinContent(ix,iy, getSFs(etaBin, ptBin)[2])
                    # h2.SetBinError(ix,iy, getSFs(etaBin, ptBin)[3])
                    # h2err.SetBinContent(ix,iy, getSFs(etaBin, ptBin)[3])
                    ## For Plotting SF3
                    h2.SetBinContent(ix,iy, getSFs(etaBin, ptBin)[4])
                    h2.SetBinError(ix,iy, getSFs(etaBin, ptBin)[5])
                    h2err.SetBinContent(ix,iy, getSFs(etaBin, ptBin)[5])
h2.GetXaxis().SetTitle("SuperCluster #eta")
h2.GetYaxis().SetTitle("p_{T} [GeV]")
h2err.GetXaxis().SetTitle("SuperCluster #eta")
h2err.GetYaxis().SetTitle("p_{T} [GeV]")

ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetPaintTextFormat('1.3f')
ROOT.gStyle.SetOptTitle(1)
ROOT.gStyle.SetOptStat(0)

c2D = ROOT.TCanvas('canScaleFactor','canScaleFactor',900,600)
c2D.Divide(2,1)
c2D.GetPad(1).SetRightMargin(0.15)
c2D.GetPad(1).SetLeftMargin( 0.15)
c2D.GetPad(1).SetTopMargin(  0.10)
c2D.GetPad(2).SetRightMargin(0.15)
c2D.GetPad(2).SetLeftMargin( 0.15)
c2D.GetPad(2).SetTopMargin(  0.10)
c2D.GetPad(1).SetLogy()
c2D.GetPad(2).SetLogy()

c2D.cd(1)
h2.SetMinimum(0.0)
h2.SetMaximum(h2.GetMaximum())
h2.DrawCopy("colz TEXT45")


c2D.cd(2)
h2err.SetMinimum(0)
h2err.SetMaximum(h2err.GetMaximum())    
h2err.DrawCopy("colz TEXT45")

# c2D.Print('sf1.png')
# c2D.Print('sf2.png')
c2D.Print('sf3.png')

