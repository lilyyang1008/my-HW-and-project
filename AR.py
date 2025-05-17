# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 15:39:41 2024

@author: user
"""
import cv2
import numpy as np

#Perspective Transformation    
def paste_polygon(f,g,polygon_x,polygon_y):
    nr1,nc1=f.shape[:2]
    nr2,nc2=g.shape[:2]
    pts1=np.float32([[0,0],[0,nr1],[nc1,nr1],[nc1,0]])#4 pair of control point
    pts2=np.float32([ [polygon_y[0],polygon_x[0]],[polygon_y[1],polygon_x[1]],
                     [polygon_y[2],polygon_x[2]],[polygon_y[3],polygon_x[3]] ])
                     
    blank=f.copy()
    blank.fill(255)
    neg_img=np.zeros([nr2,nc2,0],dtype=np.uint8)
    cpy_img=np.zeros([nr2,nc2,0],dtype=np.uint8)
    warp_matrix=cv2.getPerspectiveTransform(pts1,pts2)
    neg_img=cv2.warpPerspective(f, warp_matrix,(nc2,nr2),cv2.INTER_CUBIC)
    cpy_img=cv2.warpPerspective(blank,warp_matrix,(nc2,nr2),cv2.INTER_CUBIC)
    cv2.bitwise_not(cpy_img,cpy_img)
    cv2.bitwise_and(cpy_img,g,cpy_img)
    cv2.bitwise_or(cpy_img,neg_img,g)
    
def AR_TV_show(f,g,ar_show=1):
    if ar_show==1:
        pt_x=[220,377,380,220]
        pt_y=[275,273,535,535]
        paste_polygon(f, g, pt_x, pt_y)
    if ar_show==2:
        pt_x=[90,292,310,40]
        pt_y=[357,360,735,740]
        paste_polygon(f, g, pt_x, pt_y)
    if ar_show==3:
        pt_x=[190,440,405,220]
        pt_y=[45,45,310,310]
        paste_polygon(f, g, pt_x, pt_y)        

ar_show=eval(input("請輸入AR_show(1,2,3):"))
path1=input("請輸入影片路徑:").strip()
path2=input("請輸入儲存路徑:").strip()


cap=cv2.VideoCapture(path1)
if not cap.isOpened():
    exit()

if ar_show==1:
    background=cv2.imread(r"D:\video_processing\HW2\Background1.bmp",-1)

elif ar_show==2:
    background=cv2.imread(r"D:\video_processing\HW2\Background2.bmp",-1)

elif ar_show==3:
    background=cv2.imread(r"D:\video_processing\HW2\Background3.bmp",-1)

else:
    print("請重新輸入1,2或3")
    ar_show=eval(input("請輸入AR_show(1,2,3):"))

print(background.shape[0],background.shape[1])
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out=cv2.VideoWriter(path2,fourcc,30,(background.shape[1],background.shape[0]))
while True:
    ret,frame=cap.read()
    if not ret:
        break
    img=background.copy()
    AR_TV_show(frame,img,ar_show)
    
    cv2.imshow("example",img)
    out.write(img)
    if cv2.waitKey(33)==27:
        #33ms=30fps,27=ESC
        break
cap.release()
out.release()
cv2.destroyAllWindows()


