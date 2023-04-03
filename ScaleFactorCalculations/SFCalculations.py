from uncertainties import ufloat
import ROOT

def isFloat( myFloat ):
    try:
        float(myFloat)
        return True
    except:
        return False
    
def get(filename, flag1, etabin, ptbin):
    file = ROOT.TFile(filename, "READ")
    if flag1 == 'data':
        hist = file.Get("EGamma_EffData2D")
    if flag1 == 'mc':
        hist = file.Get("EGamma_EffMC2D")
    nbins_x = hist.GetNbinsX()
    nbins_y = hist.GetNbinsY()
    for i in range(1, nbins_x+1):
        for j in range(1, nbins_y+1):
            x_low = hist.GetXaxis().GetBinLowEdge(i)
            x_up = hist.GetXaxis().GetBinUpEdge(i)
            y_low = hist.GetYaxis().GetBinLowEdge(j)
            y_up = hist.GetYaxis().GetBinUpEdge(j)
            val = [hist.GetBinContent(i, j), hist.GetBinError(i, j)]
            print(filename,etabin,ptbin,val)
            if (x_low, x_up) == etabin and (y_low, y_up) == ptbin:
                return val
            else:
                continue


ptbins = [(10.0, 20.0), (20.0, 35.0), (35.0, 50.0), (50.0, 100.0), (100.0, 200.0), (200.0, 500)]
etabins = [(-2.5, -2.1), (-2.1, -1.566), (-1.566, -1.444), (-1.444, -0.8), (-0.8, 0.0), 
           (0.0, 0.8), (0.8, 1.444), (1.444, 1.566), (1.566, 2.1), (2.1, 2.5)]

# print(get("LX.root", 'data', 'value', etabins[0], ptbins[0]))

SFFilename = 'CrossTrigger_systCombined_SFs.txt'
fOut = open( SFFilename,'w')

fOut.write("### var1 : el_sc_eta" + '\n')
fOut.write("### var2 : el_pt" + '\n')
# fOut.write('### var1[0]\t var1[1]\t var2[0]\t var2[1]\t, effDataSLF, err_effDataSLF, effMCSLF, err_effMCSLF')

for ptbin in ptbins:
    for etabin in etabins:
        SLF_D = get("SLF.root", 'data', etabin, ptbin)
        SLF_M = get("SLF.root", 'mc', etabin, ptbin)
        LX_D = get("LX.root", 'data', etabin, ptbin)
        LX_M = get("LX.root", 'mc', etabin, ptbin)
        JX_D = get("JX.root", 'data', etabin, ptbin)
        JX_M = get("JX.root", 'mc', etabin, ptbin)
        SLFandLX_D = get("SLFandLX.root", 'data', etabin, ptbin)
        SLFandLX_M = get("SLFandLX.root", 'mc', etabin, ptbin)
        eD_SLF = ufloat(SLF_D[0], SLF_D[1])
        eM_SLF = ufloat(SLF_M[0], SLF_M[1])
        eD_LX = ufloat(LX_D[0], LX_D[1])
        eM_LX = ufloat(LX_M[0], LX_M[1])
        eD_JX = ufloat(JX_D[0], JX_D[1])
        eM_JX = ufloat(JX_M[0], JX_M[1])
        eD_SLFandLX = ufloat(SLFandLX_D[0], SLFandLX_D[1])
        eM_SLFandLX = ufloat(SLFandLX_M[0], SLFandLX_M[1])
        sf1 = ((eD_LX*(1.0 - eD_SLFandLX))*eD_JX)/((eM_LX*(1.0 - eM_SLFandLX))*eM_JX)
        sf2 = ((eD_LX - eD_SLFandLX*eD_SLF)*eD_JX)/((eM_LX - eM_SLFandLX*eM_SLF)*eM_JX)
        sf3 = eD_SLFandLX*eD_SLF*eD_JX/(eM_SLFandLX*eM_SLF*eM_JX)
        astr =  '%+8.5f\t%+8.5f\t%+8.5f\t%+8.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f' % (
            float(etabin[0]), float(etabin[1]),
            float(ptbin[0]), float(ptbin[1]),
            eD_SLF.nominal_value, eD_SLF.std_dev,
            eM_SLF.nominal_value, eM_SLF.std_dev,
            eD_LX.nominal_value, eD_LX.std_dev,
            eM_LX.nominal_value, eM_LX.std_dev,
            eD_JX.nominal_value, eD_JX.std_dev,
            eM_JX.nominal_value, eM_JX.std_dev,
            eD_SLFandLX.nominal_value, eD_SLFandLX.std_dev,
            eM_SLFandLX.nominal_value, eM_SLFandLX.std_dev,
            sf1.nominal_value, sf1.std_dev, 
            sf2.nominal_value, sf2.std_dev,
            sf3.nominal_value, sf3.std_dev
            )
        print(astr)
        fOut.write(astr + '\n')

fOut.close()
        

