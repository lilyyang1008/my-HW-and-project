import numpy as np
import cv2

def draw_targert(f,pt,size,color):
    cv2.line(f,(pt[0]-size//2,pt[1]),(pt[0]+size//2,pt[1]),color,1,0,0)
    cv2.line(f,(pt[0],pt[1]-size//2),(pt[0],pt[1]+size//2),color,1,0,0)
    cv2.circle(f,pt,size//2-size//6,color,1,0,0)

def HSV_region_tracking(f,H1,H2,S1,S2,V1,V2):
    g=f.copy()
    nr,nc=f.shape[:2]
    hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)

    if H1>H2:
        low=np.array([H1/2,S1*2.55,V1*2.55])
        high=np.array([180.0,S2*2.55,V2*2.55])
        mask1=cv2.inRange(hsv,low,high)
         
        low=np.array([0.0,S1*2,55,V1*2.55])
        high=np.array([H2/2.0,S2*2.55,V2*2.55])
        mask2=cv2.inRange(hsv,low,high)
        mask=mask1|mask2

    else:
        low=np.array([H1/2,S1*2.55,V1*2.55])
        high=np.array([H2/2,S2*2.55,V2*2.55])
        mask1=cv2.inRange(hsv,low,high)
    #選取最大區域
    (n,labels,stats,centriods)=cv2.connectedComponentsWithStats(mask)

    max_idx,max_area=0,0
    for i in range(1,n):
        area=stats[i,cv2.CC_STAT_AREA]
        if max_area<area:
            max_area=area
            max_idx=i
            
    track_x,track_y=0,0
    #最大區域不是背景區域
    if max_idx!=0:
        temp=np.where(labels==max_idx,np.uint8(255),np.uint8(0))
        (track_x,track_y)=np.int16(centriods[max_idx])
    #設定追蹤區域顏色
    #紅色
    if H1>H2:
        R,G,B=255,0,0
    else:
        H=(H1+H2)//2
        #黃
        if H>=30 and H<90:
            R,G,B=255,255,0
        #綠
        elif H>=90 and H<150:
            R,G,B=0,255,0
        #青
        elif H>=150 and H<210:
            R,G,B=0,255,255
        #藍
        elif H>=210 and H<270:
            R,G,B=0,0,255
        #紫紅
        else:
            R,G,B=255,0,255
    #顯示追蹤目標    
    if max_idx!=0:
        g[:,:,0]=np.where(temp==255,B,g[:,:,0])
        g[:,:,1]=np.where(temp==255,G,g[:,:,1])
        g[:,:,2]=np.where(temp==255,R,g[:,:,2])
        draw_targert(g,(track_x,track_y),40,(255,255,255))
    return g,track_x,track_y

cap=cv2.VideoCapture(r"D:\video_processing\data\Car_Race.mp4")
if not cap.isOpened():
    print("Error: could not open video")
    exit()

while True:
    ret,img1=cap.read()
    if not ret:
        break
    #追蹤紅色區域
    img2,track_x,track_y=HSV_region_tracking(img1,330,30,30,100,30,100)
    cv2.imshow("Video",img1)
    cv2.imshow("Video tracking",img2)
    if cv2.waitKey(33)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()
