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
from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.models import TableColumn, DataTable

class TabularPlot:
    def __init__(self):
        self.layout = None
        self.measures = None
        self.matches = None

    def prepare_data(self, measures):
        melted_measures = measures.melt(
            id_vars=["match", "team_number", "phase", "task", "measure_type"],
            value_vars=["measure1", "measure2"],
            var_name="measure_col")
        
        counts = melted_measures[melted_measures.measure_type == "count"].copy()
        counts["value"] = pd.to_numeric(counts.value)
        counts["value"] = counts.value.replace(-1, np.nan)

        means = counts.pivot_table(
            "value",
            index=["team_number", "task", "measure_col"],
            columns=["phase"])
        means = means.fillna(0)

        filtered = means.unstack(["task", "measure_col"])
        nan_value = float("NaN")
        filtered = filtered.replace(0, nan_value)
        filtered = filtered.dropna(how="all", axis=1)
        return filtered

    def graph_plot(self):
        measures = data.get_data()[0]
        filtered = self.prepare_data(measures)
        filtered = filtered.fillna(0).round(1)
        source = ColumnDataSource(filtered)

        bobbo = ["team_number", "auto_hp_measure1", "auto_lower_measure1", "auto_upper_measure1", 
         "tele_lower_measure1", "tele_upper_measure1",
         "endgame_hangar_level_end_measure1", "endgame_penalty_count_measure1"]

        bobbo2 = []
        for i in bobbo:
            if i.__contains__("measure1"):
                i = i.replace("measure1", "make")
            bobbo2.append(i)
            
        auto = []
        tele = []
        end = []
                
        auto.append(TableColumn(field = bobbo[0], title = bobbo2[0].replace("_", " ")))
        tele.append(TableColumn(field = bobbo[0], title = bobbo2[0].replace("_", " ")))
        end.append(TableColumn(field = bobbo[0], title = bobbo2[0].replace("_", " ")))

            
        columns = []
        for i in range(0, len(bobbo)):
            columns.append(TableColumn(field = bobbo[i], title = bobbo2[i].replace("_", " ")))

            if(bobbo[i].__contains__("auto")):
                auto.append(TableColumn(field = bobbo[i], title = bobbo2[i].replace("_", " ")))


            elif(bobbo[i].__contains__("tele")):
                tele.append(TableColumn(field = bobbo[i], title = bobbo2[i].replace("_", " ")))

            elif(bobbo[i].__contains__("endgame")):
                end.append(TableColumn(field = bobbo[i], title = bobbo2[i].replace("_", " ")))
                

        auto_table = DataTable(source=source, columns=auto, width=1100)
        tele_table = DataTable(source=source, columns=tele, width=1100)
        end_table = DataTable(source=source, columns=end, width=1100)

        return column(auto_table, tele_table, end_table) 
    
    def get_layout(self):
        self.layout = self.graph_plot()
        return self.layout
    
    def refresh(self):
        self.layout.children[0] = self.graph_plot()
