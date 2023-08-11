import os
from PIL import Image
import pyocr
import numpy as np


class Read:
    replace_list = [
        ("……\n", "。"),
        ("\n", ""),
        ("……\n", "、"),
        (" ", ""),
        ("?", "？"),
        ("!", "！"),
        ("……？", "？"),
        ("……！", "！"),
        ("……。", "。"),
        ("……、", "、"),
        ("……", "、"),
        ("|]」", "」"),
        ("|]", "」"),
        ("璃奈", "リナ"),
        ("かなから", "から"),
    ]

    def __init__(self):
        tools = pyocr.get_available_tools()
        self.tool = tools[0]

    def read(self, filename):
        img_diag = Image.open(filename)
        img_name = img_diag.crop((447, 594, 519, 631))
        img_diag = img_diag.crop((470, 656, 1470, 810))
        img_diag.save("crop.png")
        img_diag = img_diag.convert('L')
        img_diag.save("gray.png")
        img_diag = np.array(img_diag)
        np.place(img_diag, img_diag > 160, 255)
        img_diag = Image.fromarray(np.uint8(img_diag))
        img_diag.save("mono.png")
        builder = pyocr.builders.TextBuilder(tesseract_layout=6)
        name = self.tool.image_to_string(img_name, lang="jpn", builder=builder)
        diag = self.tool.image_to_string(img_diag, lang="jpn", builder=builder)

        for old, new in self.replace_list:
            diag = diag.replace(old, new)

        return (diag, name, img_diag)


if __name__ == "__main__":
    import sys
    reader = Read()
    diag, name, img = reader.read(sys.argv[1])
    print(name, ":", diag)
    img.show()
