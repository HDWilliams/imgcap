from threading import Thread
from openai import OpenAI
from base64 import b64decode
from dotenv import load_dotenv
import os
import requests
from db import db
from models.Img import Img 
import app



class CaptionTask(Thread):
    def __init__(self, image, image_type, image_id):
        Thread.__init__(self)
        self.image = b64decode(image)
        self.image_type = image_type
        self.image_id = image_id
    
    def getImage(self, tags):
        with app.app.app_context():
            img: Img = Img.query.get(self.image_id)
            img.tags = tags
            db.session.add(img)
            db.session.commit()

            return 

    def run(self):
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('GPT_SECRET_KEY')}"
        }
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                "role": "user",
                "content": [
                        {"type": "text", 
                        "text": "caption this image based on the contents but also based on the emotions the image is likely to evoke. As an example, photos with smiling people would likely be labeled as happy, while photos of grey dark skies would likely be labeled as sad. Return the caption as a comma seperated list of all lowercase words relevant to the photo "},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{self.image_type};base64,{self.image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        #response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        #print(response['choices'][0]['message']['content'])

        self.getImage('lion')

        return



