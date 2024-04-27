import cv2
import numpy as np
import os

resizeWidth  = 700
resizeHeigth = 493
imgSize = (resizeWidth, resizeHeigth)

# Output Paths
output_name = "Output"
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
im_path = os.path.join(__location__, "calibration_imgs")
resize_path = os.path.join(__location__, "calibration_resized")
 
if not os.path.exists(resize_path):
    os.makedirs(resize_path)

dir_cont = os.listdir(im_path)

for x in dir_cont:

    if not x.endswith(".png"):
        continue
        
    img = cv2.imread(im_path + "\\" + x)

    img = cv2.resize(img, imgSize)

    
    cv2.imwrite(resize_path + "\\" + x, img)