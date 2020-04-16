# biv - bloated image viewer
# view images, albeit shittily, right in your terminal!
from sys import argv
from os import get_terminal_size
from PIL import Image
from sty import fg

cols, lines = get_terminal_size()

image_in = Image.open(argv[1])
image_resized = image_in.resize((cols, lines), Image.BICUBIC)

width, height = image_resized.size
image_map = image_resized.load()

for y in range(height):
    for x in range(width):
        r, g, b = image_map[x, y]
        buf = fg(r, g, b) + "\u2588" + fg.rs
        print(buf, end="")
    print()
