# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 20:42:43 2025

@author: user
"""

import numpy as np
import cv2
from scipy import special

def gamma_correction(f,gamma=2.0):
    c=255.0/(255.0**gamma)
    table=np.clip((np.arange(256)**gamma*c),0,255).astype(np.uint8)
    g=cv2.LUT(f,table)
    return g 

def beta_correction(f,a=2.0,b=2.0):
    x=np.linspace(0,1,256)
    table=np.round(special.betainc(a,b,x)*255,0).astype(np.uint8)
    g=cv2.LUT(f,table)
    return g

def sepia_toing(f):
    g=f.copy()
    nc,nr=f.shape[:2]
    B,G,R=f[:,:,0],f[:,:,1],f[:,:,2]
    gr=np.uint8(np.clip(0.393*R+0.769*G+0.189*B,0,255))
    gg=np.uint8(np.clip(0.329*R+0.686*G+0.168*B,0,255))
    gb=np.uint8(np.clip(0.272*R+0.534*G+0.131*B,0,255))
    g=cv2.merge((gb,gg,gr))
    return g

def sobel_gradient(f):
    if f.ndim!=3:
        kernel_x=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
        kermel_y=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
        gx=cv2.filter2D(f,cv2.CV_32F,kernel_x)
        gy=cv2.filter2D(f,cv2.CV_32F,kermel_y)
        mag=abs(gx)+abs(gy)
        g=np.uint8(np.clip(mag,0,255))
    else:
        temp1=cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        temp2=sobel_gradient(temp1)
        g=cv2.cvtColor(temp2,cv2.COLOR_GRAY2BGR)
    return g

def sobel_edge_detection(f):
    if f.ndim!=3:
        temp=sobel_gradient(f)
        ret,g=cv2.threshold(temp, 0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    else:
        gray=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
        temp=sobel_edge_detection(gray)
        ret,temp=cv2.threshold(temp,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        g=cv2.cvtColor(temp,cv2.COLOR_GRAY2BGR)
    return g

cap=cv2.VideoCapture(r"D:\video_processing\data\Landscape01.mp4")
if not cap.isOpened():
    print("error")
    exit()
    
while True:
    ret,img1=cap.read()
    if not ret:
        break
    img2=gamma_correction(img1)
    img3=beta_correction(img1)
    img4=sobel_edge_detection(img1)
    img5=sepia_toing(img1)
    
    cv2.imshow("Original",img1)
    cv2.imshow("gamma",img2)
    cv2.imshow("beta",img3)
    cv2.imshow("sobel",img4)
    cv2.imshow("sepia",img5)
    if cv2.waitKey(33)&0xFF==27:
        break

cap.release()
cv2.destroyAllWindows()