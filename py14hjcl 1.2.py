from matplotlib import pyplot as plt
import numpy as np
from numpy import pi, exp, sin, sqrt, square as sqr, power as pwr
from scipy.optimize import curve_fit
from re import search
from scipy.interpolate import interp1d
import sys
import hist_mod as hst
import asym_mod as asym
import E10keV_mod as E10
import B_E_plot_mod as B_E

#def A0(t,B,beta,tau_mu):
#    '''Used to fit a curve to the Channel Asymmetry'''
#    gamma = 851616000
#    return (-1./3.)*((sin(gamma*B*t-beta)-sin(gamma*B*t+beta))/(2.*beta))*exp(-t/tau_mu)
#
#def Asym_data(P_L, P_R, bin_edges):
#    '''Finds the the asymmetry between the two channels'''
#    Asym = (P_L-P_R)/(P_L+P_R) #both detector channels combined into asymmetry function
#    t = bin_edges[:-1]+bin_edges[1:]/2.0 #time found using bin centres from histogram
#    return Asym, t
#
#def Aysm_err(P_L, P_R):
#    '''Returns the error in the asymmetry data'''
#    P_L_err = sqrt(P_L)
#    P_R_err = sqrt(P_R)
#    A0_err = 2.*(sqrt(((sqr(P_L)*sqr(P_L_err))+(sqr(P_R)*sqr(P_R_err)))/pwr((P_L+P_R),4)))
#    return A0_err
#
#def Asym_fit(t,Asym,B_est,beta_est,A0_err):
#    '''Takes the Asymmetry Data and estimates for the magnetic field and beta parameters. Returns the actual magnetic field and beta'''
#    fitA, covA = curve_fit(A0, t, Asym, p0=(B_est, beta_est, 0.000001), sigma=(A0_err))
#    return fitA, covA

#def B(E,a,b,c):
#    '''Used to fit a quadratic to magnetic field's energy dependence'''
#    return a*np.power(E,2.)+b*E+c
#
#def B_E_fit(imp_Es, fitA_Bs, fitA_Bs_err):
#    '''Parameters for a fit for the Bfield energy dependence using the B function'''
#    fitB, covB = curve_fit(B, imp_Es, fitA_Bs, sigma=fitA_Bs_err)
#    return fitB, covB
#
#def B_E_plot(imp_Es,fitA_Bs,fitA_Bs_err):
#    '''Plots the Bfield energy dependence with a quadratic fit'''
#    imp_Es = np.asarray(imp_Es)
#    f = interp1d(imp_Es,fitA_Bs,kind='quadratic') #interpolates the data so a smooth curve can be plotted
#    xnew = np.linspace(5,25,endpoint=True) #defines new x values for the interpolated data
#    
#    plt.figure(4)
#    plt.errorbar(imp_Es, fitA_Bs, yerr=fitA_Bs_err, fmt='none') #plot using Bfield data from the Asymmetry function fits for each energy
#    plt.plot(xnew, f(xnew)) #plots the quadratic on top of the data
#    plt.title('Magnetic Field Dependence On Energy (py14hjcl)')
#    plt.xlabel('Implantation Energy (keV)')
#    plt.ylabel('Magnetic Field, B (T)')
#    plt.show()

#def bins(ch1,ch2):
#    '''Returns the appropriate number of bins for histograms based on the amount of data in each channel'''
#    return int(sqrt(len(ch1)+len(ch2)))

#def channel_split(i, time_array):
#    '''Separates the times into two channels depending on which detector was hit. Returns an array for each channel'''
#    ch1 = []
#    ch2 = []
#    for row in time_array:
#        if row[i+1] == 1:
#            ch1.append(row[i]*1e-6)
#        elif row[i+1] == 2:
#            ch2.append(row[i]*1e-6)
#        else:
#            break
#    return ch1, ch2

#def E10keV_asym_plot(t,fitA,covA,Asym,A0_err):
#    '''Plots the asymmetry function for 10keV energies'''
#    plt.figure(3)
#    plt.errorbar(t, Asym, yerr=A0_err, color='c') #takes the A0_err from the Aysm_err function for the errorbars
#    plt.title('Channel Asymmetry (py14hjcl)')
#    plt.xlabel('Time (seconds)')
#    plt.ylabel('Asymmetry Function')
#    plt.plot(t, A0(t, fitA[0], fitA[1], fitA[2]), color='b') #plots the Asym_fit function on the Asym_data
#    plt.show()

#def E10keV_hists(ch1,ch2,time_bins):
#    '''plots histograms of the decay times for 10keV'''
#    #channel 1
#    plt.figure(1)
#    plt.hist(ch1, bins=time_bins, edgecolor='none', color='r')
#    plt.title('Left Channel (py14hjcl)')
#    plt.xlabel('Time (seconds)')
#    plt.ylabel('Counts')
#    plt.show()
#    #channel 2
#    plt.figure(2)
#    plt.hist(ch2, bins=time_bins, edgecolor='none', color='g')
#    plt.title('Right Channel (py14hjcl)')
#    plt.xlabel('Time (seconds)')
#    plt.ylabel('Counts')
#    plt.show()
#
#def histograms(ch1,ch2,time_bins):
#    '''Creates histograms for all energies to use in asymmetry function (but doesn't show them)'''
#    P_L,bin_edges=np.histogram(ch1, bins=time_bins)
#    P_R,bin_edges=np.histogram(ch2, bins=time_bins)
#    P_L = np.float_(P_L)
#    P_R = np.float_(P_R)
#    return P_L, P_R, bin_edges
#
#def param_est(Asym,t):
#    '''Calculates estimates for the magnetic field and beta parameters to feed into curve_fit for the asymmetry function'''
#    gamma = 851616000
#    #uses time period to find an estimate for the magnetic field
#    for m in Asym:
#        if m > 0:
#            None
#        else:
#            T = 4.*np.float_(t[np.int_(np.where(Asym == m)[0])])
#            break
#    freq = 2.*pi/T
#    B_est = freq/gamma
#    beta_est = 3.*max(Asym[0:len(Asym)/6.]) #estimate for beta using amplitude before damping is significant
#    return B_est, beta_est

def ProcessData(filename):
    '''Takes muon decay times for given implantaion energies and returns magnetic field strength,
    detector angle and damping time for a 10keV implantaion energy (with uncertainties). Also returns
    coefficents of a quadratic fit to the magnetic field's energy dependence with uncertainties.

    Parameters
    ----------
    filename : file
        The name of the data file
    
    Returns
    -------
    10keV_B : float
        The magnetic field strength for 10keV implantation energy (T)
    
    10keV_B_error : float
        The error in the magnetic field strength (T)
    
    beta : float
        Detector angle (rad)
    
    beta_error : float
        Uncertainity in detector angle (rad)
    
    10keV_tau_damp : float
        Damping time for 10keV (s)
    
    10keV_tau_damp_error : float
        Uncertainty in damping time for 10keV (s)

    B(Energy)_coeffs : tuple
        Quadratic, linear and constant terms for fitting B dependence on energy (T/keV^2,T/keV,T)
    
    B(Energy)_coeffs_errors : tuple
        Errors in above in same order
    '''
    try:
        with open(filename, 'r') as data: #opens file as read only
            #this skips any metadata or irrelevant code at the top
            for line in data:
                if line.startswith('&END'):
                    break
                else:
                    None
            time_array = np.genfromtxt(data, delimiter='\t', names=True) #turns data into numpy array with column names
            col_names = time_array.dtype.names #array of the coloumn names
    except:
        print 'File name not in directory'
        sys.exit()
        
    #empty lists for results of each implantation energy to go into
    imp_Es = []
    fitA_Bs = []
    fitA_betas = []
    fitA_Bs_err = []
    
    i=0 #loop counter
    #while loop will cycle through each energy (used while because it can work for any number of energies within reason)
    while True:
        try:
            ch1, ch2 = hst.channel_split(i, time_array) #call the channel splitter on the data to get an array for each channel
            time_bins = hst.bins(ch1,ch2) #call the bins function to get the right number for the histograms
            P_L, P_R, bin_edges = hst.histograms(ch1,ch2,time_bins) #makes the hisograms
            #prints the histgrams for 10keV energy
            if col_names[i] == 'Time_us__10keV':
                E10.E10keV_hists(ch1,ch2,time_bins)
            elif type(col_names[i]) is str:
                pass
            else:
                break
            Asym, t = asym.Asym_data(P_L, P_R, bin_edges) #gets the asymmetry data from the histograms
            A0_err = asym.Aysm_err(P_L, P_R) #gets the errors for the asymmetry data
            B_est, beta_est = asym.param_est(Asym,t) #calculates the estimates for the asymmetry curve_fit
            fitA, covA = asym.Asym_fit(t,Asym,B_est,beta_est,A0_err) #makes the asymmetry plot
            #adds results to the lists at the start of the function for use in B-E plot
            imp_Es.append(float(search(r'\d+(d+)?', col_names[i]).group(0)))
            fitA_Bs.append(fitA[0])
            fitA_betas.append(fitA[1])
            fitA_Bs_err.append(covA[0,0])
            if col_names[i] == 'Time_us__10keV':
                E10.E10keV_asym_plot(t,fitA,covA,Asym,A0_err) #prints the Asmmetry function for 10keV energy
                #defines some of the results
                B_10keV = fitA[0]
                B_10keV_error = sqrt(covA[0,0])
                beta = fitA[1]
                beta_error = sqrt(covA[1,1])
                tau_10keV_damp = fitA[2]
                tau_10keV_damp_error = sqrt(covA[2,2])
                assert isinstance(B_10keV,float) and B_10keV != 0
            elif type(col_names[i]) is str:
                pass
            else:
                break
            i=i+2 #adds to the counter
        except IndexError:
            #loop breaks when there are no more energies
            break

    fitB, covB = B_E.B_E_fit(imp_Es, fitA_Bs, fitA_Bs_err) #makes the B-E plot
    B_E.B_E_plot(imp_Es,fitA_Bs,fitA_Bs_err) #prints the B-E plot

    results={"10keV_B": B_10keV, #this is the magnetic field for 10keV data (T)
             "10keV_B_error": float('%s' % float('%.1g' % B_10keV_error)), # the error in the magnetic field (T)
             "beta": beta, #Detector angle in radians
             "beta_error": float('%s' % float('%.1g' % beta_error)), #uncertainity in detector angle (rad)
             "10keV_tau_damp": tau_10keV_damp, #Damping time for 10keV (s)
             "10keV_tau_damp_error": float('%s' % float('%.1g' % tau_10keV_damp_error)), #and error (s)
             "B(Energy)_coeffs":(fitB[0],fitB[1],fitB[2]), #tuple of a,b,c for quadratic,linear and constant terms
                                                  #for fitting B dependence on energy
                                                  #(T/keV^2,T/keV,T)
             "B(Energy)_coeffs_errors":(float('%s' % float('%.1g' % sqrt(covB[0,0]))),
                                        float('%s' % float('%.1g' % sqrt(covB[1,1]))),
                                        float('%s' % float('%.1g' % sqrt(covB[2,2])))), # Errors in above in same order (T/keV^2,T/keV,T)
             }
    return results
    
print ProcessData('assessment_data_py14hjcl.dat')