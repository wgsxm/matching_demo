import cv2
import numpy as np
import time
import os
from matplotlib import pyplot as plt


def pre_process(im):
    # 转成灰度图：
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(im_gray, (5, 5), 0)
    _, im_inv = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    processed_im=im_inv
    return processed_im

def list_blur(ls,kernel):
    ls_=ls[:]
    if kernel<len(ls_):
        for index in range(kernel,len(ls_)-1-kernel):
            ls_[index]=sum(ls_[index-kernel:index+kernel+1])/(2*kernel+1)
    return ls_

def divider(im):
    magic_num=0.07
    white = []  # 记录每一列的白色像素总和
    height = im.shape[0]
    width = im.shape[1]
    white_max = 0
    sum=0
    for i in range(width):
        s = 0
        for j in range(height):
            if im[j][i] == 255:
                s = s + 1
            white_max = max(white_max, s)
        sum+=s
        white.append(s)
    ave_num=(sum/width)/white_max
    white=list_blur(white,2)
    
    def find_end(start_):
        cer=False
        for i in range(start_ + 1, width - 1):
            if white[i] < magic_num * white_max:
                if cer:
                    if i-start_>5:
                        return i
                    else:
                        return find_end(i)
            elif white[i]>ave_num*white_max:
                cer=True
        return width-1     
    start = 1
    n = 1
    end = 2
    res=[]
    while n < width - 2:
        n = n + 1
        if white[n] > ave_num * white_max:
            start = n
            end =find_end(start)
            n=end 
            cut = im[1:height, start:end]
            res.append(cut)
    return res

filepath="./captcha_generator/captcha"
image_list=os.listdir(filepath)
error=0
for item in image_list:
    im=cv2.imread(filepath+'/'+item)
    cuts=divider(pre_process(im))
    if len(cuts)!=4:
        error+=1

print(1-error/len(image_list),"times:",len(image_list),sep=' ')
