import os
from threading import Thread
from openai import OpenAI
from db import db
import logging

import utilities.DbInterface as DbInterface


class CaptionTask(Thread):
    """create thread to send data to model for captioning of 
    image from image_uri

    Args: 
        image_uri  (str): url of image in CDN
        image_type (str): image ext 
        image_id   (str): primary key in db

        returns: None
    """
    def __init__(self, image_uri, image_type, image_id):
        Thread.__init__(self)
        self.image_uri = image_uri
        self.image_type = image_type
        self.image_id = image_id

    def run(self):
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
                                    "url": self.image_uri #f"data:image/{self.image_type};base64,{str(self.image)[2:-1]}",
                                },
                            }
                        ],
                    }
                ],
                max_tokens=300,
            )
        except Exception as e:
            logging.exception(e)
            print(f"OpenAI API returned an API Error: {e}")
            

        #data is returned as a comma seperated string
        tags = str.split(response.choices[0].message.content, ",")
        #update tag
        DbInterface.update_tags(self.image_id, tags)

        return



