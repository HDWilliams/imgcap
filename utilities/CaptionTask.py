from threading import Thread
from openai import OpenAI
from base64 import b64encode
from dotenv import load_dotenv
import os
import requests
from db import db

from  utilities.DbInterface import DbInterface


class CaptionTask(Thread):
    #SEND IMAGE DATA TO CHATGPT FOR CAPTIONING
    def __init__(self, image, image_type, image_id):
        Thread.__init__(self)
        self.image = b64encode(image)
        self.image_type = image_type
        self.image_id = image_id

    def run(self):
        #[2:-1] used to remove b' from beginning and ' from end of b64 encoded string

        #USED FOR DEV ONLY TO AVOID SSL ISSUES FROM LOCAL SERVER
        #os.environ['REQUESTS_CA_BUNDLE'] = r"C:\Users\Hugh Day-Williams\CodingProjects\certadmin.crt"

        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('GPT_SECRET_KEY')}"
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
                                "url": f"data:image/{self.image_type};base64,{str(self.image)[2:-1]}" 
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        """
        client = OpenAI(api_key=os.environ.get('GPT_SECRET_KEY'))
        try:
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "caption this image based on the contents but also based on the emotions the image is likely to evoke. As an example, photos with smiling people would likely be labeled as happy, while photos of grey dark skies would likely be labeled as sad. Return the caption as a comma seperated list of all lowercase words relevant to the photo"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{self.image_type};base64,{str(self.image)[2:-1]}",
                                },
                            }
                        ],
                    }
                ],
                max_tokens=300,
            )
        except Exception as e:
            #Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            pass

        #data is returned as a comma seperated string
        tags = str.split(response['choices'][0]['message']['content'], ",")
        #update tag
        db_interface = DbInterface()
        db_interface.update_tags(self.image_id, tags)

        return



