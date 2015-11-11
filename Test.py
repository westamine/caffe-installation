# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 08:58:47 2015

@author: afromero
"""

###############################################################################
###############################################################################
def save_histogram(AUs_Frecuency):
    plt.figure(figsize=(13.0, 8.0))       
    ax = plt.axes()
    position_hist = np.arange(len(AUs_Frecuency))
    ax.set_xticks(position_hist + 1.0/2)
    ax.set_xticklabels(position_hist)
    ax.set_xlabel('Actions Units')
    ax.set_ylabel('Frecuency')
    ax.set_title('Frecuency of Action Units - Total of AUs='+sum(AUs_Frecuency))
    plt.bar(position_hist, AUs_Frecuency, 1, color='b')
    pyl.savefig('Histogram_AUs.png', dpi=100)
###############################################################################
###############################################################################
def Drawing_Images(Images_Draw, LM_Draw):#This variables must be dict
    import FaceExpression as FER
    import os
    
    LM={}
    LM[0] = (17, 27)#It is for nothing. Showing up all landmarks
    LM[1] = (17, 27)#All Eyebrows
    LM[2] = (36, 48)#All eyes
    LM[3] = (48, 66)#All mouth
    LM[4] = (31, 36)#All nose
    LM[5] = (54, 48)#Smile Muscle - AU12
    LM[6] = (36, 45)#Outter muscle Eye
    
    order = [1, 2, 2, 2, 2, 0, 0]
    
    count = 0        
    for show in range(0,len(Images_Draw)):
        outName_images = 'Result_Images+LM'+str(show)
        if not os.path.isdir(outName_images):
            os.mkdir(outName_images)
        outName_images_file=os.path.join(outName_images,'Image')
        for batch in range(0,len(Images_Draw[show][0])):
            FER.draw_circles_landmarks(Images_Draw[show][0][batch], \
                  LM_Draw[show][0][batch], LM[show][0], LM[show][1], 'Demo',\
                  outName_images_file+str(count).zfill(3)+'.png', order[show])
            count+=1
        count = 0     
        
##############################################################################
#----------------------------------------------------------------------------#
##############################################################################
import FaceExpression as FER

import pickle
import os.path
import time
import matplotlib.pyplot as plt
import pylab as pyl
import numpy as np

database = 'UNBC'
get_AU = 12.0
mode = ['Training', 'Test', 'ALLData']#all in case is not needed dataset splitted
Training={}
Test={}
ALLData={}
##############################################################################
####----Extracting Data from folder
##############################################################################

#--------Extracting dataset and saving them as files
for i in range(0,len(mode)):
    if os.path.isfile('ExtractData_'+mode[i]+'_'+database):
        continue
    globals()[mode[i]]['Images'], globals()[mode[i]]['AUs'], \
        globals()[mode[i]]['Landmarks'], globals()[mode[i]]['Address'], \
        globals()[mode[i]]['Images_Draw'], globals()[mode[i]]['LM_Draw'] = \
                FER.ExtractDatabase_UNBC(i)
    print "Saving %s dataset as Images, AUs, Landmarks and Address variables..."\
        %(mode[i])
    with open('Extract_'+mode[i]+'_'+database, 'w') as f:
        pickle.dump(globals()[mode[i]], f)
    print "%s Data already saved."%(mode[i])

#-------Loading files if were saved and are not variables on workspace
for i in range(0,len(mode)):
    if globals()[mode[i]]: continue
    with open('Extract_'+mode[i]+'_'+database) as f:
        print "Loading %s dataset as Images, AUs, Landmarks and Address in dict variables..."\
                %(mode[i])
        globals()[mode[i]] = pickle.load(f)
        print "%s Data already loaded."%(mode[i])

#AUs_Frecuency = FE.check_AUs_Repetitions(AUs) #Set histogram to see frecuency of AU
#save_histogram(AUs_Frecuency)    

##############################################################################
####----Spliting into training and test using one single AU 
##############################################################################  
mode_AU = ['Training_by_AU'+str(int(get_AU)), 'Test_by_AU'+str(int(get_AU)), \
                'ALLData_by_AU'+str(int(get_AU))]#all in case is not needed dataset splitted
for j in mode_AU: exec(j +' ={}')


for i in range(0,len(mode_AU)):
    print "Extracting one single AU from %s dataset"%(mode[i])
    print "Data from AU%d is foing to be splitted from Training and Test"%(int(get_AU))
    
    if os.path.isfile(mode_AU[i]+'_'+database):
        continue
    globals()[mode_AU[i]]['Images_AU'], globals()[mode_AU[i]]['Landmakrs_AU'],\
      globals()[mode_AU[i]]['Images_NO_AU'], globals()[mode_AU[i]]['Landmarks_NO_AU']\
      = FER.getFrame_by_AU(globals()[mode[i]]['Images'], globals()[mode[i]]['AUs'], \
      globals()[mode[i]]['Landmarks'], globals()[mode[i]]['Address'], get_AU)  
    #Get the data by getFrame_by_AU
                         
    print "Saving %s data..."%(mode_AU[i])
    with open(mode_AU[i]+'_'+database, 'w') as f:
        pickle.dump(globals()[mode_AU[i]], f)
    print "%s Data already saved."%(mode_AU[i])

for i in range(0,len(mode_AU)):
    if globals()[mode_AU[i]]: continue
    with open(mode_AU[i]+'_'+database) as f:
        print "Loading dataset as %s variables..."%(mode_AU[i])
        globals()[mode_AU[i]] = pickle.load(f)
        print "Data already loaded."

    

