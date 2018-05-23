#!/usr/bin/env python
#encoding=utf-8

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure, curdoc
from bokeh.server.server import Server
from bokeh.themes import Theme
from bokeh.palettes import Category20 

from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature

from random import random, randint 

from tornado import gen
from threading import Condition, Thread, Lock

from functools import partial

import numpy as np
import time

from collections import OrderedDict


class BokehLivePlot(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.server = Server({'/': self.modify_doc}, num_procs=1)
        self.server.start()

#        self.doc=curdoc()

#        self.fig = dict()
#        self.cds = dict()

        self.t_msg_new_d = Condition()

        self.d = dict( dict() )
        self._x=0.0
        self.d_x=1

        self.d = dict( dict() )

        self.source = ColumnDataSource()

    def run(self):
        print('Opening Bokeh application on http://localhost:5006/')
        self.server.io_loop.add_callback(self.server.show, "/")
        self.server.io_loop.start()

    def modify_doc(self, doc):
        source = ColumnDataSource(data=dict(x=[0], y=[0]))
        
        doc.add_root(column([], name='plt_ui_col'))

        # FixMe: consider making this class member
        fig=dict()
        cds=dict()

        #doc = curdoc()
        print(Category20[20])

        def contains_line(line_name, fig_name):
            name = str(line_name) + '_glyph'
            if fig_name in fig:
                return bool( fig[fig_name].select_one({'name': name}) )
            else:
                return False

        def add_line(line_name, fig_name):
            if not contains_line(line_name, fig_name):
                print('add line ', line_name, ' in plot ', fig_name)
                # create name strings 
                data_name= str(line_name)
                glyph_name = data_name + '_glyph'
                legend_name = data_name + '_legend'
                # add corresponding data key to ColumnDataSource
                #dummy_data = np.full([len(self.cds[fig_name].data['empty'])], np.nan)
                dummy_data = np.full([len(cds[fig_name].data['x'])], np.nan)
                cds[fig_name].add(dummy_data, data_name)
                # create line object for corresponding figure
                plot=fig[fig_name].line(source=cds[fig_name], x='x', y=data_name, line_width=2, alpha=1, color=Category20[20][randint(0,19)], muted_alpha=.2, legend=legend_name, name=glyph_name)

        # FixMe: implement and test del line
        def del_line(line_name, fig_name):
            print('del line ', line_name, ' in plot ', fig_name)
            data_name= str(line_name)
            glyph_name = data_name + '_glyph'
            legend_name = data_name + '_legend'
            
            del_legend_idx = cds[fig_name].column_names.index(data_name) - 1
            del_line=fig[fig_name].select_one({'name': glyph_name})

            cds[fig_name].remove(data_name)
            fig[fig_name].renderers.remove(del_line); fig[fig_name].legend[0].items.pop(del_legend_idx) #FixMe which should i delete

        def add_plt(fig_name):
            # make sure name is a string
            fig_name=str(fig_name)
            # create plot if not already exists
            if not fig_name in fig:
                print('add fig ' + fig_name)
                # create plot
                TOOLS="pan,wheel_zoom,box_zoom,reset, save, tap, hover"
                #TOOLS=""
                plt_col=doc.get_model_by_name('plt_ui_col').children
                fig[fig_name]=figure(plot_width=900, plot_height=280, tools=TOOLS, toolbar_location='right', logo=None, title=(fig_name), name=str(fig_name))
                cds[fig_name]=ColumnDataSource(data=dict(x=np.array([])), name=(fig_name+'_cds'))
                plt_col.append( fig[fig_name] )

            else:
                pass

        @gen.coroutine
        def update(data):
            # update x
            self._x+=self.d_x
            # update all plots
            for plt in self.d:
                # add plot if not exists 
                add_plt(plt)
                for line in self.d[plt]:
                     # add line if not exists 
                     if not (line=='x'):
                         add_line(line, plt)
                # stream data
                data=self.d[plt]
                # FixMe preset all data with nan
                data['x']=np.array([self._x])
                # data that was present formerly and is not present in current data 
                absent_d_keys=list(set(cds[plt].data.keys()) - set(data.keys()))
                for absent in absent_d_keys:#list(set(cds[plt].data.keys()) - set(data.keys())):#absent_d_keys:
                    absent_list=cds[plt].data[absent][-20:]
                    if ( len(absent_list) ) and \
                       ( np.isnan(absent_list).all() ):
                        del_line(absent, plt)
                    else:
                        data[absent]=np.array([np.nan])
                cds[plt].stream( self.d[plt], 100 )
       
        def blocking_task():
            while True:
                # data
                # consumer
                self.t_msg_new_d.acquire()
                self.t_msg_new_d.wait()

                # update the document from callback
                doc.add_next_tick_callback(partial(update, data=self.d))
                self.t_msg_new_d.release()

        
        
        thread = Thread(target=blocking_task)
        thread.start()

    def push_d(self, data):
        # data
        # producer
        self.t_msg_new_d.acquire()
        self.d=data
        self.t_msg_new_d.notify()
        self.t_msg_new_d.release()
