# azure return JASON structure
#   | language 
#   | oriantation
#   | text angle
#   | Regions
#       | boundingBox : cordinates of the bounding Box of all the text
#       | lines 
#             | boundingBox : cordinates of the bounding Box of all the line
#             | words
#                 | text : the text
#                 | boundingBox : cordinates of the bounding Box of all the text

import requests
import time
from PIL import Image
from io import BytesIO

vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/ocr"
key = "12bb5c83fb9a4d5e9df7417fd0016200"

image_path = "images/test2.jpeg"
image_data = open(image_path, "rb").read()

params = {'language': 'unk', 'detectOrientation': 'false'}
headers = {'Ocp-Apim-Subscription-Key': key, 'Content-Type': 'application/octet-stream'}

start = time.time()
response = requests.post(vision_base_url, headers=headers, params=params, data=image_data)
analysis = response.json()
print("time is ", time.time() - start)

for lines in analysis["regions"] :
    for line in lines["lines"] :
        for word in line["words"] :
            print(word["text"])

