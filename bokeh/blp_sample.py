#!/usr/bin/python3.6
#coding=utf-8


from bokeh_live_plot import BokehLivePlot
from random import uniform
from tornado import gen

import numpy as np
import random, time
from threading import Thread

#import os

#os.system("clear")
#os.system("byzanz-record --duration=16 --x=0 --y=60 --width=1300 --height=880 out.gif")

# data stimuli for test purposes
def rand_data():
    return dict( temperature=dict( t001=np.array([uniform(-1,1)]), t004=np.array([uniform(-1,1)]) ) )
def rand_data1():
    return dict( temperature=dict( t001=np.array([uniform(-1,1)]), t004=np.array([uniform(-1,1)]) ), pressure=dict( p001=np.array([uniform(-1,1)]), p002=np.array([uniform(3,2)]), p004=np.array([uniform(-4,-1)]) ) )
def rand_data2():
    return dict( temperature=dict( t001=np.array([uniform(-1,1)]), t004=np.array([uniform(-1,1)]) ),  pressure=dict( p001=np.array([uniform(-1,1)])), humidity=dict( h001=np.array([uniform(-1,1)]), h004=np.array([uniform(-1,1)]) ) )
def rand_data3():
    return dict( temperature=dict( t001=np.array([uniform(-4,23)]), t004=np.array([uniform(-1,1)]) ), pressure=dict( p001=np.array([uniform(-1,1)]), p002=np.array([uniform(4,3)]) ), humidity=dict( h001=np.array([uniform(-1,1)]), h002=np.array([uniform(-1,1)]), h004=np.array([uniform(-2,4)]) ) )
def rand_data4():
    return dict( temperature=dict( t001=np.array([uniform(-4,23)]), t004=np.array([uniform(-1,1)]) ), pressure=dict( p001=np.array([uniform(-1,1)]), p002=np.array([uniform(4,3)]), p004=np.array([uniform(1,2)]) ), humidity=dict( h001=np.array([uniform(-1,1)]), h002=np.array([uniform(-1,1)]), h004=np.array([uniform(-2,4)]) ) )

myplot = BokehLivePlot()
myplot.start()

delta_t=.2

# test dynamic_live_plot
for i in range(10):
    myplot.push_d( rand_data() )
    time.sleep(delta_t)

for i in range(20):
    myplot.push_d( rand_data1() )
    time.sleep(delta_t)

for i in range(10):
    myplot.push_d( rand_data2() )
    time.sleep(delta_t)

for i in range(30):
    myplot.push_d( rand_data3() )
    time.sleep(delta_t)

while True:
    myplot.push_d( rand_data4() )
    time.sleep(delta_t)

# this point will never be reached
while True:
    print('Greetings vom main thread.')
    time.sleep(.1)
