import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from board import DisplayCommand, BOARD_WIDTH, BOARD_HEIGHT
from exp import _face, _mouth, _eyes

from PIL import Image, ImageDraw, ImageFont
from csv import reader
import glob


dot_size = 20
line_width = 2

dot_color = (255, 100, 150)
line_color = (255, 230, 240)


def point(p):
    return p * (dot_size + line_width) + line_width


def make_image(disp_cmd, pngfile):
    im = Image.new("RGB", (point(BOARD_WIDTH), point(BOARD_HEIGHT)), (240, 255, 255))
    draw = ImageDraw.Draw(im)

    y = 0
    draw.line((0, 0, im.width, 0), fill=line_color, width=line_width)
    draw.line((0, 0, 0, im.height), fill=line_color, width=line_width)

    for x in range(0, BOARD_WIDTH):
        draw.line((point(x+1)-line_width/2, im.height, point(x+1) -
                   line_width/2, 0), fill=line_color, width=line_width)

    for row in disp_cmd.graphic:
        x = 0
        draw.line((0, point(y+1)-line_width/2, im.width, point(y+1)-line_width/2),
                  fill=line_color, width=line_width)
        for cell in row:
            if cell:
                draw.rectangle((point(x), point(y)+1,
                                point(x)+dot_size,
                                point(y)+dot_size),
                               fill=dot_color)
            x += 1
        y += 1
    im.save(pngfile)


def traverse(exps, name_base):
    for name, exp in exps.items():
        make_image(DisplayCommand(exp), name_base+name+'.png')


def main():
    traverse(_face, 'face_')
    traverse(_mouth, 'mouth_')
    traverse(_eyes, 'eyes_')

if __name__ == '__main__':
    main()
