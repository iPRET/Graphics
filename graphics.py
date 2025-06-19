"""
By default the axes are gonna be
 -> x
|
v
y

Dimensions are always ordered (x, y).

Colors are always ordered (r, g, b, (a)).

All arrays are always stored [x, y, 3/4]

All code expects positions to be iterables rather than seperate components.
All code expects colors to be iterables rather than seperate components.

The code works on uint8 for colors.

A pixel's center position is assumed to be a round number.
so in reality the screen goes from -0.5..maxx+0.5 e.g.
"""
import pygame as p
import numpy as np


width = 0
height = 0

screen = None
buffer = None
on = False


def _setup_screen_size_constants(w, h):
  global width
  global height
  width = w
  height = h
  
  global maxx
  global maxy
  maxx = width - 1
  maxy = height - 1
  


def open(width = 512, height = 512, name = "Graphics"):
  global on
  
  if on:
    raise RuntimeError("Code trying to intialize graphics a second time, it's already on.")
  
  _setup_screen_size_constants(width, height)
  
  global screen
  global buffer
  
  p.init()
  screen = p.display.set_mode((width, height))
  p.display.set_caption(name)
  buffer = np.zeros([width, height, 3], dtype = np.uint8)
  on = True
  
  
def close():
  global on
  p.quit()
  on = False
  
  
def draw():
  surf = p.image.frombuffer(buffer.swapaxes(0, 1).copy(order="C"), (width, height), "RGB")
  screen.blit(surf, (0, 0))
  p.display.flip()
  
  
def _intpoint(p):
  return [int(p[0]), int(p[1])]
  
  
def _inrange(x, mn, mx):
  return (x >= mn) and (x <= mx)
  
  
def putpixel(p, c = [255, 255, 255]):
  p = _intpoint(p)
  if _inrange(p[0], 0, maxx) and _inrange(p[1], 0, maxy):
    buffer[p[0], p[1]] = c


def rect(p1, p2, c = [255, 255, 255]):
  """
  Draws filled rectangle between two points, including the points themselves.
  """
  p1 = _intpoint(p1)
  p2 = _intpoint(p2)
  
  if p1[0] > p2[0]:
    p1[0], p2[0] = p2[0], p1[0]
  if p1[1] > p2[1]:
    p1[1], p2[1] = p2[1], p1[1]
  
  # Skip if rect doesn't intersect screen.
  if not (
    (_inrange(p1[0], 0, maxx) or _inrange(p2[0], 0, maxx)) and
    (_inrange(p1[1], 0, maxy) or _inrange(p2[1], 0, maxy))
  ):
    return
  
  p1[0] = max(p1[0], 0)
  p1[1] = max(p1[1], 0)
  p2[0] = min(p2[0], maxx)
  p2[1] = min(p2[1], maxy)
  
  buffer[p1[0]:p2[0] + 1, p1[1]:p2[1] + 1] = c
  

def line(p1, p2, c = [255, 255, 255]):
  #Shorten line by x.
  ##Reorder points to go leftward.
  if p2[0] > p1[0]:
    p1, p2 = p2, p1
  
  ## Check for out of screen.
  if p1[0] < 0:
    return
  if p2[0] > maxx:
    return
  
  ## Intersect with x boundaries.
  if p2[0] > maxx:
    deltax = p2[0] - p1[0]
    t = (maxx - p1[0]) / deltax
    deltay = p2[1] - p1[1]
    p2 = [maxx, p1[1] + t * deltay]
  
  if p1[0] < 0:
    deltax = p2[0] - p1[0]
    t = - p1[0] / deltax
    deltay = p2[1] - p1[1]
    p1 = [0, p1[1] + t * deltay]
  
  #Shorten line by y.
  ## Reorder points to go downward.
  if p2[1] < p1[1]:
    p1, p2 = p2, p1
  
  ## Check for out of screen.
  if p1[1] > maxy:
    return
  if p2[1] < 0:
    return
  
  ##Intersect with y boundaries.
  if p1[1] < 0:
    deltay = p2[1] - p1[1]
    t = -p1[1] / deltay
    deltax = p2[0] - p1[0]
    p1 = [p1[0] + deltax * t, 0]
  
  if p2[1] > maxy:
    deltay = p2[1] - p1[1]
    t = (p2[1] - maxy) / deltay
    deltax =  p2[0] - p1[0]
    p2 = (p1[0] + deltax * t, maxy)
  
  #Draw line
  deltax = p2[0] - p1[0]
  deltay = p2[1] - p1[1]
  if abs(deltax) > abs(deltay):
    ## Line is wider than it's tall.
    if p2[0] < p1[0]:
      p1, p2 = p2, p1
    
    startx = round(p1[0])
    endx = round(p2[0])
    
    dydx = (p2[1] - p1[1]) / (p2[0] - p1[0])
    
    for x in range(startx, endx + 1):
      y = p1[1] + (x - p1[0]) * dydx
      putpixel((x, y), c)
    
  else:
    ## Line is heigher than it's wide.
    if p2[1] < p1[1]:
      p1, p2 = p2, p1
    
    starty = round(p1[1])
    endy = round(p2[1])
    
    dxdy = (p2[0] - p1[0]) / (p2[1] - p1[1])
    
    for y in range(starty, endy + 1):
      x = p1[0] + (y - p1[1]) * dxdy
      putpixel((x, y), c)
  
  
def draw_np(p, pic):
  p = _intpoint(p)
  p2 = [p[0] + pic.shape[0] - 1, p[1] + pic.shape[1] - 1]
  if p2[0] < 0:
    return
  if p2[1] < 0:
    return
  if p[0] > maxx:
    return
  if p[1] > maxy:
    return
  
  picp1 = [0, 0]
  picp2 = [pic.shape[0] - 1, pic.shape[1] - 1]
  
  if p[0] < 0:
    picp1[0] = -p[0]
    p[0] = 0 
  if p[1] < 0:
    picp1[1] = -p[1]
    p[1] = 0
  if p2[0] > maxx:
    picp2[0]-= p2[0] - maxx
    p2[0] = maxx
  if p2[1] > maxy:
    picp2[1]-= p2[1] - maxy
    p2[1] = maxy
  
  buffer[p[0]:p2[0] + 1, p[1]: p2[1] + 1] = pic[picp1[0]: picp2[0] + 1, picp1[1]: picp2[1] + 1]
  
  
from PIL import Image
  
def load_pic(path):
  img = Image.open(path).convert("RGB")
  arr_yx = np.asarray(img, dtype=np.uint8)
  arr_xy = np.transpose(arr_yx, (1, 0, 2))   # now shape is (x, y, 3)
  return arr_xy
  
  
from PIL import Image, ImageDraw, ImageFont
  
def gen_text(text,
             font_path = "fonts/Atkinson.ttf",
             font_size = 16) -> np.ndarray:
    
    font = ImageFont.truetype(str(font_path), font_size)

    # First pass—get bounding box
    dummy = Image.new("L", (1, 1), 0)
    w, h = ImageDraw.Draw(dummy).textbbox((0, 0), text, font=font)[2:]

    # Second pass—actually draw
    img = Image.new("L", (w, h), 0)  # 'L' = 8-bit greyscale
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, fill=255, font=font)

    arr = np.asarray(img).swapaxes(0, 1)

    return arr