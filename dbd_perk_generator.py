import cv2 as cv
from cv2.typing import MatLike
import numpy as np

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

def main() -> None:
  """
  Generates a single perk image.
  """
  foreground_filename = 'original_perks/0.webp'
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
  composite_filename = 'new_perks/0.png'
  cv.imwrite(composite_filename, composite)

if __name__=="__main__":
  main()