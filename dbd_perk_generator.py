import cv2 as cv
from cv2.typing import MatLike
import numpy as np
import urllib3

def add_diamond(img:MatLike, origin:tuple[int, int], size:int, colour:tuple[int, int, int]) -> MatLike:
  if len(origin) != 4:
    origin = (
      (origin[0], origin[1]),
      (origin[0], origin[1]),
      (origin[0], origin[1]),
      (origin[0], origin[1])
      )

  for i in range(0, size//2):
    if i == 0:
      img[origin[0][0]][origin[1][1]] = [colour[0], colour[1], colour[2], 255]
      img[origin[1][0]][origin[1][1]] = [colour[0], colour[1], colour[2], 255]
      img[origin[2][0]][origin[2][1]] = [colour[0], colour[1], colour[2], 255]
      img[origin[3][0]][origin[3][1]] = [colour[0], colour[1], colour[2], 255]
      continue
    for j in range(-1, i):
      x = -(i - 1) + (j)
      y = (1 + j)
      img[origin[0][0]+x][origin[0][1]+y] = [colour[0], colour[1], colour[2], 255]
    for j in range(-1, i):
      x = (1 + j)
      y = (i - 1) - (j)
      img[origin[1][0]+x][origin[1][1]+y] = [colour[0], colour[1], colour[2], 255]
    for j in range(-1, i):
      x = (i - 1) - (j)
      y = -(j + 1)
      img[origin[2][0]+x][origin[2][1]+y] = [colour[0], colour[1], colour[2], 255]
    for j in range(-1, i):
      x = -(j + 1)
      y = -(i - 1) + (j)
      img[origin[3][0]+x][origin[3][1]+y] = [colour[0], colour[1], colour[2], 255]

  return img

def combine_images(background:MatLike, foreground:MatLike) -> MatLike:
  """
  Combines two images, accounting for their transparent qualities.

  Credit to Mala for the alpha compositing: 
  https://stackoverflow.com/questions/40895785/using-opencv-to-overlay-transparent-image-onto-another-image
  """
  # Make sure both images have alpha channels
  if (len(background[0][0])!=4) or (len(background[0][0])!=4):
    background = cv.cvtColor(background, cv.COLOR_BGR2BGRA)
    foreground = cv.cvtColor(foreground, cv.COLOR_BGR2BGRA)

  # Normalise alpha channels from 0-255 to 0-1
  alpha_background = background[:,:,3] / 255
  alpha_foreground = foreground[:,:,3] / 255

  # Set adjusted colors
  for i in range(len(alpha_foreground)):
    for j in range(len(alpha_foreground[i])):
      for k in range(0, 3):
        background[i,j,k] = \
          (alpha_foreground[i,j] * foreground[i,j,k]) + \
            (alpha_background[i,j] * background[i,j,k] * \
             (1 - alpha_foreground[i,j]))

  # Set adjusted alpha and denormalise back to 0-255
  for i in range(len(alpha_foreground)):
    for j in range(len(alpha_foreground[i])):
      background[i,j,3] = (1 - (1 - alpha_foreground[i,j]) * (1 - alpha_background[i,j])) * 255

  # Return the composite image
  return background

def get_images() -> MatLike:
  # Get webpage data
  URL:str = "https://deadbydaylight.fandom.com/wiki/Perks"
  response:object = urllib3.request(method="GET", url=URL, decode_content=True)
  data:str = response.data.decode(encoding='utf-8', errors='strict')
  # Isolate survivor perks
  data = remove_prefix(string=data, prefix="Survivor Perks", amount=2)
  totalSurvivorPerks = remove_prefix(string=data, prefix=" (", amount=1)
  totalSurvivorPerks = int(remove_suffix(string=totalSurvivorPerks, suffix=")"))
  for i in range(totalSurvivorPerks):
    data = remove_prefix(string=data, prefix='h>\n<th><a href="/wiki/', amount=1)
    perkName = remove_suffix(string=data, suffix='"')
    URL:str = f"https://deadbydaylight.fandom.com/wiki/{perkName}"
    response:object = urllib3.request(method="GET", url=URL, decode_content=True)
    imgData:str = response.data.decode(encoding='utf-8', errors='strict')
    imgURL = remove_prefix(string=imgData, prefix=f'<a href="/wiki/{perkName}', amount=1)
    imgURL = remove_prefix(string=imgURL, prefix='-src="', amount=1)
    imgURL = remove_suffix(string=imgURL, suffix='"')
    response:object = urllib3.request(method="GET", url=imgURL, decode_content=True)
    array = bytearray(response.data)
    array = np.asarray(array, dtype=np.uint8)
    img = cv.imdecode(array, -1)
    cv.imwrite(f"raw_survivor_perks/{i}.png", img)
  # Get webpage data
  URL:str = "https://deadbydaylight.fandom.com/wiki/Perks"
  response:object = urllib3.request(method="GET", url=URL, decode_content=True)
  data:str = response.data.decode(encoding='utf-8', errors='strict')
  # Isolate killer perks
  data = remove_prefix(string=data, prefix="Killer Perks", amount=2)
  totalKillerPerks = remove_prefix(string=data, prefix=" (", amount=1)
  totalKillerPerks = int(remove_suffix(string=totalKillerPerks, suffix=")"))
  for i in range(totalKillerPerks):
    data = remove_prefix(string=data, prefix='h>\n<th><a href="/wiki/', amount=1)
    perkName = remove_suffix(string=data, suffix='"')
    URL:str = f"https://deadbydaylight.fandom.com/wiki/{perkName}"
    response:object = urllib3.request(method="GET", url=URL, decode_content=True)
    imgData:str = response.data.decode(encoding='utf-8', errors='strict')
    imgURL = remove_prefix(string=imgData, prefix=f'<a href="/wiki/{perkName}', amount=1)
    imgURL = remove_prefix(string=imgURL, prefix='-src="', amount=1)
    imgURL = remove_suffix(string=imgURL, suffix='"')
    response:object = urllib3.request(method="GET", url=imgURL, decode_content=True)
    array = bytearray(response.data)
    array = np.asarray(array, dtype=np.uint8)
    img = cv.imdecode(array, -1)
    cv.imwrite(f"raw_killer_perks/{i}.png", img)

def remove_prefix(string:str, prefix:str, amount:int) -> str:
  """
  Returns substring of a string from the prefix (excluded) to the terminal character.
  """
  for _ in range(amount):
    index = string.find(prefix)
    string = string.removeprefix(string[:index+len(prefix)])
  return string

def remove_suffix(string:str, suffix:str) -> str:
  """
  Returns substring of a string until the suffix (excluded).
  """
  index = string.find(suffix)
  string = string.removesuffix(string[index:])
  return string

def main() -> None:
  """
  Generates a single perk image.
  """
  get_images()
  for i in range(140):
    foreground_filename = f"raw_survivor_perks/{i}.png"
    foreground:MatLike = cv.imread(foreground_filename, cv.IMREAD_UNCHANGED)
    background = np.zeros(shape=(256, 256, 4), dtype=np.uint8)
    background:MatLike = add_diamond(
      img=background,
      origin=(len(background)//2, len(background)//2), 
      size=len(background),
      colour=(0, 0, 0)
      )
    background:MatLike = add_diamond(
      img=background,
      origin=(len(background)//2, len(background)//2), 
      size=int(0.8*len(background)),
      colour=(112, 34, 133)
      )
    composite = combine_images(background=background, foreground=foreground)
    composite_filename = f"new_survivor_perks/{i}.png"
    cv.imwrite(composite_filename, composite)
  for i in range(121):
    foreground_filename = f"raw_killer_perks/{i}.png"
    foreground:MatLike = cv.imread(foreground_filename, cv.IMREAD_UNCHANGED)
    background = np.zeros(shape=(256, 256, 4), dtype=np.uint8)
    background:MatLike = add_diamond(
      img=background,
      origin=(len(background)//2, len(background)//2), 
      size=len(background),
      colour=(0, 0, 0)
      )
    background:MatLike = add_diamond(
      img=background,
      origin=(len(background)//2, len(background)//2), 
      size=int(0.8*len(background)),
      colour=(112, 34, 133)
      )
    composite = combine_images(background=background, foreground=foreground)
    composite_filename = f"new_killer_perks/{i}.png"
    cv.imwrite(composite_filename, composite)

if __name__=="__main__":
  main()