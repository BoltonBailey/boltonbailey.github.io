"""Generate a minsweeper board from an image of one
"""

from PIL import Image
import pytesseract

# WIP


im = Image.open('test1.png')

print(im.width)
print(im.height)
print(im.getpixel((300, 300)))
print(im.getpixel((277, 277)))

start_x = 170
start_y = 395

cell_width = 64
cell_height = 64


def get_cell(im, x, y):
    return im.crop(
        (170 + x * 64,
         395 + y * 64,
         170 + x * 64 + 320,
         395 + y * 64 + 320))


get_cell(im, 2, 4).show()
# get_cell(im, 2, 5).show()
