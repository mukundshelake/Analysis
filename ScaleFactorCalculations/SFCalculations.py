"""
The script calculates the cross triggers as per the formula given in slide 19 of the https://mattermost.web.cern.ch/files/hri6ynr3n7y8zgbhuo9n8byoee/public?h=xPH1ebP7lefEXXBrVqKQ8gG4-O2wPOm6NvMD-G_nJUU.
With the normal error propagation formula using 'uncertainities' python module.

input: Root files for the 4 trigger bits, containing their efficiencies. These are the outputs of the module https://github.com/mukundshelake/egm_tnp_analysis.
       Place the ROOT fies in the input folder.Provide the ROOT file names in line 74 onwards.
output: Text file "outputs/CrossTrigger_systCombined_SFs.txt" containing the bin boundaries and different values (error) used in the formula and the calculated scale factors (erros); bin by bin.

Note: We can choose which bins to plot; PROVIDED THAT THE CORRESPONDING BINS ARE ALREADY PRESENT IN THE ROOT FILE.
      You can't play with the bin boundaries, you can simply omit or add bins (provided they are in root files)

Import: uncertainties  

Infra: python 3.10.10 and ROOT 6.26/10
"""





from uncertainties import ufloat
import ROOT, os

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

# Input and Output folders
inputF = "inputs"
outputF = "outputs"



SFFilename = 'CrossTrigger_systCombined_SFs.txt'
fOut = open( SFFilename,'w')

fOut.write("### var1 : el_sc_eta" + '\n')
fOut.write("### var2 : el_pt" + '\n')
# fOut.write('### var1[0]\t var1[1]\t var2[0]\t var2[1]\t, effDataSLF, err_effDataSLF, effMCSLF, err_effMCSLF')

for ptbin in ptbins:
    for etabin in etabins:
        SLF_D = get(os.path.join(inputF, "SLF.root"), 'data', etabin, ptbin)
        SLF_M = get(os.path.join(inputF, "SLF.root"), 'mc', etabin, ptbin)
        LX_D = get(os.path.join(inputF, "LX.root"), 'data', etabin, ptbin)
        LX_M = get(os.path.join(inputF, "LX.root"), 'mc', etabin, ptbin)
        JX_D = get(os.path.join(inputF, "JX.root"), 'data', etabin, ptbin)
        JX_M = get(os.path.join(inputF, "JX.root"), 'mc', etabin, ptbin)
        SLFandLX_D = get(os.path.join(inputF, "SLFandLX.root"), 'data', etabin, ptbin)
        SLFandLX_M = get(os.path.join(inputF, "SLFandLX.root"), 'mc', etabin, ptbin)
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
        

