import pickle
import numpy as np
import pandas as pd
import bokeh.models as models
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap, dodge
from math import pi
from bokeh.layouts import column, row, grid, gridplot
from bokeh.palettes import Set3
from bokeh.plotting import figure, show
from bokeh.transform import cumsum
import viewer.app.data as data
from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.models import TableColumn, DataTable
import bokeh.palettes
from bokeh.models import CustomJS, Select


class SixTeamChart: 
    def __init__(self, match):
        self.measures = data.get_data()[0]
        self.layout = None
        self.matches = data.get_data()[1]
        self.select = None
        self.match = match
    
    def prepare_data(self, measures, matches, match):
        teams = list(matches[matches.match == match]["team_number"])
        fullmatch = []
        climb_len = 0
        for team in teams:
            color = list(matches[(matches.team_number == team) & (matches.match == match)]["alliance"])[0]

                
            m = measures[measures.team_number == team].copy()
            m['phase_task'] = m['phase'] + "_" + m['task']
            m = m[["match", "team_number", "phase_task", "measure1"]]
            filter1 = m["phase_task"].isin(["auto_upper", "auto_lower", "tele_upper", "tele_lower", "endgame_hangar_level_end"])
            m = m[filter1]

            m["measure1"] = m["measure1"].astype("int32")

            tele_up, tele_low, auto_up, auto_low = 0, 0, 0, 0
            if("tele_upper" in m["phase_task"].unique()):
                tele_up = round(m[m["phase_task"] == "tele_upper"]["measure1"].sum() * 2/(len(m[m["phase_task"] == "tele_upper"]["measure1"])), 1)
            if("tele_lower" in m["phase_task"].unique()):
                tele_low = round(m[m["phase_task"] == "tele_lower"]["measure1"].sum()/(len(m[m["phase_task"] == "tele_lower"]["measure1"])), 1)
            if("auto_upper" in m["phase_task"].unique()):
                auto_up = round(m[m["phase_task"] == "auto_upper"]["measure1"].sum() * 4/(len(m[m["phase_task"] == "auto_upper"]["measure1"])), 1)
            if("auto_lower" in m["phase_task"].unique()):
                auto_low = round(m[m["phase_task"] == "auto_lower"]["measure1"].sum() * 2/(len(m[m["phase_task"] == "auto_lower"]["measure1"])), 1)
            if('endgame_hangar_level_end' in m['phase_task'].unique()):
                level = list(m[m['phase_task'] == 'endgame_hangar_level_end']['measure1'])
                sum = 0
                for i in level:
                    if (i != 0):
                        climb_len +=1
                    if (i == 1):
                        i = 4
                    if (i == 2):
                        i = 6
                    if (i == 3):
                        i = 10
                    if (i == 4):
                        i = 15
                    sum += i
                if(climb_len == 0):
                    hangar = 0
                else:
                    hangar = round(sum / climb_len, 1)
            bob = [team, color, tele_up, tele_low, auto_up, auto_low, hangar]
            fullmatch.append(bob)
        df = pd.DataFrame(fullmatch, columns = ["team", "color", "tele_up", "tele_low", "auto_up", "auto_low", "hangar"])
        return df

    def graph_plot(self):
        self.measures = data.get_data()[0]
        self.matches = data.get_data()[1]
        match = self.select.value
        df = self.prepare_data(self.measures, self.matches, match)

        source = df

        p = figure(x_range = df["team"].unique(),
                y_range = (0,45), 
                title = "Six Team Chart", 
                x_axis_label="Team",
                y_axis_label="Average Points",
                plot_width = 600, 
                height = 400, 
                toolbar_location = None, 
                tools="hover", tooltips="@team: @color, $name: @$name")

        vbar = p.vbar_stack(["auto_low", "auto_up", "tele_low", "tele_up","hangar"],
                                    x = "team", 
                                    color = bokeh.palettes.Paired[5][:], 
                                    width = 0.9,
                                    source = source)

        legend_items = [(lbl, [glyph]) for lbl, glyph in zip(['auto_low', 'auto_up', 'tele_low', 'tele_up','hangar'], vbar)]

        legend = models.Legend(items = legend_items, location = "top_right") 
        p.add_layout(legend, 'right')

        return p
    
    def get_layout(self):
        self.select = Select(value=self.match, options = list(self.matches.match.unique()))
        self.select.on_change("value", self._callback)
        self.layout = column(self.graph_plot(), self.select)
        return self.layout

    def _callback(self, attr, old, new):
        plot = self.graph_plot()
        self.layout.children[0] = plot

    
    def refresh(self):
        self._callback("value", self.select.value, self.select.value)
