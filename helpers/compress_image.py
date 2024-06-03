from PIL import Image
import io

def compress_image(file, quality=60):
  """compress image to specified quality
  returns image file as JPEG
  """
  image = Image.open(file.stream)
  image_io = io.BytesIO()
  image.save(image_io, 'JPEG', quality=quality)
  return image_io.getvalue()