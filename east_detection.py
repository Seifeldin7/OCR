# some issues in my machine with ros
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')

import cv2
from decode import decode
import numpy as np
from imutils.object_detection import non_max_suppression

img = cv2.imread("images/sign.jpg",1)               
img = cv2.resize(img, (160,160))

#get NN layer names
layerNames = ["feature_fusion/Conv_7/Sigmoid","feature_fusion/concat_3"]
#load NN
net = cv2.dnn.readNet("frozen_east_text_detection.pb")
#get blobs from img 
#TODO What is blobs
blob = cv2.dnn.blobFromImage(img, 1.0, (160, 160),(123.68, 116.78, 103.94), swapRB=True, crop=False)
net.setInput(blob)
#NN feedforward
(scores, geometry) = net.forward(layerNames)

confidences , rects = decode(scores, geometry, 0.5)
boxes = non_max_suppression(np.array(rects), probs=confidences)

for (startX, startY, endX, endY) in boxes:
	cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)

cv2.imshow("image", img)
cv2.waitKey(0)