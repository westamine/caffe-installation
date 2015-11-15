# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 11:07:31 2015

@author: afromero
"""

###############################################################################
###############################################################################
def save_histogram(AUs_Frecuency, mode):
    plt.figure(figsize=(13.0, 8.0))       
    ax = plt.axes()
    position_hist = np.arange(len(AUs_Frecuency))
    ax.set_xticks(position_hist + 1.0/2)
    ax.set_xticklabels(position_hist)
    ax.set_xlabel('Actions Units')
    ax.set_ylabel('Frecuency')
    ax.set_title('Frecuency of Action Units for '+mode+'- Total of AUs='+str(sum(AUs_Frecuency)))
    plt.bar(position_hist, AUs_Frecuency, 1, color='b')
    pyl.savefig('Histograms/Histogram_AUs_'+mode+'.png', dpi=100)
    
###############################################################################
###############################################################################    

import FaceExpression as FER

import pickle
import os.path
import matplotlib.pyplot as plt
import pylab as pyl
import numpy as np

database = 'UNBC'
folder_save = os.path.join('..','datos','Experiments','DataExtracted')
mode = ['Data', 'Training', 'Test']#ALLData in case is not needed dataset splitted
Training={}
Test={}
ALLData={}


##############################################################################
####----Extracting Data from folder
##############################################################################

#--------Extracting dataset and saving them as files
for i in range(0,len(mode)):
    if not os.path.isfile(os.path.join(folder_save,'Extract_'+mode[i]+'_'+database)):
        globals()[mode[i]]['Images'], globals()[mode[i]]['AUs'], \
            globals()[mode[i]]['Landmarks'], globals()[mode[i]]['Address'],  = \
                    FER.ExtractDatabase_UNBC(i)
        print "Saving %s dataset as Images, AUs, Landmarks and Address variables..."\
            %(mode[i])
        with open(os.path.join(folder_save,'Extract_'+mode[i]+'_'+database), 'w') as f:
            pickle.dump(globals()[mode[i]], f)
        print "%s Data already saved."%(mode[i])

#-------Loading files if were saved and are not variables on workspace
    if not globals()[mode[i]]:
        with open(os.path.join(folder_save,'Extract_'+mode[i]+'_'+database)) as f:
            print "Loading %s dataset as Images, AUs, Landmarks and Address in dict variables..."\
                    %(mode[i])
            globals()[mode[i]] = pickle.load(f)
            print "%s Data already loaded."%(mode[i])
    AUs_Frecuency = FER.check_AUs_Repetitions(globals()[mode[i]]['AUs']) #Set histogram to see frecuency of AU
    save_histogram(AUs_Frecuency, mode[i]) 

  