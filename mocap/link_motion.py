import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from time import sleep, time
from math import pi

# rina lib
#from frame.frame_client import FrameClient
from mocap import Mocap, IIR
from anata.anata import *


iif_lpf = [1.80249550318775681e-01,-1.39494354369317497e+00,4.89049261407235869e-01,1.30521432019709172e-01,2.61042864039418343e-01,1.30521432019709172e-01,1.87543844814114846e-01,-1.45139377612967801e+00,5.49307740896159413e-01,1.30521432019709172e-01,2.61042864039418343e-01,1.30521432019709172e-01,2.02700722337186973e-01,-1.56869220159573763e+00,6.74519355799253817e-01,1.30521432019709172e-01,2.61042864039418343e-01,1.30521432019709172e-01,2.26631545050917482e-01,-1.75389181280556983e+00,8.72212908009109777e-01,1.30521432019709172e-01,2.61042864039418343e-01,1.30521432019709172e-01 ]
x_filter = IIR(iif_lpf)
y_filter = IIR(iif_lpf)
z_filter = IIR(iif_lpf)

traj_generator = t_linear

for i in reversed(range(1,3)):
    print(i)
    sleep(1)

m = Mocap('/dev/ttyACM3')

wait_init()

set_exp(eyes['normal']+mouth['normal'])


prev_time = time()
while True:
    (c,x,y,z) = m.get_euler()
    print(hex(c),x,y,z)
    current_time = time()

    x = x * pi / 180
    x = x_filter.apply(x)
    y = y * pi / 180
    y = y_filter.apply(y)
    z = z * pi / 180
    z = z_filter.apply(z)

    move(current_time-prev_time, [-x,y,z])
    print(x,y,z)
    prev_time = current_time
