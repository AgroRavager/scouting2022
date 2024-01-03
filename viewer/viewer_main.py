import pickle
import pandas as pd
import bokeh.io as io
import bokeh.models as models
import bokeh.plotting as plotting
import bokeh.resources as resources
import bokeh.layouts as layouts
#import scouter.scout.event as event

# import data function
def make_data_source():
    graph_data = plotting.ColumnDataSource(measures)
    return graph_data



#graph_data is the column data source defined earlier

#data_changes is a value representing the changes you'd like to make to the data in the graph
#frame_change_items is a dictonary of values in the frame you'd want to change, options being title, y_range, and x_range 
#with the key being the changed item and the value being what you want to change it to
def data_refresh(graph_data,data_changes,frame_change_items,scout_graph):
    #data aggregation functions
    graph_data.data = data_changes
    #you can easily add more values that can be changed, but these are the most likely ones to be changed
    for item in frame_change_items:
        if item == None:
            continue
        elif item == "title": #title dosen't seem to work, graph dosen't upate, but the ranges should work for a bar graph. TODO
            scout_graph.title = frame_change_items[item]
        elif item == "y_range":
            scout_graph.y_range.factors = frame_change_items[item]
        elif item == "x_range":
            scout_graph.x_range.factors = frame_change_items[item]
        elif item == "background_fill_color":
            scout_graph.background_fill_color.factors = frame_change_items[item]


#graph_data is the column data source defined earlier
#figure args is a list of arguments you want to pass into your figure, depending on what type of graph you want to make
#graph args is a list of arguments you want to pass into the figure, depending on your graph type
#defaut graph values is a list of the default values you want to pass into the data refresh the first time the function is run
def init_graph(figure_args,graph_args):
    scout_graph = plotting.figure(**figure_args)
    scout_graph.scatter(source = graph_args)
    return scout_graph

#add any extra widgets and widget callbacks
def def_and_show_layout(scout_graph,widget_args):
    fin_layout = layouts.row(scout_graph,*widget_args)
    plotting.curdoc().add_root(fin_layout)