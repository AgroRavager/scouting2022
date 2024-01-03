import pandas as pd
import server.database as database
import pandas as pd
import bokeh.io as io
import bokeh.models as models 
from bokeh.models import MultiChoice
import bokeh.plotting as plotting
import bokeh.resources as resources
from bokeh.models import ColumnDataSource
import math
import bokeh.palettes
import numpy as np
from bokeh.layouts import column
import viewer.app.data as data

class CountPlot:
    def __init__(self, inittasks, alltasks):
        self.inittasks = inittasks
        self.alltasks = alltasks
        self.multi_choice = None
        self.layout = None

    def _callback(self, attr, old, new):
        if len(new) < 3:
            self.multi_choice.update(value=old)
        else:
            plot = self.graph_plot() 
            self.layout.children[0] = plot

    def get_layout(self): 
        self.multi_choice = MultiChoice(value=self.inittasks,
                                        options=self.alltasks)
        self.multi_choice.on_change("value", self._callback)
        self.layout = column(self.graph_plot(), self.multi_choice)
        return self.layout
    
    def prepare_data(self, measuresdf):
        measuresdf = measuresdf[measuresdf['team_number'].str.contains('frc')]
        melted_measures = measuresdf.melt(
            id_vars=["match", "team_number", "phase", "task", "measure_type"],
            value_vars=["measure1", "measure2"],
            var_name="measure_col")
        
        counts = melted_measures[melted_measures.measure_type == "count"].copy()
        counts["value"] = pd.to_numeric(counts.value)
        counts["value"] = counts.value.replace(-1, np.nan)

        counts['team_number']=pd.to_numeric(counts['team_number'].str[3:])
        counts.sort_values(by = ['team_number'], inplace = True)

        means = counts.pivot_table(
                    "value",
                    index=["team_number", "task", "measure_col"],
                    columns=["phase"])
        means = means.fillna(0).unstack(["task", "measure_col"]).reset_index().copy() 
        means.sort_values(by = ['team_number'], inplace = True)
        means['team_number','',''] = means['team_number','',''].astype(str)
        cds = ColumnDataSource(means)
        return cds

        # cds["auto_upper_measure1"] = cds["auto_upper_measure1"] * 4

    
        
    def graph_plot(self):
        measures = data.get_data()[0]
        filtered = self.prepare_data(measures)
        tasks = self.multi_choice.value
        plot = plotting.figure(
            x_range = np.unique(filtered.data["team_number__"]),
            x_axis_label="Team",
            y_axis_label="Average Successes",
            title= "Successes",
            tools = "hover", 
            tooltips = "@team_number__ $name: @$name",
            width=1200, height=500)
        
        vbar = plot.vbar_stack(tasks,
                        x = "team_number__", 
                        color = bokeh.palettes.Paired[len(tasks)], 
                        width = 0.9,
                        source = filtered)

        legend_items = [(lbl, [glyph]) for lbl, glyph in zip(tasks, vbar)]
        legend = models.Legend(items = legend_items, location = "top_right") 
        plot.add_layout(legend, 'right')

        plot.xaxis.major_label_orientation = math.pi/4
        return plot

    def refresh(self):
        self._callback("value", self.multi_choice.value, self.multi_choice.value)


