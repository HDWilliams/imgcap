def prep_images_for_display(images:list):
  """split list of images into two list of even and odd indexs
  used for 2 column display, while keeping images in chronological order"""
  split_images = [images[::2],images[1::2]]
  return split_images