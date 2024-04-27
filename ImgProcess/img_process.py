import cv2
import numpy as np
import os

# Camera Settings
fps = 30
resizeWidth  = 700
resizeHeigth = 493
frameSize = (resizeWidth, resizeHeigth)

# Output Paths
output_name = "Output"
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
im_path = os.path.join(__location__, output_name + "\\rgb")
txt_path = os.path.join(__location__, output_name)

read_path = os.path.join(__location__, "vid")

if not os.path.exists(im_path):
    os.makedirs(im_path)

def contrast_lab(img):
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(1,1))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)

    # Stacking the original image with the enhanced image
    result = np.hstack((img, enhanced_img))

    return enhanced_img

def contrast_weighted(img):
    contrast = 1.2
    brightness = 0

    return cv2.addWeighted(img, contrast, img, 0, brightness)

with open(txt_path + "\\rgb.txt", 'w') as f:

    f.writelines(["# color images\n", f"# file: '{output_name}.bag'\n", "# timestamp filename\n"])

    i = 0
    while True:

        if not os.path.exists(read_path + "\\" + str(i + 1) + ".png"):
            break

        frame = cv2.imread(read_path + "\\" + str(i + 1) + ".png")

        frame = cv2.resize(frame, frameSize)

        frame = contrast_weighted(frame)

        timestamp = ('%.6f' % (i / fps)).zfill(17)
        imgNumber = str(i).zfill(5)
        frameFileName = str(f'{imgNumber}.png')
        print(frameFileName)
        cv2.imwrite(im_path + "\\" + frameFileName, frame)
        cv2.imshow('Video', frame)
        
        f.write(f"{timestamp} rgb/{frameFileName}\n")
    
        # key controller
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
    
        i += 1

cv2.destroyAllWindows()
