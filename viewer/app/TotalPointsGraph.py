import bokeh.io as io
import bokeh.models as models
import bokeh.plotting as plotting
import bokeh.resources as resources
import pandas as pd
from bokeh.models import ColumnDataSource
import math
from bokeh.io import output_notebook
import bokeh.palettes
import pickle
import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap, dodge
import math
from bokeh.layouts import column, row, grid, gridplot

import viewer.app.data as data

class TotalPointsGraph:
    def __init__(self):
        self.layout = None
    
    def refresh(self):
        self.layout = self.graph_plot()

    def get_layout(self):
        self.layout = self.graph_plot()
        return self.layout
    
    def prepare_data(self):
        measures = data.get_data()[0]
        measures = measures[measures['team_number'].str.contains('frc')].copy()
        measures['measure1'] = measures['measure1'].replace(['true'],2).copy()
        measures['measure1'] = measures['measure1'].replace(['false'],0).copy()
        
        teams = list(measures['team_number'].unique())
        allteams = []
        for team in teams:
            m = measures[measures.team_number == team].copy()
            m['phase_task'] = m['phase'] + "_" + m['task']
            m = m[['match', 'team_number', 'phase_task', 'measure1']]
            filter1 = m['phase_task'].isin(['auto_upper', 'auto_lower', 'tele_upper', 'tele_lower', 'endgame_hangar_level_end', 'auto_taxi'])
            m = m[filter1]

            m['measure1'] = m['measure1'].astype('int32')

            tele_up, tele_low, auto_up, auto_low, auto_taxi = 0, 0, 0, 0, 0
            if('tele_upper' in m['phase_task'].unique()):
                tele_up = round(m[m['phase_task'] == 'tele_upper']['measure1'].sum() * 2/(len(m[m['phase_task'] == 'tele_upper']['measure1'])), 1)
            if('tele_lower' in m['phase_task'].unique()):
                tele_low = round(m[m['phase_task'] == 'tele_lower']['measure1'].sum()/(len(m[m['phase_task'] == 'tele_lower']['measure1'])), 1)
            if('auto_upper' in m['phase_task'].unique()):
                auto_up = round(m[m['phase_task'] == 'auto_upper']['measure1'].sum() * 4/(len(m[m['phase_task'] == 'auto_upper']['measure1'])), 1)
            if('auto_lower' in m['phase_task'].unique()):
                auto_low = round(m[m['phase_task'] == 'auto_lower']['measure1'].sum() * 2/(len(m[m['phase_task'] == 'auto_lower']['measure1'])), 1)
            if('endgame_hangar_level_end' in m['phase_task'].unique()):
                level = list(m[m['phase_task'] == 'endgame_hangar_level_end']['measure1'])
                sum = 0
                for i in level:
                    if (i == 1):
                        i = 4
                    if (i == 2):
                        i = 6
                    if (i == 3):
                        i = 10
                    if (i == 4):
                        i = 15
                    sum += i
                hangar = round(sum / len(m[m['phase_task'] == 'endgame_hangar_level_end']['measure1']), 1)
            if('auto_taxi' in m['phase_task'].unique()):
                taxi = round(m[m['phase_task'] == 'auto_taxi']['measure1'].sum()/(len(m[m['phase_task'] == 'auto_taxi']['measure1'])), 1)
            pointslist = [team, tele_up, tele_low, auto_up, auto_low, hangar, taxi]
            allteams.append(pointslist)
        df = pd.DataFrame(allteams, columns = ['team', 'tele_up', 'tele_low', 'auto_up', 'auto_low', 'hangar', 'taxi'])
        df['total_points'] = df["tele_up"] + df["tele_low"] + df["auto_up"] + df["auto_low"] + df['hangar'] + df['taxi']
        for i in range(0, len(df['team'])):
            df['team'].loc[i] = int(df['team'].iloc[i][3:])
        df.sort_values(by = ['team'], inplace = True)
        df['team'] = df['team'].astype(str)
        return df

    def graph_plot(self):
        filtered = self.prepare_data()
        filtered = ColumnDataSource(filtered)
        plot = plotting.figure(x_range = filtered.data["team"],
            x_axis_label="Team",
            y_axis_label="Average Points",
            title= "Points",
            tools = "hover", 
            tooltips = "@team $name: @$name",
            width=1200, height=500)
        tasks = ['tele_up', 'tele_low', 'auto_up', 'auto_low', 'hangar', 'taxi']

        vbar = plot.vbar_stack(tasks,
                                x = "team", 
                                color = bokeh.palettes.Paired[len(tasks)], 
                                width = 0.9,
                                source = filtered)

        legend_items = [(lbl, [glyph]) for lbl, glyph in zip(tasks, vbar)]
        legend = models.Legend(items = legend_items, location = "top_right") 
        plot.add_layout(legend, 'right')

        plot.xaxis.major_label_orientation = math.pi/4
        return plot




    

