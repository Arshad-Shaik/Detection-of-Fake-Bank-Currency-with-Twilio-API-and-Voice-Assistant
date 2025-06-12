import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def get_pixel(img, center, x, y):
    new_value = 0
    try:
        if img[x][y] >= center:
            new_value = 1
    except:
        pass
    return new_value

def lbp_calculated_pixel(img, x, y):
    center = img[x][y]
    val_ar = []
    val_ar.append(get_pixel(img, center, x-1, y+1))     # top_right
    val_ar.append(get_pixel(img, center, x, y+1))       # right
    val_ar.append(get_pixel(img, center, x+1, y+1))     # bottom_right
    val_ar.append(get_pixel(img, center, x+1, y))       # bottom
    val_ar.append(get_pixel(img, center, x+1, y-1))     # bottom_left
    val_ar.append(get_pixel(img, center, x, y-1))       # left
    val_ar.append(get_pixel(img, center, x-1, y-1))     # top_left
    val_ar.append(get_pixel(img, center, x-1, y))       # top
    
    power_val = [1, 2, 4, 8, 16, 32, 64, 128]
    val = 0
    for i in range(len(val_ar)):
        val += val_ar[i] * power_val[i]
    return val    


    
def main():
    filename = 'data/Fake'
    for root, dirs, files in os.walk(filename):
        for fdata in files:
            image_file = root+"/"+fdata;
            img_bgr = cv2.imread(image_file)
            height, width, channel = img_bgr.shape
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            img_lbp = np.zeros((height, width,3), np.uint8)
            for i in range(0, height):
                for j in range(0, width):
                    img_lbp[i, j] = lbp_calculated_pixel(img_gray, i, j)
            cv2.imwrite('LBP/validation/Fake/'+fdata, img_lbp)
            cv2.imwrite('LBP/train/Fake/'+fdata, img_lbp)

    filename = 'data/Real'
    for root, dirs, files in os.walk(filename):
        for fdata in files:
            image_file = root+"/"+fdata;
            img_bgr = cv2.imread(image_file)
            height, width, channel = img_bgr.shape
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            img_lbp = np.zeros((height, width,3), np.uint8)
            for i in range(0, height):
                for j in range(0, width):
                    img_lbp[i, j] = lbp_calculated_pixel(img_gray, i, j)
            cv2.imwrite('LBP/validation/Real/'+fdata, img_lbp)
            cv2.imwrite('LBP/train/Real/'+fdata, img_lbp)
    print("LBP Program is finished")

if __name__ == '__main__':
    main()
