import pandas as pd
import viewer.app.data as data
import bokeh.layouts as layouts
import bokeh.models as models
import bokeh.plotting as plotting
from bokeh.layouts import column

class defense_table:

    def __init__(self):
        self.layout = layouts.row([])
        self.measures = None
        self.matches = None

    def prepare_data(slef,measures):
        defenses_table = measures[measures.task.isin(["defense", "defended_against"])]
        defense_table = defenses_table[defenses_table.task == "defense"]
        defended_against_table = defenses_table[defenses_table.task == "defended_against"]

        defense_table = defense_table.drop(["match","measure2","measure_type","phase","task"], axis = 1)
        defended_against_table = defended_against_table.drop(["match","measure2","measure_type","phase","task"], axis = 1)

        defense_table["measure1"] = defense_table["measure1"].apply(pd.to_numeric)
        defended_against_table["measure1"] = defended_against_table["measure1"].apply(pd.to_numeric)

        defense_table = defense_table.groupby("team_number").mean().sort_values(by="measure1", ascending = False)
        defended_against_table = defended_against_table.groupby("team_number").mean().sort_values(by="measure1", ascending = False)

        defense_table = defense_table.round(2)
        defended_against_table = defended_against_table.round(2)


        defense_table = plotting.ColumnDataSource(defense_table.rename({"measure1":"average defense score"}))
        defended_against_table = plotting.ColumnDataSource(defended_against_table.rename({"measure1":"average defended against score"}))
        return defense_table, defended_against_table


    def graph_plot(self):
        measures = data.get_data()[0]
        defense_table, defended_against_table = self.prepare_data(measures)
        bk_defense_table_columns = [models.TableColumn(field = "team_number", title = "team_number"),
                                    models.TableColumn(field = "measure1", title = "average defense score")]

        bk_defended_against_table_columns = [models.TableColumn(field = "team_number", title = "team_number"),
                                            models.TableColumn(field = "measure1",
                                                                title = "average defended against score")]                        
        bk_defense_table = models.DataTable(source = defense_table,
                                            columns = bk_defense_table_columns)

        bk_defended_against_table = models.DataTable(source = defended_against_table,
                                                    columns = bk_defended_against_table_columns)


        return [bk_defense_table,bk_defended_against_table]

    def refresh(self):
        self.layout.children[0] = column(self.graph_plot())

    def get_layout(self):
        self.layout = column(self.graph_plot())
        return self.layout

