# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 13:56:23 2024

@author: user
"""

import numpy as np
import cv2
#%%
def sobel_gradient(f):
    if f.ndim!=3:
        kernel_x=np.array([[-1,-2,-1],[0,0,0,],[1,2,1]])
        kernel_y=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
        gx=cv2.filter2D(f,cv2.CV_32F,kernel_x)
        gy=cv2.filter2D(f,cv2.CV_32F,kernel_y)
        mag=abs(gx)+abs(gy)
        g = np.uint8(np.clip(mag, 0, 255))
    else:
        temp1=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
        temp2=sobel_gradient(temp1)
        g=cv2.cvtColor(temp2, cv2.COLOR_GRAY2BGR)
        
    return g


def sobel_gradient_detection(f):
    if f.ndim!=3:
        kernel_x=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
        kernel_y=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
        gx=cv2.filter2D(f,cv2.CV_32F,kernel_x)
        gy=cv2.filter2D(f,cv2.CV_32F,kernel_y)
        angle=np.arctan2(gy,gx)
        angle=np.where(angle<0,angle+2*np.pi,angle)
        grad_dir=angle*255/(2*np.pi)
        g=np.uint8(np.clip(grad_dir,0,255))
    else:
        temp1=cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        temp2=sobel_gradient_detection(temp1)
        g=cv2.cvtColor(temp2, cv2.COLOR_GRAY2BGR)
    return g

def sobel_edge_detection(f):
    if f.ndim!=3:
        temp=sobel_gradient(f)
        ret,g=cv2.threshold(temp,0,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    else:
        gray=cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        temp=sobel_gradient(gray)
        ret,temp=cv2.threshold(temp,0,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        g=cv2.cvtColor(temp, cv2.COLOR_GRAY2BGR)
    return g

             
def canny_edge_detection(f,low_thresh,high_thresh,filter_size):
    if f.ndim!=3:
        g=cv2.Canny(f, low_thresh, filter_size)
    else:
        gray=cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        g=cv2.Canny(gray, low_thresh, high_thresh, filter_size)
    return g

def k_means_segmentation(f,k):
    z=f.reshape(-1,3).astype(np.float32)
    criteria=(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,10,1.0)
    ret,label,center=cv2.kmeans(z, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center=np.uint8(center)
    result=center[label.flatten()]
    g=result.reshape(f.shape)
    return g
#%%
img1=cv2.imread(r"D:\computer_version\image\Osaka.bmp",-1)
cv2.imshow("original",img1)
img2=sobel_gradient(img1)
cv2.imshow("sobel gradient", img2)
img3=sobel_edge_detection(img1)
cv2.imshow("sobel edge detection",img3)
img4=canny_edge_detection(f=img1, low_thresh=10, high_thresh=250, filter_size=3)
cv2.imshow("canny", img4)
img5=k_means_segmentation(img1, 2)
cv2.imshow("k means segmentation", img5)
cv2.waitKey(0)