from turtle import title
import pandas as pd
import bokeh.io as io
import bokeh.models as models
import bokeh.plotting as plotting
import bokeh.resources as resources
import bokeh.layouts as layouts
from bokeh.palettes import Category20b
import pickle

# The vif.pickle file contains scouting data from the
# 2020 Glacier Peak competition.
tasks_graph = {}
with open("vif.pickle", "rb") as sfile:
    sdata = pickle.load(sfile)
for key in sdata.keys():
    locals()[key] = sdata[key]
ttd_cds = models.ColumnDataSource({'teams':[],"movedAuto":[],"pickupPowerCellsG":[],"launchInner":[],"launchOuter":[],"launchLower":[],"defense":[]})

#pivots the table and selects a couple rows i want to use
team_restrict = list(set(measures["team"]))
tasks_restrict = list(set(measures["task"]))
agg_options = ["sum","mean"]
def remake_data(team_include, tasks_include, agrefunct):
    frame = measures[["team","task","successes"]]
    frame = frame.pivot_table(index = "task", columns = "team", values = "successes", aggfunc = agrefunct)#could make this all one line
    frame = frame.filter(items = tasks_include, axis = 0)
    frame = frame.filter(items = team_include)
    frame = frame.fillna(0)#replacing all the NaN values with 0

    #returns a couple lists that i can use when making a chart
    tasks = list(frame.index)
    teams = list(frame.columns)
    a1 = []
    for value in teams[0:3]:
        a1.append("1")
    a2 = []
    for value in teams[3:]:
        a2.append("2")

    teams1 = list(zip(a1,teams[0:3]))
    teams2 = list(zip(a2,teams[3:]))
    #teams = teams1+teams2
    #making the data into a structure (that i kinda stole from the bokeh documentation)
    ttd = {"teams" : teams,}#task team dict
    for item in tasks:
        ttd[item] = list(frame.loc[item])
    print("data defined")
    if type(tasks_graph) != dict:
        tasks_graph.title = "title"
        print("title changed")
        tasks_graph.y_range.factors = teams
    ttd_cds.data = ttd
    return teams, tasks, ttd, ttd_cds, agrefunct


tetalst = [team_restrict,tasks_restrict,agg_options[0]]
teams, tasks, ttd, ttd_cds , agrefunct = remake_data(tetalst[0],tetalst[1],tetalst[2])

#defining the chart
tasks_graph = plotting.figure(y_range = models.FactorRange(factors=teams), height = 625, title = "teams based on tasks preformed")
    
#defining the data in the graph
tasks_graph.hbar_stack(stackers=tasks, y="teams", height = 0.8, color = Category20b[len(tasks)], source = ttd_cds, legend_label = tasks)
tasks_graph.x_range.start = 0
#tasks_graph.legend.location = "bottom_right"

tup_teams = [team_value[1] for team_value in teams]

#defining widgets


def agg_change(agg_attr, agg_old, agg_new):
    print(agg_new)
    agg_new = agg_options[agg_new]
    tetalst[2] = agg_new
    print(tetalst[2])
    remake_data(tetalst[0],tetalst[1],tetalst[2])

def team_change(team_attr, team_old, team_new):
    print(team_new)
    tetalst[0] = team_new
    remake_data(tetalst[0],tetalst[1],tetalst[2])

def task_change(task_attr, task_old, task_new):
    print(task_new)
    new_tasks = []
    for number in task_new:
        new_tasks.append(tasks_restrict[number])
    tetalst[1] = new_tasks
    remake_data(tetalst[0],tetalst[1],tetalst[2])
task_choice = models.CheckboxGroup(labels = tasks, active = list(range(len(tasks))))
team_choice = models.MultiChoice(options = teams, value = team_restrict)
agg_choice = models.RadioGroup(labels = ["sum","average"], active = 0)
task_choice.on_change("active",task_change)
team_choice.on_change("value",team_change)
agg_choice.on_change("active",agg_change)




#defining a layout
pres_layout = layouts.row(
            tasks_graph,
            team_choice,
            task_choice,
            agg_choice
)
plotting.curdoc().add_root(pres_layout)
#plotting.curdoc().add_root(team_choice2)
