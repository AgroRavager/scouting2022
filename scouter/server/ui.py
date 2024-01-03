import flask
import flask_socketio

# Initialize Flask app and configure the secret key
app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "1737124"

# Initialize Flask-SocketIO
socketio = flask_socketio.SocketIO(app)

@app.route("/set-measure/<match_id>/<int:team_number>/<any(auto, teleop, endgame):phase>/<task>/<result>")
def set_measure(match_id, team_number, phase, task, result):
    """
    A route to handle setting a measure for a team in a match. 
    Currently returns a placeholder response.

    Args:
        match_id (str): The ID of the match.
        team_number (int): The number of the team.
        phase (str): The phase of the match (auto, teleop, endgame).
        task (str): The task being measured.
        result (str): The result of the task.

    Returns:
        str: A placeholder HTML response.
    """
    # TODO: Implement the logic for setting a measure
    return "<p>How did it take you this long to figure it out<p>"

@app.route("/station/<any(blue, red):alliance>/<int(min=1, max=3):station_number>/")
def displayTeam(alliance, station_number):
    """
    Displays the team information for a specific alliance and station.

    Args:
        alliance (str): The alliance color (blue or red).
        station_number (int): The station number (1 to 3).

    Returns:
        Rendered HTML template with alliance and station number.
    """
    # TODO: Implement the logic for displaying team information
    return flask.render_template("index.html", alliance=alliance, station_number=station_number)

@app.route("/")
def index():
    """
    The main index route that renders the homepage.

    Returns:
        Rendered HTML for the index page.
    """
    # TODO: Implement additional logic for the homepage if necessary
    return flask.render_template("index.html")

if __name__ == "__main__":
    # Run the Flask app with SocketIO on port 8131
    socketio.run(app, port=8131, debug=True)
