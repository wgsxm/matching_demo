import cv2
import numpy as np
import time
import os

# cv2.imread(filepath)
im = cv2.imread("./codes/a9H1.png")

# 转成灰度图：
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(im_gray, (5, 5), 0)
# kernel = 1/16*np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
# blurred = cv2.filter2D(im_gray, -1, kernel)
# 二值化：
# 非自适应阈值二值化：
_, im_inv = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# 自适应阈值二值化：
# im_inv = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# 运用高斯模糊降噪：

kernel = 1/16*np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
im_blur = cv2.filter2D(im_inv, -1, kernel)


_, im_res = cv2.threshold(im_blur, 127, 255, cv2.THRESH_BINARY)

# 腐蚀(去除一些小物体，或者是粘连物体)

# kernel1 = np.ones((2, 2), np.uint8)
# erosion = cv2.erode(im_res, kernel1, iterations=1)

# 将字符连接部分膨胀处理
kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
dilated = cv2.dilate(im_res, kernel2, iterations=1)

# cv2.imshow("image", dilated)
# cv2.waitKey(0)

# 切割图像:
contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 将图像按从左到右进行排序：
# contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

result = []

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    box = np.int64([[x, y], [x+w, y], [x+w, y+h], [x, y+h]])
    result.append(box)

for box in result:
    cv2.drawContours(im, [box], 0, (0, 0, 255), 2)
    roi = dilated[box[0][1]:box[3][1], box[0][0]:box[1][0]]
    roistd = cv2.resize(roi, (30, 30))
    timestamp = int(time.time() * 1e6)
    filename = "{}.jpg".format(timestamp)
    filepath = os.path.join("./char", filename)  # char文件夹用于存放训练文件
    cv2.imwrite(filepath, roistd)





