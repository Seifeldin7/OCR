# some issues in my machine with ros
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')

import cv2
from decode import decode
import numpy as np
import time
from imutils.object_detection import non_max_suppression

orig = cv2.imread("images/test2.jpeg",1)  
(H, W) = orig.shape[:2] 
new_H = 160
new_W = 320
rW = W / float(new_W)
rH = H / float(new_H)            
img = cv2.resize(orig, (new_W,new_H))

#get NN layer names
layerNames = ["feature_fusion/Conv_7/Sigmoid","feature_fusion/concat_3"]
#load NN
net = cv2.dnn.readNet("frozen_east_text_detection.pb")
#get blobs from img 
#TODO What is blobs
start = time.time()
blob = cv2.dnn.blobFromImage(img, 1.0, (new_W, new_H),(123.68, 116.78, 103.94), swapRB=True, crop=False)
net.setInput(blob)
#NN feedforward
(scores, geometry) = net.forward(layerNames)
end = time.time()
confidences , rects = decode(scores, geometry, 0.8)
boxes = non_max_suppression(np.array(rects), probs=confidences)

print("time is ", end-start)
for (startX, startY, endX, endY) in boxes:
    startX = int(startX * rW)
    startY = int(startY * rH)
    endX = int(endX * rW)
    endY = int(endY * rH)
    cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

cv2.imshow("image", orig)
cv2.waitKey(0)