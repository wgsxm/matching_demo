import cv2
import numpy as np
import time
import os
from matplotlib import pyplot as plt

im = cv2.imread("./divider/test.png")
def pre_process(im):
    # 转成灰度图：
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(im_gray, (5, 5), 0)
    _, im_inv = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    processed_im=im_inv
    # cv2.imshow('a',blurred)
    # cv2.imshow('b',im_inv)
    # cv2.waitKey(10000)
    # cv2.destroyAllWindows()
    return processed_im

    

processed_im=pre_process(im)

#计算竖直投影值
vertical_projection = cv2.reduce(processed_im , 0, cv2.REDUCE_SUM, dtype=cv2.CV_32S)
vertical_projection=vertical_projection[0]

plt.plot(vertical_projection)
plt.show()






# # 切割图像:
# contours, hierarchy = cv2.findContours(processed_im,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # 将图像按从左到右进行排序：
# # contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

# result = []

# for contour in contours:
#     x, y, w, h = cv2.boundingRect(contour)
#     box = np.int64([[x, y], [x+w, y], [x+w, y+h], [x, y+h]])
#     result.append(box)

# for box in result:
#     cv2.drawContours(im, [box], 0, (0, 0, 255), 2)
#     roi = processed_im[box[0][1]:box[3][1], box[0][0]:box[1][0]]
#     roistd = cv2.resize(roi, (30, 30))
#     timestamp = int(time.time() * 1e6)
#     filename = "{}.jpg".format(timestamp)
#     filepath = os.path.join("./divider/char", filename)
#     cv2.imwrite(filepath, roistd)

# for box in result:
#    cv2.drawContours(im, [box], 0, (0, 0, 255), 2)



