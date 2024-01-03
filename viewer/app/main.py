from bokeh.plotting import curdoc, figure
from bokeh.models import Panel, Tabs, Div
from bokeh.layouts import column, row, grid, gridplot

import viewer.app.CountPlot as cp
import viewer.app.StartingPos as sp
import viewer.app.TabularPlot as tabp
import viewer.app.data as data
import viewer.app.SixTeamChart as stc 
import viewer.app.OneTeam as oneteam
import viewer.app.defense_table as dft
import viewer.app.TotalPointsGraph as totalpoints
import viewer.app.TotalPointsTable as totaltable


div = Div(text="""<h1>Welcome to the IRS 1318 Scouting Homepage!</h1>""" )

inittasks = ["auto_upper_measure1",
            "tele_upper_measure1",
            "tele_lower_measure1",
            "auto_lower_measure1",
            "endgame_hangar_level_end_measure1"]

alltasks = ["auto_pickup-field_measure1",
            "auto_pickup-terminal_measure1",
            "auto_upper_measure1",
            "tele_upper_measure1",
            "auto_lower_measure1",
            "tele_lower_measure1",
            "auto_upper_measure2",
            "tele_upper_measure2",
            "auto_lower_measure2",
            "tele_lower_measure2",
            "auto_hp_measure1",
            "auto_hp_measure2",
            "tele_pickup-field_measure1",
            "tele_pickup-terminal_measure1",
            "endgame_hangar_level_end_measure1"]

try:
    cplot = cp.CountPlot(inittasks, alltasks)
    tab1 = Panel(child=cplot.get_layout(), title="Count Plot")
except BaseException as err:
    tab1 = Panel(child=Div(text=f"<code>{err}</code>"), title="Count Plot")

try:
    totalpointgraph = totalpoints.TotalPointsGraph()
    tab2 = Panel(child=totalpointgraph.get_layout(), title="Total Points")
except BaseException as err:
    tab2 = Panel(child=Div(text=f"<code>{err}</code>"), title="Total Points")

try:
    totaltable = totaltable.TotalTable()
    tab25 = Panel(child = totaltable.get_layout(), title="Total Table")
except BaseException as err:
    tab25 = Panel(child=Div(text=f"<code>{err}</code>"), title="Total Table")

try:
    tplot = tabp.TabularPlot()
    tab3 = Panel(child=tplot.get_layout(), title="Table Plot")
except BaseException as err:
    tab3 = Panel(child=Div(text=f"<code>{err}</code>"), title="Table Plot")

try:
    sixplot = stc.SixTeamChart("qm1")
    tab4 = Panel(child=sixplot.get_layout(), title = 'Six Team Chart')
except BaseException as err:
    tab4 = Panel(child=Div(text=f"<code>{err}</code>"))

try:
    teamplot = oneteam.OneTeam()   
    tab5 = Panel(child=teamplot.get_layout(), title = "One Team")
except BaseException as err:
    tab5 = Panel(child=Div(text=f"<code>{err}</code>"), title = "One Team")

try:
    dftable = dft.defense_table()
    tab6 = Panel(child=dftable.get_layout(), title = "Defense Table")
except BaseException as err:
    tab6 = Panel(child=Div(text=f"<code>{err}</code>"), title = "Defense Table")

try:
    splot = sp.StartingPos()
    tab7 = Panel(child=splot.get_layout(), title='Position Plot')
except BaseException as err:
    tab7 = Panel(child=Div(text=f"<code>{err}</code>"), title='Position Plot')

try:
    refreshclass = data.RefreshData([cplot, sixplot, teamplot, tplot, dftable, splot, totalpointgraph])
    tab8 = Panel(child=refreshclass.get_layout(), title="Refresh Data")
except BaseException as err:
    tab8 = Panel(child=Div(text=f"<code>{err}</code>"), title="Refresh Data")

column = column(div, Tabs(tabs=[tab1, tab2, tab25, tab3, tab4, tab5, tab6, tab7, tab8]))
curdoc().add_root(column)