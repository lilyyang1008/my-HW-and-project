import numpy as np
import cv2
cap=cv2.VideoCapture(r"D:\video_processing\data\Akiyo.avi")
ret,frame1=cap.read()
gray1=cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
nr,nc=frame1.shape[:2]
block_size=16
while True:
    ret,frame2=cap.read()
    if not ret:
        break
    result=frame1.copy()
    gray2=cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    flow=cv2.calcOpticalFlowFarneback(gray1,gray2,None,0.5,3,15,3,5,1.2,0)
    for x in range(0,nr,block_size):
        for y in range(0,nc,block_size):
            cv2.circle(result,(y,x),1,(0,0,255),1,-1)
            u=int(round(x+flow[x,y][0]*5))
            v=int(round(y+flow[x,y][1]*5))
            cv2.line(result,(y,x),(v,u),(215,0,0),1)

    cv2.imshow("original",frame1)
    cv2.imshow("result",result)
    if cv2.waitKey(33)&0xFF==27:
        break
    frame1=frame2.copy()
    gray1=gray2.copy()
cap.release()
cv2.destroyAllWindows()