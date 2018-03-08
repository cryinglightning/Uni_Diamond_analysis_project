#Module for all things asymmetrical

import numpy as np
from numpy import pi, exp, sin, sqrt, square as sqr, power as pwr
from scipy.optimize import curve_fit
import sys

def A0(t,B,beta,tau_mu):
    '''Used to fit a curve to the Channel Asymmetry'''
    try:
        gamma = 851616000
        return (-1./3.)*((sin(gamma*B*t-beta)-sin(gamma*B*t+beta))/(2.*beta))*exp(-t/tau_mu)
    except:
        print 'The type of parameter entered into the function used to fit a curve '\
        'to the Asymmetry function was invalid. Make sure the data file is correctly formatted, '\
        'if it is, the asym module may need maintainance'
        sys.exit()
        
def Asym_data(P_L, P_R, bin_edges, time_bins):
    '''Finds the the asymmetry between the two channels'''
    try:
        Asym = (P_L-P_R)/(P_L+P_R) #both detector channels combined into asymmetry function
        t = bin_edges[0:time_bins] #time found using bins from histogram
        return Asym, t
    except:
        print 'There was a problem finding the asymmetry between the two channels. '\
        'Make sure the data file is correctly formatted, if it is, the asym module may need maintainance'
        sys.exit()

def Asym_err(P_L, P_R):
    '''Returns the error in the asymmetry data'''
    try:
        P_L_err = sqrt(P_L)
        P_R_err = sqrt(P_R)
        A0_err = 2.*(sqrt(((sqr(P_L)*sqr(P_L_err))+(sqr(P_R)*sqr(P_R_err)))/pwr((P_L+P_R),4)))
        return A0_err
    except:
        print 'There was a problem finding the error in the asymmetry between the two channels. '\
        'Make sure the data file is correctly formatted, if it is, the asym module may need maintainance'
        sys.exit()

def Asym_fit(t,Asym,B_est,beta_est,A0_err):
    '''Takes the Asymmetry Data and estimates for the magnetic field and beta parameters. Returns the actual magnetic field and beta'''
    try:
        fitA, covA = curve_fit(A0, t, Asym, p0=(B_est, beta_est, 0.000001), sigma=(A0_err))
        return fitA, covA
    except:
        print 'An error occurred when trying to calculate the fitting parameters for the asymmetry curve. '\
        'Make sure the data file is correctly formatted, if it is, the asym module may need maintainance'
        sys.exit()
    
def param_est(Asym,t):
    '''Calculates estimates for the magnetic field and beta parameters to feed into curve_fit for the asymmetry function'''
    try:
        gamma = 851616000
        #uses time period to find an estimate for the magnetic field
        for m in Asym:
            if m > 0:
                None
            else:
                T = 4.*np.float_(t[np.int_(np.where(Asym == m)[0])])
                break
        freq = 2.*pi/T
        B_est = freq/gamma
        beta_est = 3.*max(Asym[0:len(Asym)/6.]) #estimate for beta using amplitude before damping is significant
        return B_est, beta_est
    except:
        print 'An error occurred when trying to estimate the fitting parameters for the asymmetry curve. '\
        'Make sure the data file is correctly formatted, if it is, the asym module may need maintainance'
        sys.exit()