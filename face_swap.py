# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 14:44:48 2024
Face swap
@author: user
"""

import numpy as np
import cv2

def applyAffineTransform( src, srcTri, dstTri, size ):

	# Given a pair of triangles, find the affine transform
	warpMat = cv2.getAffineTransform( np.float32( srcTri ), np.float32( dstTri ) )

	# Apply the Affine Transform just found to the src image
	dst = cv2.warpAffine( src, warpMat, ( size[0], size[1] ), None, flags = cv2.INTER_LINEAR, borderMode = cv2.BORDER_REFLECT_101 )

	return dst


def rectContains( rect, point ):

	if point[0] < rect[0]:
		return False
	elif point[1] < rect[1]:
		return False
	elif point[0] > rect[0] + rect[2]:
		return False
	elif point[1] > rect[1] + rect[3]:
		return False
	return True


def calculateDelaunayTriangles( rect, points ):

	subdiv = cv2.Subdiv2D( rect )

	# Insert points into subdiv
	for p in points:
		subdiv.insert( p ) 

	triangleList = subdiv.getTriangleList()

	delaunayTri = []
	pt = []

	for t in triangleList:
		pt.append( ( t[0], t[1] ) )
		pt.append( ( t[2], t[3] ) )
		pt.append( ( t[4], t[5] ) )

		pt1 = ( t[0], t[1] )
		pt2 = ( t[2], t[3] )
		pt3 = ( t[4], t[5] )

		if rectContains( rect, pt1 ) and rectContains( rect, pt2 ) and rectContains( rect, pt3 ):

			ind = []
			for j in range( 3 ):
				for k in range( len( points ) ):
					if abs( pt[j][0] - points[k][0] ) < 1.0 and abs( pt[j][1] - points[k][1] ) < 1.0:
						ind.append( k )

			if len( ind ) == 3:
				delaunayTri.append( ( ind[0], ind[1], ind[2] ) )

		pt = []

	return delaunayTri


def warpTriangle( img1, img2, t1, t2 ):

	# Find bounding rectangle for each triangle
	r1 = cv2.boundingRect( np.float32( [t1] ) )
	r2 = cv2.boundingRect( np.float32( [t2] ) )

	# Offset points by left top corner of the respective rectangles
	t1Rect = []
	t2Rect = []
	t2RectInt = []

	for i in range( 3 ):
		t1Rect.append( ( ( t1[i][0] - r1[0] ), ( t1[i][1] - r1[1] ) ) )
		t2Rect.append( ( ( t2[i][0] - r2[0] ), ( t2[i][1] - r2[1] ) ) )
		t2RectInt.append( ( ( t2[i][0] - r2[0] ), ( t2[i][1] - r2[1] ) ) )

	# Get mask by filling triangle
	mask = np.zeros( ( r2[3], r2[2], 3 ), dtype = np.float32 )
	cv2.fillConvexPoly( mask, np.int32( t2RectInt ), ( 1.0, 1.0, 1.0 ), 16, 0 )

	# Apply warpImage to small rectangular patches
	img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]

	size = ( r2[2], r2[3] )
	img2Rect = applyAffineTransform( img1Rect, t1Rect, t2Rect, size )
	img2Rect = img2Rect * mask

	# Copy triangular region of the rectangular patch to the output image
	img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] * ( ( 1.0, 1.0, 1.0 ) - mask )
	img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] + img2Rect



def face_swap(f1,f2):
    g=f2.copy()
    face_cascade=cv2.CascadeClassifier(r"D:\computer_version\Face_Detection\haarcascade_frontalface_alt.xml")
    facemark=cv2.face.createFacemarkLBF()
    #facemark=cv2.face.LBPHFaceRecognizer_create()
    facemark.loadModel(r"D:\computer_version\Face_Detection\lbfmodel.yaml")
    face1=face_cascade.detectMultiScale(f1,1.1,5,minSize=(30,30))
    face2=face_cascade.detectMultiScale(f2,1.1,5,minSize=(30,30))
    
    if len(face1):
        status1,landmarks1=facemark.fit(f1,face1)
    if len(face2):
            status2,landmarks2=facemark.fit(f2,face2)
    if not status1 or not status2:
        return g
    points1=landmarks1[0][0]
    points2=landmarks2[0][0]
    
    #find conves hull
    hull1=[]
    hull2=[]
    hullIndex=cv2.convexHull(np.array(points2),returnPoints=False)
    #****
    for i in range(len(hullIndex)):
        hull1.append(points1[int(hullIndex[i])])
        hull2.append(points2[int(hullIndex[i])])
        
    #find delunay tringulation
    sizeImg2=f2.shape
    rect=(0,0,sizeImg2[1],sizeImg2[0])
    dt=calculateDelaunayTriangles(rect,hull2)
    
    for i in range(len(dt)):
        t1=[]
        t2=[]
        for j in range(3):
            t1.append(hull1[dt[i][j]])
            t2.append(hull2[dt[i][j]])
        warpTriangle(f1,g,t1,t2)
        
    #calculate mask
    hull8U=[]
    for i in range(len(hull2)):
        hull8U.append((hull2[i][0],hull2[i][1]))

    mask=np.zeros(f2.shape,dtype=f2.dtype)
    cv2.fillConvexPoly(mask, np.int32(hull8U), (255,255,255))  
    
    r=cv2.boundingRect(np.float32([hull2]))
    center=((r[0]+int(r[2]/2),r[1]+int(r[3]/2)))
    
    g=cv2.seamlessClone(np.uint8(g), f2, mask, center, cv2.NORMAL_CLONE)
    return g 

img1=cv2.imread(r"D:\computer_version\image\Girl1.jpg",-1)
img2=cv2.imread(r"D:\computer_version\image\1.jpg",-1)
img3=face_swap(img1, img2) 
cv2.imshow("after", img3)
cv2.waitKey(0)    
    