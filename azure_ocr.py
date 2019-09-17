import requests
import time

ocr_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/ocr"
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/" + \
    "Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png"


# headers = {'Ocp-Apim-Subscription-Key': "12bb5c83fb9a4d5e9df7417fd0016200"}
params = {'language': 'unk', 'detectOrientation': 'false'}
data = {'url': image_url}

image_path = "images/car_wash.png"
with open(image_path, 'rb') as f:
    img_data = f.read()
print(img_data)
# Set Content-Type to octet-stream
headers = {'Ocp-Apim-Subscription-Key': "12bb5c83fb9a4d5e9df7417fd0016200", 'Content-Type': 'application/octet-stream'}
# put the byte array into your post request
# response = requests.post(ocr_url, headers=headers, params=params, data = image_data)

start = time.time()
response = requests.post(ocr_url, headers=headers, params=params, json=data)
# response.raise_for_status()
analysis = response.json()
print("time is ", time.time() - start)
print(analysis)
print("image url is ",image_url)