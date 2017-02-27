# -*- coding: cp936 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt
################################################################################

print 'Load Object Cascade Classifier'

faceCascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt.xml')
lefteyeCascade = cv2.CascadeClassifier('./haarcascades/haarcascade_mcs_lefteye.xml')
righteyeCascade = cv2.CascadeClassifier('./haarcascades/haarcascade_mcs_righteye.xml')
noseCascade = cv2.CascadeClassifier('./haarcascades/haarcascade_mcs_nose.xml')
mouthCascade = cv2.CascadeClassifier('./haarcascades/haarcascade_mcs_mouth.xml')
################################################################################

print 'Load Image'

imgFile = '5.jpg'

def nothing(x):
    pass

cv2.namedWindow('image')
#cv2.createTrackbar('minSzie','image',0,255,nothing)
#cv2.createTrackbar('maxSize','image',0,255,nothing)
#cv2.createTrackbar('minNeighbors','image',0,255,nothing)

cap = cv2.VideoCapture(0)
while(1):
    ret, img = cap.read()
    #img=cv2.imread(imgFile)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgGray=cv2.equalizeHist(imgGray)
    #faces = faceCascade.detectMultiScale(imgGray, scaleFactor = 1.3, minNeighbors = 4, minSize = (60,60), maxSize = (300,300), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    faces = faceCascade.detectMultiScale(imgGray, 1.3, 5)
    for (x,y,w,h) in faces:
        centerX=x+w/2
        centerY=y+h/2
        #print centerX,centerY
        #cv2.circle(img,(centerX,centerY),3,(0,0,0))
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        
        faceGray = imgGray[y:y+h, x:x+w]
        faceColor = img[y:y+h, x:x+w]
        
        
        # for small Alice
        lefteye = lefteyeCascade.detectMultiScale(faceGray, scaleFactor = 1.1, minNeighbors = 16, minSize = (10,0), maxSize = (80,80), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        righteye = righteyeCascade.detectMultiScale(faceGray, scaleFactor = 1.1, minNeighbors = 16, minSize = (10,10), maxSize = (80,80), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        # cannot search nose successfully!
        nose = noseCascade.detectMultiScale(faceGray, scaleFactor = 1.3, minNeighbors = 5, minSize = (20,20), maxSize = (80,80), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)        
        # mistaken eye for mouth!
        mouth = mouthCascade.detectMultiScale(faceGray, scaleFactor = 1.3, minNeighbors = 16, minSize = (20,20), maxSize = (80,80), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        
            
        leftX=0
        leftY=0
        rightX=0
        rightY=0
        noseX=0
        noseY=0
        mounthX=0
        mounthY=0
        for (ex,ey,ew,eh) in lefteye:
            leftX=x+ex+ew/2
            leftY=y+ey+eh/2
            if leftY<centerY and leftX<centerX:
                cv2.rectangle(faceColor, (ex,ey), (ex+ew,ey+eh), (0,255,0), 2)
                break
        
        for (ex,ey,ew,eh) in righteye:
            rightX=x+ex+ew/2
            rightY=y+ey+eh/2
            if rightY<centerY and rightX>centerX:
                cv2.rectangle(faceColor, (ex,ey), (ex+ew,ey+eh), (255,255,0), 2)
                break

        for (ex,ey,ew,eh) in mouth:
            mounthX=x+ex+ew/2
            mounthY=y+ey+eh/2
            if mounthY>centerY:
                cv2.rectangle(faceColor, (ex,ey), (ex+ew,ey+eh), (0,100,100), 2)
                break

        for (ex,ey,ew,eh) in nose:
            noseX=x+ex+ew/2
            noseY=y+ey+eh/2
            if  mounthY!=0 and rightY!=0 and leftY!=0:
                if noseY<mounthY and noseY>leftY and noseY>rightY and noseX>leftX and noseX<rightX:
                    cv2.rectangle(faceColor, (ex,ey), (ex+ew,ey+eh), (0,255,255), 2)
                break
            elif  mounthY!=0 and rightY!=0:
                if noseY<mounthY and noseY>rightY and noseX<rightX:
                    cv2.rectangle(faceColor, (ex,ey), (ex+ew,ey+eh), (0,255,255), 2)
                break
            elif  mounthY!=0 and leftY!=0:
                if noseY<mounthY and noseY>leftY and noseX>leftX:
                    cv2.rectangle(faceColor, (ex,ey), (ex+ew,ey+eh), (0,255,255), 2)
                break

        print "左眼：(",leftX,",",leftY,")\n"
        print "右眼：(",rightX,",",rightY,")\n"
        print "鼻子：(",noseX,",",noseY,")\n"
        print "嘴巴：(",mounthX,",",mounthY,")\n\n"
        
    
    cv2.imshow('image',img)
    if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()           
print 'finish!'
