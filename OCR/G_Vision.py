import base64
import json
import requests

crendital=json.load(open('credential.json'))
apikey = crendital['G_VISION_KEY']

def apply_ocr():
    with open("./test.png", "rb") as img_file:
        my_base64 = base64.b64encode(img_file.read())

    url = "https://vision.googleapis.com/v1/images:annotate?key="+apikey
    data = {

        "requests": [
            
                {
                    "image": {
                        "content": my_base64.decode("utf-8")

                    },
                    "features": [
                        {
                            "type": "TEXT_DETECTION"
                        }
                    ],
                    "imageContext": {
                                    "languageHints": ["pt"]
                                                        
                                                        }
                    
                    
                    }
            
        ]

    }
    r = requests.post(url=url, data=json.dumps(data))
         
    if r.status_code != 200: return "error" 
    
    texts = r.json()['responses'][0]['textAnnotations']

    results = []

    for t in texts:
        results.append(t['description'])

    return results



text = apply_ocr()

print(" ".join(text))


