# some issues in my machine with ros
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')

import cv2
from decode import decode
import numpy as np
import time
import pytesseract
from imutils.object_detection import non_max_suppression

new_H = 160
new_W = 160

orig = cv2.imread("images/test2.jpeg",1)
H,W = orig.shape[:2]
rH = H/new_H
rW = W/new_W
img = cv2.resize(orig,(new_H,new_W))

layerNames = ["feature_fusion/Conv_7/Sigmoid","feature_fusion/concat_3"]

net = cv2.dnn.readNet("frozen_east_text_detection.pb")

blob = cv2.dnn.blobFromImage(img, 1.0, (new_H, new_W),(123.68, 116.78, 103.94), swapRB=True, crop=False)
net.setInput(blob)
(scores, geometry) = net.forward(layerNames)
confidences , rects = decode(scores, geometry, 0.8)
boxes = non_max_suppression(np.array(rects), probs=confidences)

padding = 0.5
# initialize the list of results
results = []
 
# loop over the bounding boxes
for (startX, startY, endX, endY) in boxes:
    # scale the bounding box coordinates based on the respective
    # ratios
    startX = int(startX * rW)
    startY = int(startY * rH)
    endX = int(endX * rW)
    endY = int(endY * rH)

    # in order to obtain a better OCR of the text we can potentially
    # apply a bit of padding surrounding the bounding box -- here we
    # are computing the deltas in both the x and y directions
    # dX = int((endX - startX) * padding)
    # dY = int((endY - startY) * padding)

    # # apply padding to each side of the bounding box, respectively
    # startX = max(0, startX - dX)
    # startY = max(0, startY - dY)
    # endX = min(H, endX + (dX * 2))
    # endY = min(W, endY + (dY * 2))

    roi = orig[startY:endY, startX:endX]
    config = ("-l eng --oem 1 --psm 7")
    text = pytesseract.image_to_string(roi, config=config)
    print(text)
    results.append(((startX, startY, endX, endY), text))

results = sorted(results, key=lambda r:r[0][1])
 
# loop over the results
# i = 0
# for ((startX, startY, endX, endY), text) in results:
#     # display the text OCR'd by Tesseract
#     print("OCR TEXT")
#     print("========")
#     print("{}\n".format(text))

#     # strip out non-ASCII text so we can draw the text on the image
#     # using OpenCV, then draw the text and a bounding box surrounding
#     # the text region of the input image
#     text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
#     output = orig.copy()
#     cv2.rectangle(output, (startX, startY), (endX, endY),
#         (0, 0, 255), 2)
#     cv2.putText(output, text, (startX, startY - 20),
#         cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

#     # show the output image
#     cv2.imwrite("img"+str(i)+".jpg",output)
#     i = i + 1

