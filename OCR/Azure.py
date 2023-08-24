import json
import time
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
from PIL import Image, ImageDraw 

credential = json.load(open('credential.json'))
API_KEY = credential['API_KEY']
ENDPOINT = credential['ENDPOINT']

cv_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

# image_url = 'https://i.imgur.com/dZqANc6.png'
# response = cv_client.read(url=image_url, language='pt', raw=True)

img = "./test.png"
response = cv_client.read_in_stream(open(img, 'rb'),  language='pt', raw=True)

operationLocation = response.headers['Operation-Location']
operation_id = operationLocation.split("/")[-1]

while True:
    result = cv_client.get_read_result(operation_id)
    if result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# print(result)
# print(result.status)
# print(result.analyze_result)

if result.status == OperationStatusCodes.succeeded:
    for text_result in result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            # print(line.bounding_box)

image = Image.open(img)
if result.status == OperationStatusCodes.succeeded:
    for text_result in result.analyze_result.read_results:
        for line in text_result.lines:
            x1,y1,x2,y2,x3,y3,x4,y4 = line.bounding_box
            draw = ImageDraw.Draw(image)
            draw.line(
            ((x1,y1),(x2,y1),(x2,y2),(x3,y2),(x3,y3),(x4,y3),(x4,y4),(x1,y4),(x1,y1)),
            fill= (255,0,0),
            width=5
            )
image.show()

