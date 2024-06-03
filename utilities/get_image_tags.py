import os
from openai import OpenAI
from db import db
import logging

import utilities.DbInterface as DbInterface


def get_image_tags_gpt(image_uri):
    """ label image contents, emotion"""
    client = OpenAI(api_key=os.environ.get('GPT_SECRET_KEY'))
    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "caption image on the contents, the emotions the image evokes and the following compositional techniques where applicable, 'rule of thirds', 'centered', 'pattern', 'leading lines', 'symmetry', 'framing'. As an example, photos with smiling people would likely be labeled as happy, while photos of grey dark skies would likely be labeled as sad. Return the caption as a comma seperated list of all lowercase words relevant to the photo"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_uri #f"data:image/{self.image_type};base64,{str(self.image)[2:-1]}",
                            },
                        }
                    ],
                }
            ],
            max_tokens=300,
        )
        tags = str.split(response.choices[0].message.content, ",")
    except Exception as e:
        logging.exception(e)
        print(f"OpenAI API returned an API Error: {e}")
        #flag for recaptioning`s`
        tags = []
    #data is returned as a comma seperated string
    #update tag

    return tags

def tag_image(image_uri, image_id):
    """get tags from chatgpt and update database asynchronously"""
    tags = get_image_tags_gpt(image_uri)
    if tags:
        DbInterface.update_tags(image_id, tags)
        print('tags updated from gpt')
    return


