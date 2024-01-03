import json
import pathlib
import urllib.request
import urllib.error
import sys

import bokeh.layouts as bklayouts
import bokeh.models as bkmodels
import pandas as pd


DATA_FILE_NAME = "viewer_data.json"
path = pathlib.Path(__file__).parent.absolute().joinpath(DATA_FILE_NAME)
if len(sys.argv) > 1:
    flask_server_ip = sys.argv[1]
else:
    flask_server_ip = "127.0.0.1"

# A tuple of four dataframes: measures, matches, status, teams
viewer_data = None


class ViewerDataError(Exception):
    pass


def convert_json(jdata):
    """Converts JSON string from Flask server into dict of DataFrames
    
    Args: jdata can be a JSON string, or a Python data strcuture created
        by json.load() or json.loads().

    Returns: A dictionary of four pandas DataFrames
    """

    if isinstance(jdata, str):
        jdata = json.loads(jdata)

    return {
        "measures": pd.DataFrame(jdata["measures"]),
        "matches": pd.DataFrame(jdata["matches"]),
        "status": pd.DataFrame(jdata["status"]),
        "teams": pd.DataFrame(jdata["teams"]),
    }


def get_data_from_server():
    """Downloads data from server as JSON"""
    global viewer_data
    url = f"http://{flask_server_ip}:8131/viewerdata"
    print("Downloading data from", url)
    viewer_data_json = urllib.request.urlopen(url).read().decode("utf-8")
    print(f"Downloaded {len(viewer_data_json)} characters of JSON data.")
    viewer_data = convert_json(viewer_data_json)
    with open(path, "wt") as jfile:
        jfile.write(viewer_data_json)
    print("Scouting data saved to", path)


def get_data():
    """Creates or returns tuple of dataframes."""
    global viewer_data
    if viewer_data is None:
        if not path.is_file():
            try:
                get_data_from_server()
            except urllib.error.URLError:
                raise ViewerDataError
        else:
            print("Reading Viewer Data from", str(path))
            with open(path, "rt") as jfile:
                viewer_data = convert_json(json.load(jfile))
    return (
        viewer_data["measures"],
        viewer_data["matches"],
        viewer_data["status"],
        viewer_data["teams"]
    )


class RefreshData:
    def __init__(self, graphlist):
        self.graphlist = graphlist

    def refresh_graphs(self):
        get_data_from_server()
        for graph in self.graphlist:
            try:
                graph.refresh()
            except BaseException as err:
                print(err)

    def get_layout(self):
        divtext = """
        <h2>To Refresh Scouting Data ...</h2>
        <ol>
        <li>Connect to the network that is running the scouting server.</li>
        <li>Press the <i>Refresh from Server</i> button below.</li>
        </ol>
        """
        divwidget = bkmodels.Div(text=divtext)
        btn = bkmodels.Button(label="Refresh from Server", button_type="primary")
        btn.on_click(self.refresh_graphs)
        layout = bklayouts.column(divwidget, btn)
        return layout
