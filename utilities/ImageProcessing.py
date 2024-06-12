import os
from datetime import datetime
from werkzeug.utils import secure_filename
import utilities.StorageInterface as StorageInterface
import utilities.DbInterface as DbInterface
from utilities.get_image_tags import tag_image, get_image_tags_aws
from models.All import Img
from helpers.compress_image import compress_image

def process_image(file):
  """saves image to CDN, upon completion starts image captioning (new thread), and then updates database with image metadata"""
  filename_secured = datetime.now().strftime("%Y%m%d_%H%M%S") + secure_filename(file.filename)
  image = compress_image(file)
  image_uri = StorageInterface.upload_to_aws(image, filename_secured)
  if image_uri:
    img = DbInterface.save_img(filename_secured, image_uri)
    tag_image(image_uri, img.id, filename_secured, os.getenv('BUCKET'), model='aws')
  #BEGIN IMAGE CAPTIONING, AS OF 05/2024 USING CHATGPT FOR CAPTIONING
  return


def delete_image_and_metadata(image_id):
  img = Img.query.filter_by(id = image_id).one()
  is_deleted_from_db = DbInterface.delete_img(img)
  if is_deleted_from_db:
      StorageInterface.delete_from_aws(img.name)
  return
  