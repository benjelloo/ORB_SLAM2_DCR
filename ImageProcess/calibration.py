# Import required modules 
import cv2 
import numpy as np 
import os 
import glob 
  
# Define the dimensions of checkerboard 
CHECKERBOARD = (4,4) 
  
# stop the iteration when specified 
# accuracy, epsilon, is reached or 
# specified number of iterations are completed. 
criteria = (cv2.TERM_CRITERIA_EPS + 
            cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001) 
  
# Vector for 3D points 
threedpoints = [] 
  
# Vector for 2D points 
twodpoints = [] 
  
square_size = 15 # 15*15mm
  
#  3D points real world coordinates 
objectp3d = np.zeros((1, CHECKERBOARD[0]  
                      * CHECKERBOARD[1],  
                      3), np.float32) 
objectp3d[0, :, :2] = (square_size*np.mgrid[0:CHECKERBOARD[0], 
                               0:CHECKERBOARD[1]]).T.reshape(-1, 2)
prev_img_shape = None
  
  
# Extracting path of individual image stored 
# in a given directory. Since no path is 
# specified, it will take current directory 
# jpg files alone 
images = glob.glob('./calibration_resized/*') 
  
for filename in images: 
    img = cv2.imread(filename)
    print(filename)
    
    # Color-segmentation to get binary mask
    lwr = np.array([0, 0, 143])
    upr = np.array([128,128, 252])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    msk = cv2.inRange(hsv, lwr, upr)

    # Extract chess-board
    krn = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 30))
    dlt = cv2.dilate(msk, krn, iterations=5)
    res = 255 - cv2.bitwise_and(dlt, msk)

    # Displaying chess-board features
    res = np.uint8(res)
    ret, corners = cv2.findChessboardCorners(res, CHECKERBOARD,
                                             flags=cv2.CALIB_CB_ADAPTIVE_THRESH +
                                                   cv2.CALIB_CB_FAST_CHECK +
                                                   cv2.CALIB_CB_NORMALIZE_IMAGE)
    cv2.imshow('img', res) 
    cv2.waitKey(0)
    # If desired number of corners can be detected then, 
    # refine the pixel coordinates and display 
    # them on the images of checker board 
    if ret == True: 
        threedpoints.append(objectp3d) 
  
        # Refining pixel coordinates 
        # for given 2d points. 
        corners2 = cv2.cornerSubPix( 
            res, corners, (11, 11), (-1, -1), criteria) 
  
        twodpoints.append(corners2) 
  
        # Draw and display the corners 
        img = cv2.drawChessboardCorners(img,  
                                          CHECKERBOARD,  
                                          corners2, ret) 
  
        cv2.imshow('img', img) 
        cv2.waitKey(0) 
  
cv2.destroyAllWindows() 
  
h, w = img.shape[:2] 
  
  
# Perform camera calibration by 
# passing the value of above found out 3D points (threedpoints) 
# and its corresponding pixel coordinates of the 
# detected corners (twodpoints) 
ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera( 
    threedpoints, twodpoints, res.shape[::-1], None, None) 
  
  
# Displaying required output 
print(" Camera matrix:") 
print(matrix) 
  
print("\n Distortion coefficient:") 
print(distortion) 
  
print("\n Rotation Vectors:") 
print(r_vecs) 
print(len(r_vecs))
  
print("\n Translation Vectors:") 
print(t_vecs) 
print(len(t_vecs))
