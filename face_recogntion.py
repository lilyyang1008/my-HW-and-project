# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 14:23:55 2024

@author: user
"""

import cv2
import numpy as np
import os

def face_extraction(database):
    face_cascade=cv2.CascadeClassifier(r"D:\computer_version\Face_Detection\haarcascade_frontalface_alt.xml")
    if database==1:
        filenames=os.listdir(r"D:\computer_version\actor")
    if database==2:
        filenames=os.listdir(r"D:\computer_version\actress")
    n=len(filenames)
    for i in range(n):
        if filenames[i][-3:]=="jpg":
            print(filenames[i])
            if database==1:
                #pathname="D://computer_version//actor//"+filenames[i]
                pathname=os.path.join(r"D:\computer_version\actor", filenames[i])
            if database==2:
                #pathname="D://computer_version//actress//"+filenames[i]
                pathname=os.path.join(r"D:\computer_version\actress", filenames[i])
            #print("pathname=",pathname)
            img=cv2.imread(pathname,-1)
            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            face=face_cascade.detectMultiScale(gray,1.1,5,minSize=(30,30))

            if len(face)==1:
                for(x,y,w,h) in face:
                    ROI=gray[y:y+h+1,x:x+w+1]
                    ROI=cv2.resize(ROI,(200,200),cv2.INTER_LINEAR)
                
                else:
                    idx=np.argmax(face[:,2])
                    (x,y,w,h)=face[idx]
                    ROI=gray[y:y+h+1,x:x+w+1]
                    ROI=cv2.resize(ROI,(200,200),cv2.INTER_LINEAR)
                        
            if database==1:
                #filenameface="D://computer_version//actor//face//"+filenames[i][:-4]+".bmp"
                filenameface=os.path.join(r"D:\computer_version\actor\face",filenames[i][:-4]+".bmp")
            if database==2:
                #filenameface="D://computer_version//actress//face//"+filenames[i][:-4]+".bmp"
                filenameface=os.path.join(r"D:\computer_version\actress\face",filenames[i][:-4]+".bmp")
            #print("filenameface=",filenameface)
            cv2.imwrite(filenameface,ROI)
#face_extraction(1)
face_extraction(2)
#%%   
def face_recognition(f, database):
    face_cascade = cv2.CascadeClassifier(r"D:\computer_version\Face_Detection\haarcascade_frontalface_alt.xml")
    
    if database == 1:
        folder = r"D:\computer_version\actor\face"
    elif database == 2:
        folder = r"D:\computer_version\actress\face"
    else:
        print("Invalid database option")
        return
    
    filenames = os.listdir(folder)
    
    images = []
    labels = []
    
    # 讀取所有圖片並為每個人賦予標籤
    for i, filename in enumerate(filenames):
        if filename.endswith(".bmp"):  # 或其他格式
            pathname = os.path.join(folder, filename)
            img = cv2.imread(pathname, cv2.IMREAD_GRAYSCALE)
            if img is None:
                print(f"Error: Unable to read {pathname}")
                continue
            images.append(img)
            labels.append(i)  # 這裡使用 `i` 作為標籤，表示每個文件對應一個不同的人
    if len(images) < 2:
        print("Error: Not enough training data. You need at least two images for training.")
        return
    # 訓練識別模型
    model = cv2.face.EigenFaceRecognizer_create()
    model.train(images, np.array(labels))  # 使用標籤來訓練模型

    # 顯示所有識別類別
    classnames = filenames
    for k in range(len(filenames)):
        classnames[k] = classnames[k][:-4]  # 去掉 .bmp 擴展名
    
    return model, classnames

def face_recognition_(f,face_cascade,model,classnames):
    g=f.copy()
    gray=cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    face=face_cascade.detectMultiScale(gray,1.1,5,minSize=(30,30))
    if len(face)!=0:
        if len(face)==1:
            for (x,y,w,h) in face:
                ROI=gray[y:y+h+1,x:x+w+1]
            ROI=cv2.resize(ROI,(200,200),cv2.INTER_LINEAR)
        else:
            idx=np.argmax(face[:,2])
            (x,y,w,h)=face[idx]
            ROI=gray[y:y+h+1,x:x+w+1]
            ROI=cv2.resize(ROI,(200,200),cv2.INTER_LINEAR)
        predict=model.predict(ROI)
        label=classnames[predict[0]]
        if w<500:
            font=cv2.FONT_HERSHEY_COMPLEX_SMALL
        else:
            font=cv2.FONT_HERSHEY_TRIPLEX
        labelsize=cv2.getTextSize(label, font, fontScale=1.0, thickness=1)
        text_width,test_height=labelsize[0][0],labelsize[0][1]
        cv2.rectangle(g, (x,y), (x+w,x+h),(255,0,0),2)
        cv2.rectangle(g,(x,y-2), (x+w,x+h),(255,255,255),1)
        cv2.putText(g, label, (x,y-2), font, 1.0,(255,255,255),1)
    return g

img1=cv2.imread(r"D:\computer_version\image\1.jpg",-1)
if img1 is None:
    print("Error: Image not found.")
else:
    model, classnames = face_recognition(img1, 2)

    # 確保返回的模型是有效的

    if model is not None:
        face_cascade = cv2.CascadeClassifier(r"D:\computer_version\Face_Detection\haarcascade_frontalface_alt.xml")
        img2 = face_recognition_(img1, face_cascade, model, classnames)
        if img2 is not None and img2.any():  # 確保 img2 是有效的
            cv2.imshow("face recognition", img2)
            cv2.waitKey(0)
        else:
            print("Error: Failed to process face recognition.")
    else:
        print("Error: Model not trained.")
        

