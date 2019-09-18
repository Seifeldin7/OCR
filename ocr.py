import cv2
import numpy as np
import pytesseract

HSV_RANGES = {
    # red is a major color
    'red': [
        {
            'lower': np.array([0, 39, 64]),
            'upper': np.array([20, 255, 255])
        },
        {
            'lower': np.array([161, 39, 64]),
            'upper': np.array([180, 255, 255])
        }
    ],
    # yellow is a minor color
    'yellow': [
        {
            'lower': np.array([21, 39, 64]),
            'upper': np.array([40, 255, 255])
        }
    ],
    # green is a major color
    'green': [
        {
            'lower': np.array([41, 39, 64]),
            'upper': np.array([80, 255, 255])
        }
    ],
    # cyan is a minor color
    'cyan': [
        {
            'lower': np.array([81, 39, 64]),
            'upper': np.array([100, 255, 255])
        }
    ],
    # blue is a major color
    'blue': [
        {
            'lower': np.array([101, 39, 64]),
            'upper': np.array([140, 255, 255])
        }
    ],
    # violet is a minor color
    'violet': [
        {
            'lower': np.array([141, 39, 64]),
            'upper': np.array([160, 255, 255])
        }
    ],
    # next are the monochrome ranges
    # black is all H & S values, but only the lower 25% of V
    'black': [
        {
            'lower': np.array([0, 0, 0]),
            'upper': np.array([180, 255, 63])
        }
    ],
    # gray is all H values, lower 15% of S, & between 26-89% of V
    'gray': [
        {
            'lower': np.array([0, 0, 64]),
            'upper': np.array([180, 38, 228])
        }
    ],
    # white is all H values, lower 15% of S, & upper 10% of V
    'white': [
        {
            'lower': np.array([0, 0, 229]),
            'upper': np.array([180, 38, 255])
        }
    ]
}
def edge_detect(frame):
  frame = cv2.Canny(frame, 100, 100)
  blur5 = cv2.GaussianBlur(frame,(5,5),0)
  blur3 = cv2.GaussianBlur(frame,(1,1),0)
  return blur5-blur3

# Creates a binary mask from HSV image using given colors.
def create_mask(hsv_img, colors):



    mask = np.zeros((hsv_img.shape[0], hsv_img.shape[1]), dtype=np.uint8)

    for color in colors:
        for color_range in HSV_RANGES[color]:
            mask += cv2.inRange(
                hsv_img,
                color_range['lower'],
                color_range['upper']
            )

    return mask

def get_string(img):
    # Read image with opencv
    #img = cv2.imread(img_path)


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1)
    gray = cv2.erode(gray, kernel, iterations=1)
    gray = cv2.medianBlur(gray, 3)
    #  Apply threshold to get image with only black and white
    #gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 2)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(gray)

    return result


def isPaper(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    _, mask = cv2.threshold(hsv, 200, 255, cv2.THRESH_BINARY)

    #inverse of the mask
    mask_inv = cv2.bitwise_not(mask)

    #remove noise
    kernel = np.ones((11,11),np.uint8)
    mask_inv = cv2.morphologyEx(mask_inv, cv2.MORPH_CLOSE, kernel)
    #get contour of paper
    edges = edge_detect(mask_inv)
    cnts_t,_  = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts_t, key=cv2.contourArea)

    #get extreme points of the paper
    leftmost = tuple(c[c[:,:,0].argmin()][0])
    rightmost = tuple(c[c[:,:,0].argmax()][0])
    topmost = tuple(c[c[:,:,1].argmin()][0])
    bottommost = tuple(c[c[:,:,1].argmax()][0])
    x,top_y = topmost
    x,bot_y = bottommost
    lef_x,y = leftmost
    right_x,y = rightmost

    #get the prespective of the paper
    pts1 = np.float32([[lef_x, top_y], [right_x, top_y], [lef_x, bot_y], [right_x, bot_y]])
    pts2 = np.float32([[0, 0], [500, 0], [0, 600], [500, 600]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(frame, matrix, (500, 600))


    #show image of paper only
    cv2.imshow("paper",result)

#apply ocr using tesseract to get text and print it
    print(get_string(result))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

frame = cv2.imread("text.png")
choice = input("is the image in a paper? write p for paper")
if(choice == 'p'):
    isPaper(frame)
else:
    print(get_string(frame))
# i tried to get the words of each color


#img = cv2.imread('add-text.jpg')
#img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#y_mask = create_mask(img_hsv, ['yellow'])
#mask_img = cv2.bitwise_and(img_hsv, img_hsv, mask=y_mask)
#print(get_string(mask_img))
#cv2.imshow("image",mask_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
