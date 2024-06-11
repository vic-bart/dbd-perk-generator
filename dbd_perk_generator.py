import cv2 as cv
from cv2.typing import MatLike
import numpy as np

def clear_terminal():
  import os
  os.system('cls' if os.name == 'nt' else 'clear')

def generate_perk_background(colour:tuple[int, int, int]) -> MatLike:
  clear_terminal()
  size = 10
  background = np.zeros(shape=(size, size, 4), dtype=np.uint8)
  background = [([0] * size) for _ in range(size)]
  origin = (size//2-1, size//2-1)

  for i in range(0, 4):
    if i == 0:
      background[origin[0]][origin[1]] = 1
      continue
    for j in range(0, i):
      x = -(i - 1) + (j)
      y = (1 + j)
      background[origin[0]+x][origin[1]+y] = 1
    for j in range(0, i):
      x = (1 + j)
      y = (i - 1) - (j)
      background[origin[0]+x][origin[1]+y] = 1
    for j in range(0, i):
      x = (i - 1) - (j)
      y = -(j + 1)
      background[origin[0]+x][origin[1]+y] = 1
    for j in range(0, i):
      x = -(j + 1)
      y = -(i - 1) + (j)
      background[origin[0]+x][origin[1]+y] = 1

  return

  offset = 0
  for i in (-1, 1):
    for j in range(len(background)//2, (len(background)//2) + (i * (len(background)//2)) + (offset*i), i):
      for k in range((128-j)+offset, len(background)-(129-j)-offset, 1):
        print(j, k)
        background[j-1][k-1] = [colour[0], colour[1], colour[2], 255]
  return background

def main() -> None:
  """
  Generates a single perk image.
  """
  foreground_filename = 'original_perks/0.webp'
  foreground:MatLike = cv.imread(foreground_filename, cv.IMREAD_UNCHANGED)
  background:MatLike = generate_perk_background(colour=(100, 100, 100))
  # composite_filename = 'new_perks/0.png'
  # cv.imwrite(composite_filename, background)

if __name__=="__main__":
  main()