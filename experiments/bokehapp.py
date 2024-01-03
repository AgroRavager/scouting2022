import bokeh.io as io
import bokeh.models as models
import bokeh.plotting as plotting
import bokeh.resources as resources
import pandas as pd
from bokeh.models import ColumnDataSource
import bokeh.layouts as layouts
import math
from bokeh.io import output_notebook
import bokeh.palettes

import pickle

# The vif.pickle file contains scouting data from the
# 2020 Glacier Peak competition.
with open("vif.pickle", "rb") as sfile:
    sdata = pickle.load(sfile)

measures = sdata["measures"]

measuresnofinish = measures[measures.phase != "finish"]
aggDF = measuresnofinish.pivot_table("successes",["team","task"], "phase")

# make the DF a column data source
aggLaunchDF = aggDF.reset_index()
source = ColumnDataSource(aggLaunchDF) 
colors = ["blue", "green"]

def filter_task(attr, old, new):
    source.data = aggLaunchDF[aggLaunchDF["task"] == new]

filter_task(None, None, "launchOuter")

# figure object
launch_outer_plot = plotting.figure(x_range = aggLaunchDF["team"].unique(),
    x_axis_label="Team",
    y_axis_label="Average Points",
    title="Successes in Launch Outer",
    tools = "hover", 
    tooltips = "@team $name: @$name",
    width=800, height=400)

# plot data
launch_outer_plot.vbar_stack(["teleop","auto"],
                             x = "team", 
                             color = bokeh.palettes.Category10[3][:2], 
                             width = 0.9,
                             source = source, 
                             legend_label = ["teleop","auto"])
# diagonal team names
launch_outer_plot.xaxis.major_label_orientation = math.pi/4
# display the plot
title = models.Div(text = "<h1> Successes in Launch Outer </h1>") 

select = models.Select(title = "Task", value = "launchOuter", options = ["launchLower", "launchOuter", "launchInner"])
select.on_change("value", filter_task)

page_layout = layouts.column([title, launch_outer_plot, select])
plotting.curdoc().add_root(page_layout)