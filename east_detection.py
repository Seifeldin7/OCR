# some issues in my machine with ros
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')

import cv2

orignal = cv2.imread("images/sign.jpg",1)
img = cv2.resize(orignal, (320,320))


cv2.imshow("image", img)
cv2.imshow("orignal image", orignal)


cv2.waitKey(0)