#Module for splitting up the channels and making histograms

import numpy as np
from numpy import sqrt
import sys

def bins(ch1,ch2):
    '''Returns the appropriate number of bins for histograms based on the amount of data in each channel'''
    try:
        return int(sqrt(len(ch1)+len(ch2)))
    except:
        print 'An error occurred when trying to calculate the number of bins to use in the histogram. '\
        'Something may have gone wrong when the data was split into each detector channel '\
        'Make sure the data file is correctly formatted and that all the data in the time columns are floats'\
        'if it is/they are, the hist module may need maintainance'
        sys.exit()

def channel_split(i, time_array):
    '''Separates the times into two channels depending on which detector was hit. Returns an array for each channel'''
    ch1 = []
    ch2 = []
    for row in time_array:
        if row[i+1] == 1:
            ch1.append(row[i]*1e-6)
        elif row[i+1] == 2:
            ch2.append(row[i]*1e-6)
        else:
            break
    return ch1, ch2

def histograms(ch1,ch2,time_bins):
    '''Creates histograms for all energies to use in asymmetry function (but doesn't show them)'''
    try:
        P_L,bin_edges=np.histogram(ch1, bins=time_bins)
        P_R,bin_edges=np.histogram(ch2, bins=time_bins)
        P_L = np.float_(P_L)
        P_R = np.float_(P_R)
        return P_L, P_R, bin_edges
    except:
        print 'An error occurred when trying to create histograms for each channel. '\
        'Make sure the data file is correctly formatted and that all the data in the time columns are floats'\
        'if it is/they are, the hist module may need maintainance'
        sys.exit()
    