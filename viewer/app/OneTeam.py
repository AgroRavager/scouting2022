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
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap, dodge
import math
from bokeh.layouts import column, row, grid, gridplot
import bokeh.models as models
import viewer.app.data as data

class OneTeam:
    def __init__(self):
        self.measures = data.get_data()[0]
        self.matches = data.get_data()[1] 
        self.layout = None
        self.select = None
        self.team = 'frc1318'
    
    def prepare_data(self):
        self.team = self.select.value
        self.measures = data.get_data()[0]
        self.matches = data.get_data()[1]
        m = self.measures[self.measures.team_number == self.team].copy()
        m['phase_task'] = m['phase'] + "_" + m['task']
        m = m[['match', 'team_number', 'phase_task', 'measure1']].copy()
        filter1 = m['phase_task'].isin(['auto_upper', 'auto_lower', 'tele_upper', 'tele_lower', 'endgame_hangar_level_end'])
        m = m[filter1]

        tele_up, tele_low, auto_up, auto_low, hangar = ['tele_up'], ['tele_low'], ['auto_up'], ['auto_low'], ['hangar']
        tasks = ['tele_upper', 'tele_lower', 'auto_upper', 'auto_lower', 'endgame_hangar_level_end']
        for i in range(0, len(m)):
            if(m.iloc[i]['phase_task'] == 'tele_upper'):
                tele_up.append(m.iloc[i]['measure1'])
            if(m.iloc[i]['phase_task'] == 'tele_lower'):
                tele_low.append(m.iloc[i]['measure1'])
            if(m.iloc[i]['phase_task'] == 'auto_upper'):
                auto_up.append(m.iloc[i]['measure1'])
            if(m.iloc[i]['phase_task'] == 'auto_lower'):
                auto_low.append(m.iloc[i]['measure1'])
            if(m.iloc[i]['phase_task'] == 'endgame_hangar_level_end'):
                hangar.append(m.iloc[i]['measure1'])
        
        matches = list(m.match.unique())
        matches.insert(0, 'match')
        big_boi = [['team', self.team], matches, tele_up, tele_low, auto_up, auto_low, hangar]

        for l in range(1, len(big_boi[1])):
            for i in big_boi:
                if(i != big_boi[0]):
                    if (len(big_boi[1]) - len(i)) > 0:
                        i.append('0')
                if(i == big_boi[0]):
                    if (len(big_boi[1]) - len(i)) > 0:
                        i.append(self.team)
        
        dictchart = {'team': big_boi[0][1:], 'match': big_boi[1][1:], 'tele_up': big_boi[2][1:], 'tele_low': big_boi[3][1:], 'auto_up': big_boi[4][1:], 'auto_low':big_boi[5][1:], 'hangar':big_boi[6][1:]}
        df = pd.DataFrame(dictchart)
        df.drop(columns = 'team')

        ls = ['tele_up', 'tele_low', 'auto_up', 'auto_low', 'hangar']

        for i in ls:
            df[i] = df[i].astype('int32')
        return df
    
    def graph_plot(self):
        df = self.prepare_data() 
        source = df

        p = figure(x_range = df['match'],
                y_range = (0,25), 
                title = self.team + " Team Chart",
                x_axis_label="Match",
                y_axis_label="Average Successes", 
                plot_width = 600, 
                height = 400, 
                toolbar_location = None, 
                tools="hover", tooltips="@team @match, $name: @$name")

        vbar = p.vbar_stack(['auto_low', 'auto_up', 'tele_low', 'tele_up','hangar'],
                                    x = 'match', 
                                    color = bokeh.palettes.Paired[5][:], 
                                    width = 0.9,
                                    source = source)
        
        legend_items = [(lbl, [glyph]) for lbl, glyph in zip(['auto_low', 'auto_up', 'tele_low', 'tele_up','hangar'], vbar)]

        legend = models.Legend(items = legend_items, location = "top_right") 
        p.add_layout(legend, 'right')
        return p

    def get_layout(self):
        team_list = list(self.measures.team_number.unique())
        team_list2 = []
        for ind, team in enumerate(team_list):
            if team.startswith('frc'):
                team_list2.append(team_list[ind])
        team_list2.sort(key=lambda x: int(x[3:]))
        self.select = Select(value=self.team, options = team_list2)
        # self.select = Select(value=self.team, options = list(self.measures.team_number.unique()))
        self.select.on_change("value", self._callback)
        self.layout = column(self.graph_plot(), self.select)
        return self.layout

    def _callback(self, attr, old, new):
        plot = self.graph_plot()
        self.layout.children[0] = plot
        
    def refresh(self):
        self._callback("value", self.select.value, self.select.value)
