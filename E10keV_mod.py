#Module for plotting 10keV results

from matplotlib import pyplot as plt
import asym_mod as asym
import sys

def E10keV_hists(ch1,ch2,time_bins):
    '''plots histograms of the decay times for 10keV'''
    try:
        #channel 1
        plt.figure(1)
        plt.hist(ch1, bins=time_bins, edgecolor='none', color='r')
        plt.title('Left Channel (10keV) (py14hjcl)')
        plt.xlabel('Time (s)')
        plt.ylabel('Counts')
        plt.show()
    except:
        print 'An error occurred when trying to plot the left channel histogram for 10keV energy. '\
        'Make sure the data file is correctly formatted and all the data in the time columns are floats. '\
        'If it is/they are, the E10keV module may need maintainance'
        sys.exit()
    try:
        #channel 2
        plt.figure(2)
        plt.hist(ch2, bins=time_bins, edgecolor='none', color='g')
        plt.title('Right Channel (10keV) (py14hjcl)')
        plt.xlabel('Time (s)')
        plt.ylabel('Counts')
        plt.show()
    except:
        print 'An error occurred when trying to plot the right channel histogram for 10keV energy. '\
        'Make sure the data file is correctly formatted and all the data in the time columns are floats. '\
        'If it is/they are, the E10keV module may need maintainance'
        sys.exit()
        
def E10keV_asym_plot(t,fitA,covA,Asym,A0_err):
    '''Plots the asymmetry function for 10keV energies'''
    try:
        plt.figure(3)
        #takes the A0_err from the Aysm_err function for the errorbars
        plt.errorbar(t*1e6,
                     Asym,
                     yerr=A0_err,
                     fmt='x',
                     color='c',
                     label='Measured Asymmetry'
                     )
        plt.title('Channel Asymmetry (10keV) (py14hjcl)')
        plt.xlabel('Time ($\mu$s)')
        plt.ylabel('Asymmetry Function')
        plt.plot(t*1e6, asym.A0(t, fitA[0], fitA[1], fitA[2]), color='b', label='Fitted data') #plots the Asym_fit function on the Asym_data
        plt.legend()
        plt.show()
    except:
        print 'An error occurred when trying to plot the Asymmetry function for 10keV energy. '\
        'Make sure the data file is correctly formatted, if it is, the E10keV module may need maintainance'
        sys.exit()