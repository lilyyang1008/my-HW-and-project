# -*- coding: utf-8 -*-
"""
Created on Wed May 29 16:45:18 2024
https://github.com/qwp8510/Self-driving_Finding_lane/blob/master/Video_Finding_lane/Video_Finding_lane.ipynb
@author: user
"""
import cv2
import numpy as np

# Function to process each frame
def process_frame(frame,value=50):
    #frame = cv2.resize(frame,(1500,800))
    blur = cv2.GaussianBlur(frame,(5,5),0)
    hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    low = np.array([18,90,140])
    high= np.array([48,160,255])
    mask = cv2.inRange(final_hsv,low,high)
    #height,width=mask.shape
    canny = cv2.Canny(mask,30,150)
    height, width = canny.shape
    #mask = np.zeros_like(canny)

    # Only focus lower half of the screen
    polygon = np.array([[
    (0, height * 0.6),
        (width, height * 0.6),
        (width, height),
        (0, height)
    ]], np.int32)
    mask2 = np.zeros_like(canny)
    cv2.fillPoly(mask2, polygon, 255)
    masked_edges = cv2.bitwise_and(mask2, canny)
    
    # Detect lines using Hough Transform
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, 50, minLineLength=100, maxLineGap=150)
    
    # Draw lines on the frame
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    
    
    return frame

# Open the video file
cap = cv2.VideoCapture(r"C:\Users\user\Downloads\road_car_view (online-video-cutter.com).mp4")

# Get the video writer initialized to save the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('D:\\computer_version\\output4.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        processed_frame = process_frame(frame)
        out.write(processed_frame)
        
        # Display the resulting frame (optional)
        cv2.imshow('frame', processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything when done
cap.release()
out.release()
cv2.destroyAllWindows()

#%%
import cv2
import numpy as np
value=50
def save_frame_from_video(video_path, frame_number, output_image_path):
    # 打開視頻文件
    cap = cv2.VideoCapture(video_path)
    
    # 獲取總幀數
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 檢查請求的幀號是否在範圍內
    if frame_number >= total_frames or frame_number < 0:
        print("請求的幀號超出範圍")
        return
    
    # 設置視頻幀的位置
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # 讀取幀
    ret, frame = cap.read()
 
    if ret:
        # 保存幀為圖像
        blur = cv2.GaussianBlur(frame,(5,5),0)
        hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        final_hsv = cv2.merge((h, s, v))
        low = np.array([18,90,140])
        high= np.array([48,160,255])
        mask = cv2.inRange(final_hsv,low,high)
        canny = cv2.Canny(mask,30,150)
        height, width = canny.shape
        polygon = np.array([[
        (0, height * 0.6),
            (width, height * 0.6),
            (width, height),
            (0, height)
        ]], np.int32)
        mask2 = np.zeros_like(canny)
        cv2.fillPoly(mask2, polygon, 255)
        masked_edges = cv2.bitwise_and(mask2, canny)
      
        
        lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, 50, minLineLength=100, maxLineGap=150)
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    result=cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        cv2.imwrite(output_image_path,result)
        print(f"幀 {frame_number} 已保存為 {output_image_path}")
    else:
        print("未能讀取幀")
    
    # 釋放視頻資源
    cap.release()

# 示例使用
video_path = r"C:\Users\user\Downloads\road_car_view (online-video-cutter.com).mp4" # 替換成你的影片路徑
frame_number = 100        # 替換成你想要擷取的幀號
output_image_path = r'D:\computer_version\frame100-2.jpg'  # 輸出的圖像文件路徑

save_frame_from_video(video_path, frame_number, output_image_path)
