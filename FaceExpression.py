# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 07:42:21 2015

@author: afromero
"""

import os
import glob
import cv2 as cv
import numpy as np

def ExtractDatabase_UNBC(set_training_id):
    #set_training_id = 0 for the entire dataset    
    #set_training_id= 1 for Training
    #set_training_id = 2 for Test
    
    database = "UNBC"
#    plottingNumber = 10#Optional
#    database = os.path.join('../datos/',database)#Location of database in virtualmachine
#    Comment last line for location of database in personal computer

    print "Location of database: %s"%(database)    
    
    Images = []
    AUs = []
    Landmarks = []
    Address = []
#    Draw_Images = {}
#    Draw_LM = {}
#    temp_Images=[]
#    temp_Landmarks = []
#    for cc in range(0,plottingNumber):
#        Draw_Images[cc]=[]
#        Draw_LM[cc]=[]
        
    FACS_Folder = os.path.join(database,'Frame_Labels','FACS')
    Landmarks_Folder = os.path.join(database,'AAM_landmarks')
    Images_Folder = os.path.join(database,'Images')

    subject_id = sorted(os.listdir(FACS_Folder))    
    if not set_training_id:
        mode = 'Data'
    elif set_training_id==1: 
        subject_id = subject_id[len(subject_id)/2+1:]
        mode = 'Training'
    elif set_training_id==2:
        subject_id = subject_id[len(subject_id)/2+1:]
        mode = 'Test'
        
    for i in range(0,len(subject_id)): #range(0,plottingNumber) in case of plotting
        
        sequence_id = sorted(os.listdir(os.path.join(FACS_Folder,subject_id[i])))
        
        for j in range(0,len(sequence_id)): #range(0,1): in case of plotting
            
            filename_folder =  sorted(glob.glob(os.path.join(\
                            Images_Folder,subject_id[i], sequence_id[j],'*png')))
                            
            for k in range(0,len(filename_folder)):
                filename = filename_folder[k].split('/')
                filename = filename[-1][:-4]
                ssf = os.path.join(subject_id[i], sequence_id[j], filename)
                FACS_file = os.path.join(FACS_Folder, ssf+'_facs.txt')
                print "File %s belongs to %s, processing... AU annotation: "%(ssf, mode),
                if not os.stat(FACS_file).st_size: 
                    print "Empty File."
                    continue #If FACS_file is empty
                
                ############--------------Read FACS File
                count = 0
                with open(FACS_file,'r') as f:
                    for batch in read_by_batch(f):
                        if float(batch)==50.0 or float(batch)==0.0: 
                            print "¿50? ",
                            continue#IDK what 50 means on facs files
                        if not count:
                            AUs.append([float(batch)]) 
                        else:
                            AUs[-1].append(float(batch))
                        count+=1
                        print "%s "%(str(float(batch))),

                print ""
                ############--------------Read Images File                
                Images_file = os.path.join(Images_Folder, ssf+'.png')              
                Images.append(cv.imread(Images_file))                
#                temp_Images.append(cv.imread(Images_file))
                Address.append(Images_file)
                
                ############--------------Read Landmarks File
                Landmarks_file = os.path.join(Landmarks_Folder, ssf+'_aam.txt')
                s_landmarks = open(Landmarks_file,'r').read().split()
                mat_landmarks = np.zeros((len(s_landmarks)/2, 2))
                count=0
                for marks in range(0,len(s_landmarks),2):
                    mat_landmarks[count][0] = float(s_landmarks[marks])
                    mat_landmarks[count][1] = float(s_landmarks[marks+1])
                    count+=1
                Landmarks.append(mat_landmarks)
#                temp_Landmarks.append(mat_landmarks)
#        Draw_Images[i].append(temp_Images)
#        Draw_LM[i].append(temp_Landmarks)
#        temp_Images=[]
#        temp_Landmarks=[]
    print "Images, AUs, Landmarks and Addresses from %s (%d data) successfully extracted!"\
                                                                %(mode, len(AUs))        
    return Images, AUs, Landmarks, Address 
                
def read_by_batch(fileobj):
    for line in fileobj:
        batch = line.split()
        yield batch[0]

def check_AUs_Repetitions(AU_Array):
    AUs_List = []
    for element in AU_Array:
        for pos in element:
            AUs_List.append(int(pos))
    AUs_repetitions = np.bincount(np.array(AUs_List))
    return AUs_repetitions
    
def get_data_disjoint(Images, AUs, Landmarks, Address):
    Images_out    = []
    AUs_out       = []
    Landmarks_out = []
    Address_out   = []
    count = 0
    for element in AUs:
        for position in element:
            AUs_out.append(int(position))
            Images_out.append(Images[count])
            Landmarks_out.append(Landmarks[count])
            Address_out.append(Address[count])
        count += 1
    return Images_out, AUs_out, Landmarks_out, Address_out

def getAnnotation_by_AU(AUs, number_of_AU, Address):
    annotations = []
    count = 0
    for element in AUs:
        if element==number_of_AU:
            annotations.append(1)
            print "AU%d for TruePositive Data, from file %s. - count = %d"\
                %(int(element), Address[count], count)
        else:
            annotations.append(0)
            print "AU%d for TrueNegative Data, from file %s. - count = %d"\
                %(int(element), Address[count], count)
        count += 1

    print "Data for TP=%d, data for TN=%d"%(np.bincount(np.array(annotations))[1],\
                                            np.bincount(np.array(annotations))[0])
    return annotations

def getRecs_by_AU(Landmarks, points_AU):
    rects_landmark  = []
    points_landmark = []
    sizeRect = 5
    for sequence in Landmarks:
        recs_AU = np.zeros((len(points_AU),4), dtype='float32')
        gt_AU   = np.zeros((len(points_AU),2), dtype='float32')
        for point in range(0,len(points_AU)):
            coordinate = sequence[points_AU[point]]
            gt_AU[point, :] = np.array([coordinate])
            recs_AU[point, :] = np.array([coordinate[0]-sizeRect, coordinate[1]-sizeRect,\
                                        coordinate[0]+sizeRect, coordinate[1]+sizeRect])
                
#                rects_landmark[-1].append([points_landmark[-1][0]-5, points_landmark[-1][1]-5, \
#                                        points_landmark[-1][0]+5, points_landmark[-1][1]+5])
        rects_landmark.append(recs_AU) 
        points_landmark.append(gt_AU)
    return rects_landmark, points_landmark