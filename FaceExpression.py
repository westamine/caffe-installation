# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 07:42:21 2015

@author: afromero
"""
def ExtractDatabase_MMI():
    import os
    import xml.etree.ElementTree as ET
    import glob
    import cv2 as cv

    database = "MMI"
    database = os.path.join('/home/rv.andres10/Datasets',database)#Location of database
    print "Location of database: %s"%(database)    
    root = os.listdir(database)#Sessions and subjects
    Images = []
    AUs = []
    Sessions = sorted(os.listdir(os.path.join(database,root[0])))
    for i in range(1,len(Sessions)+1):
        #Files = os.listdir(os.path.join(database,
        #                                root[0], Sessions[int(i)-1]))
        FACS_file = glob.glob(os.path.join(database,
                                          root[0], 
                                          Sessions[int(i)-1], '*oao*'))            
        #print "\n AUs from File %s"%(FACS_file)                                              
        if not FACS_file: 
            #print "There is no file associated"
            continue                                            
        Video_file = glob.glob(os.path.join(database,
                                          root[0], 
                                          Sessions[int(i)-1], '*avi'))         
        xml_File = ET.parse(FACS_file[0]).getroot()
        # xml_File.attrib['NumFrames'] -> Number of frames
        for child_root in xml_File:
            if child_root.tag=="Metatag": continue
            #it is no needed Metatag info
            if child_root.tag == "ActionUnit": #Branch Action Unit
                for j in range(0,len(child_root)):
                    if int(child_root[j].attrib['Type'])==3 or\
                            (int(child_root[j].attrib['Type'])==2 and \
                            (j+1)>len(child_root)-1):  #Branch markers
                    #It is needed type 3 action unit 
                    #OR sometimes type 2 is the maximun, such as 344 folder  
                        count=0    
                        if Video_file: Video = cv.VideoCapture(Video_file[0])
                        else: 
                            #print "There is no video file"
                            continue
                    
                        while(Video.isOpened()):
                            count+=1
                            ret, frame = Video.read() #Read entire video
                            if count==1: 
                                Images.append(frame)                            
                                AUs.append('99')
                            if count==int(child_root[j].attrib['Frame']): 
                            #Look for frame having type 3 action unit
                                break  #If founf it break
                        Video.release()                      
    
                        Images.append(frame)#Extract frame and save it
                        AUs.append(child_root.attrib['Number'])#Extract AU and save it
                        print "AU %s type %d associated with frame %d of Video %s"\
                            %(child_root.attrib['Number'], \
                            int(child_root[j].attrib['Type']), count, Video_file[0])
    
    print "%d Actions Units (%d labels) of dataset extracted successfully!"%(len(AUs), len(set(AUs)))
    return Images, AUs, 0

def ExtractDatabase_UNBC(set_training_id):
    #set_training_id= 0 for Training, set_training_id = 1 for Test
    #set_training_id = 2 for the entire dataset
    import os
    import glob
    import cv2 as cv
    import numpy as nm
    
    database = "UNBC"
#    plottingNumber = 10#Optional
    database = os.path.join('/home/rv.andres10/Datasets',database)#Location of database
    print "Location of database: %s"%(database)    
    
    Images = []
    AUs = []
    Landmarks = []
    Address = []
    Draw_Images = {}
    Draw_LM = {}
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
        subject_id = subject_id[0:len(subject_id)/2+1]
        mode = 'Training'
    elif set_training_id==1: 
        subject_id = subject_id[len(subject_id)/2+1:]
        mode = 'Test'
    elif set_training_id==2:
         mode = 'All '
        
    for i in range(0,len(subject_id)): #range(0,plottingNumber) in case of plotting
        
        sequence_id = sorted(os.listdir(os.path.join(FACS_Folder,subject_id[i])))
        
        for j in range(0,len(sequence_id)): #range(0,1): in case of plotting
            
            filename_folder =  sorted(glob.glob(os.path.join(\
                            Images_Folder,subject_id[i], sequence_id[j],'*png')))
                            
            for k in range(0,len(filename_folder)):
                filename = filename_folder[k].split('/')
                filename = filename[-1][:-4]
                ssf = os.path.join(subject_id[i], sequence_id[j], filename)
                print "File %s belongs to %s, processing..."%(ssf, mode)
                FACS_file = os.path.join(FACS_Folder, ssf+'_facs.txt')
                if not os.stat(FACS_file).st_size: continue #If FACS_file is empty
                
                ############--------------Read FACS File
                count = 0
                AU_NumberOccurrence = 0
                with open(FACS_file,'r') as f:
                    
                    for batch in read_by_batch(f):
                        if not count: #Only read the first column
                            if not AU_NumberOccurrence:
                                AUs.append([float(batch)]) 
                            else:
                                AUs[-1].append(float(batch))    
                            AU_NumberOccurrence+=1
                        count+=1
                        if count == 4: count=0 #Because FACS are 4 columns
                
                ############--------------Read Images File                
                Images_file = os.path.join(Images_Folder, ssf+'.png')              
                Images.append(cv.imread(Images_file))                
#                temp_Images.append(cv.imread(Images_file))
                Address.append(Images_file)
                ############--------------Read Landmarks File
                Landmarks_file = os.path.join(Landmarks_Folder, ssf+'_aam.txt')
                s_landmarks = open(Landmarks_file,'r').read().split()
                mat_landmarks = nm.zeros((len(s_landmarks)/2, 2))
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
    return Images, AUs, Landmarks, Address, Draw_Images, Draw_LM   
                
def read_by_batch(fileobj):
    for line in fileobj:
        for batch in line.split():
            yield batch

def draw_circles_landmarks(Image, Landmark, Number1, Number2, nameWindow, filename, all):
    import cv2 as cv 
    import pickle
    drawImage = Image
    with open('Jet_map','r') as f:
        Jet = pickle.load(f)
    if not all: 
        new_LM = [Landmark[Number1]]+[Landmark[Number2]]
        count = 45
    elif all == 1: 
        new_LM = Landmark
        count=0
    elif all == 2:
        new_LM = Landmark[Number1:Number2]
        count=0
    
    for x,y in new_LM:
    #for x,y in Landmark:            #Total 66 landmarks each image.
        cv.circle(drawImage, (int(x),int(y)), 2, tuple(255*px for px in Jet[count]), -1)
        count+=1    
    cv.startWindowThread()
    cv.namedWindow(nameWindow, cv.WINDOW_NORMAL)
    drawImage = cv.resize(drawImage, (350,240))
    cv.imshow(nameWindow,drawImage)  
    cv.imwrite(filename, drawImage)

def check_AUs_Repetitions(AU_Array):
    import numpy as np
    AUs_List = []
    for element in AU_Array:
        for pos in element:
            AUs_List.append(int(pos))
    AUs_repetitions = np.bincount(np.array(AUs_List))
    return AUs_repetitions
    
def getFrame_by_AU(Images, AUs, Landmarks, Address, number_of_AU):
    import numpy as np    
    Training_Images = []
    Training_Landmarks = []
    Test_Images = []
    Test_Landmarks = []
    count = 0
    for element in AUs:
        temp_Images=[]
        temp_Landmarks=[]
        for pos in element:
            if pos==number_of_AU:
                Training_Images.append(Images[count])
                Training_Landmarks.append(Landmarks[count])
                print "AU%d for True Data, from file %s. - count = %d"\
                    %(int(pos), Address[count], count)
                flag = 0
                break
            else:
                if Test_Images and np.array_equiv(Test_Images[-1],Images[count]) and\
                    np.array_equal(Test_Images[-1],Images[count]): 
                        continue
                temp_Images.append(Images[count])
                temp_Landmarks.append(Landmarks[count])
                flag = 1
        #As the same image ould have several AUs, only assign Test images to those
        #images which do not have selected AU
        if flag and temp_Images:
            Test_Images.append(temp_Images[0])
            Test_Landmarks.append(temp_Landmarks[0])
            print "AU%d for False Data, from file %s. - count = %d"\
                %(int(pos), Address[count], count)
        count+=1
    print "Data for TP=%d, data for FN=%d"%(len(Training_Images), len(Test_Images))
    return Training_Images, Training_Landmarks, Test_Images, Test_Landmarks
        