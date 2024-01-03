import pickle
import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap, dodge
from math import pi
from bokeh.layouts import column, row, grid, gridplot
from bokeh.palettes import Set3
from bokeh.plotting import figure, show
from bokeh.transform import cumsum
import viewer.app.data as data 

class StartingPos:
    def __init__(self):
        self.layout = None
        self.measures = None
        self.matches = None

    def prepare_data(self, matches, measures):
        # finds last match in measures
        last_row = measures.iloc[-1]
        lm = last_row[0]
        last_match = int(lm.split("m")[1])
        # filters matches to qm matches only and converts to numbered matches
        qmmatch = matches[matches.match.str.startswith("qm") == True].copy()
        new = qmmatch["match"].str.split("m", expand = True)
        qmmatch["match_number"] = new[1]
        qmmatch["match_number"] = pd.to_numeric(qmmatch["match_number"])

        # filters qmmatches to matches before last match in measures
        lmatches = qmmatch[qmmatch.match_number <= last_match]
        lmatches

        matches_played = (lmatches.groupby("team_number")
                        .size()
                        .reset_index()
                        .set_index("team_number")
                        .rename({0: "matches_played"}, axis="columns")
                        )

        measures = measures[measures.team_number.str.startswith("frc") == True]
        measures = measures[measures.task == "start_pos"]

        pichart = (
            measures.groupby(["team_number", "measure1"])
            .size()
            .unstack("measure1")
            .merge(matches_played, on='team_number') # error ?
        )

        pi2 = pichart.drop("matches_played", axis=1)
        return pi2

    def graph_plot(self):
        measures = data.get_data()[0] 
        matches = data.get_data()[1]
        pi2 = self.prepare_data(matches, measures)

        plist = []
        pgrid = []
        count = 0
        for index, row in pi2.iterrows():
            team = row
            data2 = team.reset_index(name="value").rename(columns={"index": "position"}).fillna(0)
            
            data2["angle"] = data2["value"]/data2["value"].sum() * 2*pi
            data2["color"] = Set3[len(team)]
            
            p = figure(height=350, title= team.name, toolbar_location=None,
                tools="hover", tooltips="@position: @value", x_range=(-0.5, 1.0))

            p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum("angle", include_zero=True), 
                    end_angle=cumsum('angle'),line_color="white", fill_color='color', 
                    legend_field="position", source=data2)
            
            p.axis.axis_label = None
            p.axis.visible = False
            p.grid.grid_line_color = None
            
            plist.append(p)
            count = count + 1
            if count%6==0:
                pgrid.insert(int(count/6) - 1, plist)
                plist = []
        pgrid.insert(int(count/6), plist)
        return pgrid
        
    def get_layout(self):
        pgrid = self.graph_plot()
        self.layout = gridplot(pgrid, plot_width = 250, plot_height = 250)
        return self.layout

    def refresh(self):
        pgrid = self.graph_plot()
        self.layout.children[0] = gridplot(pgrid, plot_width = 250, plot_height = 250)
