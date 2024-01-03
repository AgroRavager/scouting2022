import json
import sys

import flask
import flask_socketio
from server.event import get_measures

import server.database as database
import server.config
import server.event as event

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "1737124"

socketio = flask_socketio.SocketIO(app)

con = database.get_con()



@app.route("/")
def index():
    """Displays buttons to access scouting stations and command page.

    Args: None

    Returns: nav.html page
    """
    return flask.render_template("index.html")


@app.route("/command")
def getcommand():
    """Displays command.html.

    Args: None

    Returns: command.html page
    """
    return flask.render_template("command.html",
    currentmatch=event.get_current_match())


@app.route("/command/match/<match>")
def setmatch(match):
    """Sets the match.
    
    Runs once a match is manually selected from command.html or runs
    automatically when all 6 scouting stations pressed the finish and
    check-in data button.

    Args: None

    Returns: The new match that is either selected or the next match in
    the table of command.html
    """
    event.set_current_match(match)
    return match


@app.route("/matches")
def matches():
    """Retrieves all of the matches in the database.

    Retrieves all matches and returns as a list. Used in command.js to
    create the match table displayed in command.html.

    Args: None

    Returns: List of all the matches in the database
    """
    return json.dumps(event.get_matches())


@app.route("/currentmatch")
def match():
    """Retrieves the current match.

    Args: None

    Returns: The current match.
    """
    return event.get_current_match()


@app.route("/team/<alliance>/<station>")
def team(alliance, station):
    """Retrieves the team number of a station.
    
    Retrieves the team number based on the match and station.

    Args:
        alliance: "red" or "blue"
        station: "1", "2", "3"

    Returns: Team number of the station
        ex: "1318"
    """
    return event.get_team(event.get_current_match(), alliance, station, ind = 0)


@app.route("/teamname/<alliance>/<station>")
def teamname(alliance, station):
    """Retrieves the team name based of a station.

    Retrieves the team name based on the match and station.

    Args:
        alliance: "red" or "blue"
        station: "1", "2", "3"

    Returns: The team name
        ex: "Issaquah Robotics Society"
    """
    return event.get_team(event.get_current_match(), alliance, station, ind = 1)


@app.route(
    "/station/<any(blue, red):alliance>/<int(min=1, max=3):station_number>/")
def displayTeam(alliance, station_number):
    """Displays the data entry page and loads the station.

    Loads the data entry page and displays the alliance and
    station_number on the page.

    Args:
        alliance: "red" or "blue"
        station_number: "1", "2", "3"

    Returns: Sets the HTML of each station's page with the alliance and
    station_number
    """
    return flask.render_template(
        "data-entry.html", alliance=alliance, station_number=station_number)


@app.route("/set-measure/<match>/<team_number>/<phase>/<task>"
           "/<measure1>/<measure2>/<measure_type>")
def set_measure(
    match, team_number, phase, task, measure1, measure2, measure_type):
    """Sends data to the database.

    Sends measures entered on the data entry page to the database.
    Pressing the finish and check-in button will resend measures.

    Args:
        match
        team_number
        phase
        task
        measure1: Data sent to the database.
        measure2: Used for misses (count) and max stars (rating),
            otherwise will be set to "-1" (count, bool, categorical).
        measure_type: "count", "categorical", "boolean", or "rating"

    Returns: Inserts data into the database.
    """
    server.database.insert_measure(match, team_number, phase, task,
                                   measure1, measure2, measure_type, con=con)
    return (match + " " + team_number + " " + phase + " " + task +
            " " + measure1 + " " + measure2 + " " + measure_type)


@app.route("/nextmatch")
def nextmatch():
    """Retrieves the next match.

    Args: None

    Returns:
        The next match.
        ex: If the current match is qm6, returns qm7
    """
    return event.get_next_match()


@app.route("/checkoutdata/<match>/<args>")
def checkout(match, args):
    """Retrieves a list of all the measures in the database.

    Retrieves all measures from the database. checkoutdata.js uses the
    measures in the database to compare with the UI, ensuring there are
    no errors in the database. retrievedata.js uses the measures to
    replace UI values with the database measures.

    Args:
        match
        args: team_number

    Returns: All measures in the database for the given match
    """
    return json.dumps(get_measures(match, args))


@app.route("/viewerdata")
def get_viewer_data():
    """
    Fetches and formats data for the application's viewer interface. 

    Returns a dictionary with keys 'measures', 'matches', 'teams', and 'status', 
    containing the respective data from the database in JSON format.
    """
    df_dict = database.get_dataframes(con=con)
    vdata = {
        "measures": json.loads(df_dict["measures"].to_json()),
        "matches": json.loads(df_dict["matches"].to_json()),
        "teams": json.loads(df_dict["teams"].to_json()),
        "status": json.loads(df_dict["status"].to_json())
    }
    return vdata


# ALL WEBSOCKETS BELOW HERE

"""Stores connected stations and their ids.

Ids are stored to ensure multiple tablets are not on the same station.
"""
socket_ids = {
    "server": None,
    "red 1": None,
    "red 2": None,
    "red 3": None,
    "blue 1": None,
    "blue 2": None,
    "blue 3": None,
}


"""List of all connected stations

Used to display all connected stations on command.html. Duplicate
stations are not kicked off, but instead the scouting technician can
check if there are multiple connections for one station.
"""
socket_connections = []


@socketio.on("connect")
def connect(station):
    """Runs when a station has connected.

    Stations usually connect when they first open the data entry page.
    command.html will also have a socket connection, though it is not
    included in lists of socket connections. Stations can additionally
    reconnect if they momentarily lose connection.

    Generates a unique id every time there is a new connection; however,
    only the id of the first connection for every station will be added
    to the socket_ids list.

    Adds all connected stations except "server" to a list with all the
    connected stations (socket_connections).

    Args:
        station: The station that has opened a connection. If a page
        other than the data entry page connects, station = "server"
            ex: "blue 2"

    Returns: list of connected stations on command.html
    """
    print("connected")
    socket_id = flask.request.sid

    if (station == "server"):
        flask_socketio.emit("changeConnect", socket_connections, broadcast=True)
        print(station)

    if socket_ids[station] is None:
        socket_ids[station] = socket_id
        socket_connections.append(" "+station)
    elif socket_ids[station] != socket_id:
        if station != "server":
            socket_connections.append(" "+station)
    else: return "connected"


@socketio.on("disconnect")
def disconnect():
    """Runs when a station has disconnected.

    Tablets disconnect when the tab is closed or tablet is shut down.

    Emits to "ondisconnect," which refreshes the list of connected
    stations with currently connected stations. The disconnected station
    should be removed from the list of socket connections.

    Clears the list of socket_connections (all connected stations).

    Args: None

    Returns: Emits to "ondisconnect" and clears socket_connections list
    """
    flask_socketio.emit("ondisconnect", broadcast=True)
    socket_connections.clear()


@socketio.on("disconarray")
def disconarray(connectstation):
    """Runs on disconnect to refresh the socket_connections list.

    Every time a tablet disconnects, all other connected stations are
    readded to the socket_connections list. (The original list is
    cleared in "disconnect") This refreshes the socket connections list
    in command.html.

    Args:
        connectstation: The connected station.
            ex: "blue 2"

    Returns: Refreshes the socket_connections list
    """
    socket_connections.append(connectstation)


@socketio.on("refresh")
def refresh():
    """Refreshes the page and clears values to start on a new match.

    Runs when the match is manually set, there is a manual update, and
    when the finish button is pressed by all 6 stations (automatically
    moving on to the next match). Essentially run whenever the match
    in the data entry or command pages has to change.

    In the javascript function, values on the UI is cleared and the next
    match and team is retrieved.

    Clears the finished_stations list so that tablets have to press the
    finish and check-in data button again.

    Args: None

    Returns: Emits to "reset", clears finished_stations list
    """
    flask_socketio.emit("reset", broadcast=True)
    for x in finished_stations:
        station = x
        print(station)
        flask_socketio.emit("resetFinish", station, broadcast=True)
    finished_stations.clear()


@socketio.on("displayConnect")
def displayConnect():
    """Lists connected stations on command.html.

    Runs whenever a station connects or disconnects. Passes
    socket_connections to the "changeConnect" emit to display on the
    command page.

    Args: None

    Returns: emits socket_connections to "changeConnect"
    """
    flask_socketio.emit("changeConnect", socket_connections, broadcast=True)


"""Keeps track of who has checked in their data.

Stations that pressed the finish and check-in data button are stored in
a set, which doesn't allow for repeat values.
"""
finished_stations = set()


@socketio.on("finished")
def finished(station):
    """ Records finished stations and updates when all stations finish.

    Runs whenever a station presses the finish and check-in data button.
    Stores finished stations in the finished_stations set.

    If there are 6 finished stations, clears finished_stations and
    resets indicators on the command page and data entry pages. Emits to
    "reset" and "setNextMatch" will reset the page to be on a new match
    (resets values on UI, retrieves new match and team).

    Args:
        station: To add to the finished_station set. Example: "blue-3"

    Returns: Adds station to finished_stations.
        If all stations are in finished_stations, refreshes values and
        updates the station to the next match.
    """
    finished_stations.add(station)
    print(finished_stations)
    if len(finished_stations) == 6:
        flask_socketio.emit("reset", broadcast=True)
        flask_socketio.emit("setNextMatch", broadcast=True)

        for x in finished_stations:
            station = x
            flask_socketio.emit("resetFinish", station, broadcast=True)

        finished_stations.clear()

@socketio.on("notifyFinish")
def notifyFinish():
    """Sets indicator at top of each data entry page.

    Runs every time the page loads (If someone has already pressed
    finish, it will display has checked) and every time a tablet
    finishes. Sets the indicator at the top of each data entry page as
    "ready", ready being a filled in circle and not ready being an
    empty circle.

    Args: None

    Returns: Emits "notifyFinish" to set the finish indicator
    """

    for x in finished_stations:
        station = x
        flask_socketio.emit("notifyFinish", station, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, port=8131, host=sys.argv[1], debug=True)