# OCR
Text detection using EAST (An Efficient and Accurate Scene Text Detector)
EAST a nural network model used to detect text in images

Steps :
    1- load images using cv\n
    2- resize image (EAST text requires that your input image dimensions be multiples of 32)
    2- Convert the image to blobs (Blob is a group of connected pixels in an image that share some common property)
    3- loading EAST layer
    4- feed forward the converted blobs to EAST
    5- calculate box arround the word if it's score is greater than a specified value
    6- draw the box
