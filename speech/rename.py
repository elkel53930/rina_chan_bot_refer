import os
import glob
import shutil
import re


for filename in glob.glob('output/kizuna04*.wav'):
    newname = re.search(r"output/kizuna04(.*).wav", filename).group(1)
    newname = "output/kizuna04_" + newname + ".wav"
    print(newname)
    shutil.move(filename, newname)
#    os.remove(filename)
