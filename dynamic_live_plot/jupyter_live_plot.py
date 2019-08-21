#!/usr/bin/env python
#encoding=utf-8

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.palettes import Category20
from bokeh.io import output_notebook, show, push_notebook
from bokeh.models import DatetimeTickFormatter

from threading import Thread

import numpy as np
from random import random, randint
import time

class JupyterLivePlot():
    output_notebook()
    def __init__(self, plot_width=600, plot_height=400, timeplot = False):
        print("Create plot")
        print("- width:", plot_width, "px")
        print("- height:", plot_height, "px")
        
        self.width_d = 200
        self.width_drop = 50
        
        # x-axis (optionally provided here)
        # can also be delivered from outside
        self._x=0.0
        self.d_x=.1
        
        # note: if the ColumnDataSource is not filled by some values
        # rendering the plot fails afterwards.
        self.cds = ColumnDataSource( data=dict(x=np.array([0.]), dummy=np.array([0.]) ) )
        #self.cds = ColumnDataSource( data=dict(x=np.array([0])) )
        if timeplot:
            self.fig = figure(plot_width=plot_width, plot_height=plot_height, x_axis_type="datetime")
            self.fig.xaxis.formatter = DatetimeTickFormatter(microseconds="%m/%d %H:%M:%S",
                                                             milliseconds="%m/%d %H:%M:%S",
                                                             seconds="%m/%d %H:%M:%S", minsec="%m/%d %H:%M:%S",
                                                             minutes="%m/%d %H:%M:%S", hourmin="%m/%d %H:%M:%S")
        else:
            self.fig = figure(plot_width=plot_width, plot_height=plot_height)
        
        # note: this is just a dummy line, which will be deleted, 
        # right after self.handler is created by the show method. 
        # Somehow not everything is rendered if no initial line 
        # glyph exists (must be some hidden magic of a constructor).
        self.fig.line(x='x', y='dummy', source=self.cds, name='dummy_glyph')
        # naming convention     -----                          -----------
        # of methods            name                           name_glyph
        # add_line and 
        # del_line
        
        # handler used for in-place updates in jupyter notebooks
        # note: this class will only work properly if used inside
        # of a jupyter notebook
        self.handle = show(self.fig, notebook_handle=True)
        
        self.del_line('dummy')
        # del line
        #del_line = my_figure.select_one({'name':'dummy_line_glyph'})
        #my_figure.renderers.remove(del_line)
        #test_data.remove('dummy_line')
        #push_notebook(handle=handle)
        
        # thread for periodic callback function 
        # for non-blocking operations 
        self.th = None
        self.stop_threads = False
        self.periodic_callback = None
        self.period_seconds = None
        
    def contains_line(self, line_name):
        #return True
        name = str(line_name) + '_glyph'
        return bool( self.fig.select_one({'name': name}) )

    def add_line(self, line_name):
        if not self.contains_line(line_name):
            push_notebook(handle=self.handle)

            # create name strings 
            data_name= str(line_name)
            glyph_name = data_name + '_glyph'
            legend_name = data_name + '_legend'
        
            # add corresponding data key to ColumnDataSource
            dummy_data = np.full([len(self.cds.data['x'])], np.nan)
            self.cds.add(dummy_data, data_name)
            push_notebook(handle=self.handle)

            # create line object for corresponding figure
            plot=self.fig.line(source=self.cds,\
                               x='x',\
                               y=data_name,\
                               line_width=2,\
                               alpha=1,\
                               color=Category20[20][randint(0,19)],\
                               muted_alpha=.2,\
                               #legend=legend_name,\
                               name=glyph_name)
            push_notebook(handle=self.handle)
    
    def del_line(self, line_name):
        #FixMe: if not contains_line(line_name):
        print('del line', line_name)
        data_name= str(line_name)
        glyph_name = data_name + '_glyph'
        print(glyph_name)
        #legend_name = data_name + '_legend'
        
        #del_legend_idx = cds[fig_name].column_names.index(data_name) - 1
        del_line=self.fig.select_one({'name': glyph_name})
        
        self.cds.remove(data_name)
        push_notebook(handle=self.handle)

        self.fig.renderers.remove(del_line); #self.fig.legend[0].items.pop(del_legend_idx) #FixMe which should i delete
        push_notebook(handle=self.handle)

    def add_periodic_callback(self, callback, period_milliseconds):
        if not self.th is None:
            print("Remove existing callback, before creating a new one.")
            # remove existing periodic callback
            self.remove_periodic_callback()

        self.periodic_callback = callback
        self.period_seconds = period_milliseconds/1000
        
        self.stop_threads=False
        self.th = Thread(target=self.blocking_task, args=(id, lambda: self.stop_threads))
        self.th.start()
        
    def remove_periodic_callback(self):
        print("stop thread")
        
        self.stop_threads=True
        del self.th
        
        self.periodic_callback = None
        self.th = None
        #self.stop_threads=False
    
    def blocking_task(self, id, stop):
        while True:
            self.periodic_callback()
            time.sleep(self.period_seconds)
            if stop():
                print("exit.")
                break
    
    def push_data(self, data):
        data_len = len(list(data.values())[0])
        if data_len > 1 and isinstance(self._x, np.ndarray):
            self._x = np.linspace(self._x[-1] + self.d_x,
                                  self._x[-1] + self.d_x * data_len,
                                  data_len)
        elif data_len > 1:
            self._x = np.linspace(self._x + self.d_x,
                                  self._x + self.d_x * data_len,
                                  data_len)
        elif isinstance(self._x, np.ndarray):
            self._x = self._x[-1]+self.d_x
        else:
            self._x += self.d_x
        
        # add lines, not seen before
        for line in data:
            # add line if not exists 
            if not (line=='x'):
                self.add_line(str(line))
        
        # set if not in data alreadyx
        # FixMe: set length
        if not 'x' in data.keys():
             if isinstance(self._x, np.ndarray):
                 data['x'] = self._x
             else:
                 data['x'] = np.array([self._x])
        # else just use the one inside of data
        
         # data that was present formerly and is not present in current data 
        absent_d_keys=list(set(self.cds.data.keys()) - set(data.keys()))
        for absent in absent_d_keys:
            absent_list=self.cds.data[absent][-self.width_drop:]
            if ( len(absent_list) ) and \
               ( np.isnan(absent_list).all() ):
                self.del_line(absent)
            else:
                data[absent]=np.array([np.nan]*data_len)
        
        # stream data
        self.cds.stream( data, self.width_d )
        push_notebook(handle=self.handle)
