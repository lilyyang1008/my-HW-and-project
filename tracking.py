# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 23:26:07 2025

@author: user
"""

import cv2

path1=input("please input the video path:").strip()
path2=input("please input the path to save the outcome:").strip()
types =input("please input the tracking type(CSRT/KCF):").strip()

def tracking(path_in,tracker_type,path_out):
    while tracker_type:
        if tracker_type=="CSRT":
            tracker=cv2.legacy.TrackerCSRT_create()
            break
        elif tracker_type=="KCF":
            tracker=cv2.legacy.TrackerKCF_create()
            break
        else:
            tracker_type=input("please input the tracking type(CSRT/KCF)").strip()
    cap=cv2.VideoCapture(path1)
    if not cap.isOpened():
        print("error:could not open video")
        exit()
        
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read first frame.")
        exit()
    area = cv2.selectROI("Select ROI", frame, showCrosshair=False, fromCenter=False)
    cv2.destroyWindow("Select ROI")
    area = tuple(map(float, area))
    ok=tracker.init(frame, area)
    if not ok:
        print("Error: Tracker initialization failed.")
        exit()
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(path2,fourcc, fps, (width, height))
    while True:
        ret,frame=cap.read()
        if not ret:
            break
    
        success,bbox=tracker.update(frame)
        if success:
            p1=(int(bbox[0]),int(bbox[1]))
            p2=(int(bbox[0]+bbox[2]),int(bbox[1]+bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 3)
        else:
            cv2.putText(frame,"Tracking Failure",(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
        cv2.imshow("video",frame)
        out.write(frame)
        if cv2.waitKey(1)&0xFF==27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


tracking(path1,types,path2)


#%%
import cv2


def save_frame(video_path, frame_number, output_image_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"無法開啟影片: {video_path}")
        return
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_number >= total:
        print(f"frame_number 超出範圍（影片只有 {total} 幀）")
        cap.release()
        return
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_image_path, frame)
        print(f"已儲存: {output_image_path}")
    else:
        print(f"讀取 frame {frame_number} 失敗於: {video_path}")
    cap.release()

num=[0,50,100,150,200,250]
for i in num:
    save_frame(r"D:\video_processing\HW3\VOT-Ball-CSRT.mp4",i,f"D:\\video_processing\\HW3\\VOT-Ball-CSRT-{i}.jpg")
    save_frame(r"D:\video_processing\HW3\VOT-Car-CSRT.mp4",i,f"D:\\video_processing\\HW3\\VOT-Car-CSRT-{i}.jpg")
    save_frame(r"D:\video_processing\HW3\VOT-Ball-KCF.mp4",i,f"D:\\video_processing\\HW3\\VOT-Ball-KCF-{i}.jpg")
    save_frame(r"D:\video_processing\HW3\VOT-Car-KCF.mp4",i,f"D:\\video_processing\\HW3\\VOT-Car-KCF-{i}.jpg")