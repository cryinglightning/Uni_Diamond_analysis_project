#Module for finding the Bfield - energy relationship

from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import sys

def B(E,a,b,c):
    '''Used to fit a quadratic to magnetic field's energy dependence'''
    try:
        return a*np.power(E,2.)+b*E+c
    except TypeError:
        print 'The type of parameter entered into the function used to fit a quadratic '\
        'to the Bfield energy dependence was invalid. Make sure the data file is correctly formatted, '\
        'if it is, the B_E_plot module may need maintainance'
        sys.exit()

def B_E_fit(imp_Es, fitA_Bs, fitA_Bs_err):
    '''Parameters for a fit for the Bfield energy dependence using the B function'''
    try:
        fitB, covB = curve_fit(B, imp_Es, fitA_Bs, sigma=fitA_Bs_err)
        return fitB, covB
    except TypeError:
        print 'The type of parameter entered into Bfield fitting function was invalid. '\
        'The parameters should be arrays of the x and y variables and the errors. '\
        'Make sure the data file is correctly formatted, if it is, the B_E_plot module may need maintainance'
        sys.exit()
    except ValueError:
        print 'Not all the arrays entered into Bfield fitting function were the same length'\
        'Make sure the data file is correctly formatted, if it is, the B_E_plot module may need maintainance'
        sys.exit()
        
def B_E_plot(imp_Es,fitA_Bs,fitA_Bs_err):
    '''Plots the Bfield energy dependence with a quadratic fit'''
    try:    
        imp_Es = np.asarray(imp_Es)
        f = interp1d(imp_Es,fitA_Bs,kind='quadratic') #interpolates the data so a smooth curve can be plotted
        xnew = np.linspace(5,25,endpoint=True) #defines new x values for the interpolated data
    
        plt.figure(4)
        plt.errorbar(imp_Es, fitA_Bs, yerr=fitA_Bs_err, fmt='x', label='Measured B-field') #plot using Bfield data from the Asymmetry function fits for each energy
        plt.plot(xnew, f(xnew), c='r', label='Fitted field') #plots the quadratic on top of the data
        plt.title('Magnetic Field Dependence On Energy (py14hjcl)')
        plt.xlabel('Implantation Energy (keV)')
        plt.ylabel('Magnetic Field, $\mu_0$H (T)')
        plt.legend(loc='lower right')
        plt.show()
    except:
        print 'An error occurred when trying to plot the Bfield - energy relationship'\
        'Make sure the data file is correctly formatted, if it is, the B_E_plot module may need maintainance'
        sys.exit()