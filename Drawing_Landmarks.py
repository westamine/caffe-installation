# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 09:56:09 2015

@author: afromero
"""

import cv2 as cv
import pickle

#number = 1
#
#if Binary_Annotations[number]:
#    s = 'AU12'
#else:
#    s = 'No AU12'        
#text = "Annotation: %s"%(s)
#
#draw_annotations(Images[number], groundtruth[number], box[number], 'Face', text, 'test_NO_AU.png')

def draw_annotations(Image, points, rect, nameWindow, set_text, filename):
    
    fontFace = cv.FONT_HERSHEY_SCRIPT_SIMPLEX;
    fontScale = 0.6;
    thickness = 1;    
    
    drawImage = Image.copy()
    with open('Jet_map','r') as f:
        Jet = pickle.load(f)
        
    count = 0
    for x,y in points:
    #for x,y in Landmark:            #Total 66 landmarks each image.
        cv.circle(drawImage, (int(x),int(y)), 1, tuple(255*px for px in Jet[count+45]), -1)
        cv.rectangle(drawImage, (rect[count][0],rect[count][1]), \
                (rect[count][2],rect[count][3]), (0,255,0), 1)
        count+=1
    cv.putText(drawImage, text, (10,40), fontFace, fontScale,(255, 255, 255), thickness, -1)
    cv.startWindowThread()
    cv.namedWindow(nameWindow, cv.WINDOW_NORMAL)
    drawImage = cv.resize(drawImage, (350,240))
    cv.imshow(nameWindow,drawImage)  
    cv.imwrite(filename, drawImage)



def draw_circles_landmarks(Image, Landmark, Number1, Number2, nameWindow, filename, all):
    
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
            draw_circles_landmarks(Images_Draw[show][0][batch], \
                  LM_Draw[show][0][batch], LM[show][0], LM[show][1], 'Demo',\
                  outName_images_file+str(count).zfill(3)+'.png', order[show])
            count+=1
        count = 0     
