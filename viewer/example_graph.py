import viewer_main as view

#this bit of code when run with in a bokeh server makes a simple scatter plot graph with number on 1-5,
#and has a button that when clicked, makes the points go to 2-10.

#this function makes a button callback that will update data that you give to it
def button_callback(event):
    print("click")
    view.data_refresh(graph_cds,{"x":[2,4,6,8,10],"y":[2,4,6,8,10]},{"title":"( ͡° ͜ʖ ͡°)","height":1000},scout_graph)
    print("click")
#
button = view.models.Button(label="click", button_type="success")
button.on_click(button_callback)
widget_args = [button]

figure_args = {"title":"title"}
graph_cds = view.plotting.ColumnDataSource({"x":[1,2,3,4,5],"y":[1,2,3,4,5]})
scout_graph = view.init_graph(figure_args,graph_cds)


button = view.models.Button(label="click", button_type="success")
button.on_click(button_callback)
widget_args = [button]

view.def_and_show_layout(scout_graph,widget_args)