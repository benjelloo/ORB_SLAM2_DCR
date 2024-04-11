# detects circular frame and crops image to that frame

import cv2 as cv
import sys
import os
import numpy as np
from PIL import Image, ImageDraw

def crop(img_path,filename,save_path):
    img = Image.open(img_path) 
    center,radius=find_circles(img_path)
    print(center,radius)
    h,w = img.size
    center = [184,166]
    radius = 178
    feather = 2
    start_pt = [center[0]-radius+feather,center[1]-radius+feather]
    end_pt = [center[0]+radius-feather,center[1]+radius-feather]
    print(start_pt,end_pt)

    for x in range(len(start_pt)):
        if start_pt[x]<0:
            start_pt[x]=0
    
    '''
    # creating luminous image 
    lum_img = Image.new('L',[h,w] ,0)  
    draw = ImageDraw.Draw(lum_img) 
    draw.pieslice([tuple(start_pt),tuple(end_pt)],0,360,fill=255) 
    img_arr = np.array(img) 
    lum_img_arr = np.array(lum_img) 

    final_img_arr = np.dstack((img_arr, lum_img_arr)) 
    
    print("Saved to ",os.path.join(save_path,filename))
    im1 = Image.fromarray(final_img_arr).save(os.path.join(save_path,filename))
    '''
    
    im1 = img.crop((center[0]-int(radius*1.42/2)+feather,center[1]-int(radius*1.42/2)+feather,center[0]+int(radius*1.42/2)-feather,center[1]+int(radius*1.42/2)-feather))
    im1.save(os.path.join(save_path,filename))
    
def find_circles(img):
    #debug
    default_file = "./Output/rgb/00000.png"
    filename = img if len(img) > 0 else default_file

    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_COLOR)

    if src is None:
        print("Error opening image!")
        return;

    gray = cv.cvtColor(src,cv.COLOR_BGR2GRAY)

    gray = cv.medianBlur(gray,5)

    rows = gray.shape[0]
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows/8, param1=100, param2 = 30, minRadius=100, maxRadius=200)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            center = (i[0],i[1])
            cv.circle(src,center,1,(0,100,100),3)
            radius=i[2] 
            print("Detected circle at ",center," with radius ", radius)
            return [(int(i[0]),int(i[1])),int(radius)]
        #cv.imshow("detected circles", src)
        #cv.waitKey(0)
    else:
        print("No circles detected")
    return 0;

if __name__ == "__main__":
    path="./Output/rgb/"
    save_path = "./Output_cropped1/rgb/"
    
    for filename in os.listdir(path):
        f = os.path.join(path,filename)
        if os.path.isfile(f) and int(filename[:-4])<=409: #409 images in the sequence ,hardcoded rn
            print("Opening ",f) 
            crop(f,filename,save_path)
    
