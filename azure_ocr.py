import requests
import time
from PIL import Image
from io import BytesIO
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

ocr_url = vision_base_url + "ocr"
#image_url = "https://i.stack.imgur.com/vrkIj.png"


params = {'language': 'unk', 'detectOrientation': 'false'}
#data = {'url': image_url}

image_path = "img2.jpg"
image_data = open(image_path, "rb").read()
# Set Content-Type to octet-stream
headers = {'Ocp-Apim-Subscription-Key': "12bb5c83fb9a4d5e9df7417fd0016200", 'Content-Type': 'application/octet-stream'}
# put the byte array into your post request
print(image_data)
start = time.time()
response = requests.post(ocr_url, headers=headers, params=params, data=image_data)
# response.raise_for_status()
analysis = response.json()
print("time is ", time.time() - start)
#print("image url is ",image_url)
