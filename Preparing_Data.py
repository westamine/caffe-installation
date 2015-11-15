# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 08:58:47 2015

@author: afromero
"""
        
##############################################################################
#----------------------------------------------------------------------------#
##############################################################################
import FaceExpression as FER
import Prepating_Hypercolums as hyper

import pickle
import os.path
#import time
#import matplotlib.pyplot as plt
#import pylab as pyl
#import numpy as np
#import sys

database = 'UNBC'
folder_prep_hyper  = os.path.join('..','datos','Experiments',database,'PreparingData_Hypercolums')
get_AU = 12.0 #Landmark 54 and 48 - Smile Muscle AU12
LM     = (48,54)

##############################################################################
####----Extracting Data from folder, considering several AUs for the same Image - DataJointed
##############################################################################
if not os.path.isfile(os.path.join(folder_prep_hyper, 'Images')):  
    #--------Extracting dataset and saving them as files
    Images, AUs, Landmarks, Address = FER.ExtractDatabase_UNBC(0)#Read from folders 
##############################################################################
####----Transforming the data, considering AU and Images one by one - DataAll
##############################################################################  
    Images, AUs, Landmarks, Address = FER.get_data_disjoint(Images, AUs, Landmarks, Address)
    print "Saving Images, AUs, Landmarks and Address variables..."
    with open(os.path.join(folder_prep_hyper, 'Images'), 'w') as f:
        pickle.dump(Images, f)
    with open(os.path.join(folder_prep_hyper, 'AUs'), 'w') as f:
        pickle.dump(AUs, f)
    with open(os.path.join(folder_prep_hyper, 'Landmarks'), 'w') as f:
        pickle.dump(Landmarks, f)
    with open(os.path.join(folder_prep_hyper, 'Address'), 'w') as f:
        pickle.dump(Address, f)        
    print "Variables already saved."
else:
    print "Loading Images, AUs, Landmarks and Address variables..."
    with open(os.path.join(folder_prep_hyper, 'Images')) as f:
        Images = pickle.load(f)
    with open(os.path.join(folder_prep_hyper, 'AUs')) as f:
        AUs = pickle.load(f)
    with open(os.path.join(folder_prep_hyper, 'Landmarks')) as f:
        Landmarks = pickle.load(f)
    with open(os.path.join(folder_prep_hyper, 'Address')) as f:
        Address = pickle.load(f)    
    print "Variables already loaded."
            
##############################################################################
####----Get annotations by AU, bounding boxand groundtruth points.
##############################################################################  
mode_AU = 'Annotations_AU'+str(int(get_AU))
folderOut = os.path.join(folder_prep_hyper, mode_AU)
os.system('mkdir '+folderOut)

print "Extracting one single AU from the entire Data"
print "Setting Data-AU%d for TruePositive(TP), TrueNegative(TN) else. "%(int(get_AU))
    
if not os.path.isfile(os.path.join(folderOut,'Binary_Annotations')):
    Binary_Annotations  = FER.getAnnotation_by_AU(AUs, get_AU, Address)  
    box, groundtruth = FER.getRecs_by_AU(Landmarks, LM)
    print "Saving variables: Binary_Annotations, bounding box and groundtruth points associated..."
    with open(os.path.join(folderOut,'Binary_Annotations'), 'w') as f:
        pickle.dump(Binary_Annotations, f)
    with open(os.path.join(folderOut,'box'), 'w') as f:
        pickle.dump(box, f)
    with open(os.path.join(folderOut,'groundtruth'), 'w') as f:
        pickle.dump(groundtruth, f)    
    print "Variables already saved."

else:
    print "Loading variables: Binary_Annotations, bounding box and groundtruth points associated..."
    with open(os.path.join(folderOut,'Binary_Annotations')) as f:
        Binary_Annotations = pickle.load(f)
    with open(os.path.join(folderOut,'box')) as f:
        box = pickle.load(f)
    with open(os.path.join(folderOut,'groundtruth')) as f:
        groundtruth = pickle.load(f)            
    print "Variables already loaded."

##############################################################################
####----Preparing data for hypercolums
############################################################################## 
im_shape = Images[0].shape
boxes = hyper.clip_boxes(box[0]-1, im_shape) 

 im_new, spp_boxes, normalized_boxes, categids = \
     hyper.get_blobs(Images[0], boxes, np.array([Binary_Annotations[0]]))


