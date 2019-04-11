#!/usr/bin/env python
#encoding=utf-8

import numpy as np
from random import choice, shuffle, uniform

#from data_factory import PlotFactory
class DataFactory():
    def __init__(self, n=1):
        print("do it, big time!")
        self.plt_max=5
        self.nmb_plt=None
        if n < self.plt_max:
            self.nmb_plt=n
        else:
            print("Maximum possible plots are", self.nmb_plt, ", n default to", self.nmb_plt)
            self.nmb_plt=5 # default to maximal possible
        self.nmb_plt=n
        self.name=["temperature", "pressure", "humidity", "acceleration", "magnetic_field"]
        self.func=[np.sin, np.cos, self.func1, self.func2, self.func3] #function
        self.a=[1,2,3,4,5] # amplitude
        self.b=[1,2,3,4,5] # bias
        self.s=[1,2,3,4,5] # shift
        self.f=[1,1,2,2,5] # frequency
        self.noise=[1,1,2,3,5] # noise (supposed to be multiplied by 0.01)
        self.randomize()

    def randomize(self):
        print("Shuffle all lists, this way iterating over\nthem has the same result as random choice.")
        shuffle(self.name)
        shuffle(self.func)
        shuffle(self.a)
        shuffle(self.b)
        shuffle(self.f)
        shuffle(self.noise)
#        if n<self._max_plts:
#            for p in range(n):
#                key=self.rand_name.remove( choice(self.name) )
#                print(self.rand_name)
#        #        self.plots[]
#        else:
#            print("Maximum number of plots available is", self._max_plts)

    def produce_data(self,x):
        print("return dictionary with data")
        data = dict()
        for i in range(self.nmb_plt):
            name=self.name[i]
            func=self.func[i]
            a = self.a[i] # amplitude
            b = self.b[i] # bias
            s = self.s[i] # shift
            f = self.f[i] # frequency
            u = self.noise[i]*0.2
            noise = uniform(-u,u)
            data[name]=np.array([ a*func( (x-s)*f  ) + b + noise])
        return data
    
    def func1(self,x):
        return ( np.sin(x)*np.cos(x) / 2.0 )
    def func2(self,x):
        return ( np.sin(x) + np.sin(x/2) + np.sin(x/4) )
    def func3(self,x):
        return ( np.sin(x)*np.sin(x/4) )
