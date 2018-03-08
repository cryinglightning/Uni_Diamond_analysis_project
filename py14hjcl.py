import numpy as np
from numpy import sqrt
import sys
import hist_mod as hst
import asym_mod as asym
import E10keV_mod as E10
import B_E_plot_mod as B_E
from re import search

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
            ch1, ch2 = hst.channel_split(i,time_array) #call the channel splitter on the data to get an array for each channel
            time_bins = hst.bins(ch1,ch2) #call the bins function to get the right number for the histograms
            P_L, P_R, bin_edges = hst.histograms(ch1,ch2,time_bins) #makes the hisograms
            #prints the histgrams for 10keV energy
            if col_names[i] == 'Time_us__10keV':
                E10.E10keV_hists(ch1,ch2,time_bins)
            elif type(col_names[i]) is str:
                pass
            else:
                break
            Asym, t = asym.Asym_data(P_L,P_R,bin_edges,time_bins) #gets the asymmetry data from the histograms
            A0_err = asym.Asym_err(P_L,P_R) #gets the errors for the asymmetry data
            B_est, beta_est = asym.param_est(Asym,t) #calculates the estimates for the asymmetry curve_fit
            fitA, covA = asym.Asym_fit(t,Asym,B_est,beta_est,A0_err) #makes the asymmetry plot
            #adds results to the lists at the start of the function for use in B-E plot
            imp_Es.append(float(search(r'\d+(d+)?', col_names[i]).group(0))) #uses re module to find the energy within the column header
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
                Results_check(B_10keV,B_10keV_error,beta,beta_error,tau_10keV_damp,tau_10keV_damp_error)
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
    
def Results_check(B_10keV,B_10keV_error,beta,beta_error,tau_10keV_damp,tau_10keV_damp_error):
    '''Type and sanity checker for the 10keV results'''
    try:
        assert isinstance(B_10keV,float) #checks it's a float
        assert 0 < B_10keV < 0.1 #checks it's within a sensible range of values
    except:
        print 'B_10keV did not return a float in the expected range'
    try:
        assert isinstance(B_10keV_error,float)
        assert 0 < B_10keV_error < 0.01
    except:
        print 'B_10keV_error did not return a float in the expected range'
    try:
        assert isinstance(beta,float)
        assert 0 < beta < 10
    except:
        print 'beta did not return a float in the expected range'
    try:
        assert isinstance(beta_error,float)
        assert 0 < beta_error < 1
    except:
        print 'beta_error did not return a float in the expected range'
    try:
        assert isinstance(tau_10keV_damp,float)
        assert 0 < tau_10keV_damp < 50
    except:
        print 'tau_10keV_damp did not return a float in the expected range'
    try:
        assert isinstance(tau_10keV_damp_error,float)
        assert 0 < tau_10keV_damp_error < 1
    except:
        print 'tau_10keV_damp_error did not return a float in the expected range'