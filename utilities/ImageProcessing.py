from werkzeug.utils import secure_filename
import utilities.StorageInterface as StorageInterface
import utilities.DbInterface as DbInterface
from utilities.get_image_tags import get_image_tags_gpt
from models.All import Img

def process_image(file):
  """saves image to CDN, upon completion starts image captioning (new thread), and then updates database with image metadata"""
  filename_secured = secure_filename(file.filename)
  image_uri = StorageInterface.upload_to_aws(file.read(), filename_secured)
  if image_uri:
    img = DbInterface.save_img(filename_secured, image_uri)
    tags = get_image_tags_gpt(image_uri)
    DbInterface.update_tags(img.id, tags)
  #BEGIN IMAGE CAPTIONING, AS OF 05/2024 USING CHATGPT FOR CAPTIONING
  return 


def delete_image_and_metadata(image_id):
  img = Img.query.filter_by(id = image_id).one()
  is_deleted_from_db = DbInterface.delete_img(img)
  if is_deleted_from_db:
      StorageInterface.delete_from_aws(img.name)
  return
  