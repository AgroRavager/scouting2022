"""
## Database Schema
teams: each row represents an FRC team.
* team_number (int) PK: Examples: 1318, 2976, 488.
* team_name (text): The name the team is commonly known by, such as
  "Issaquah Robotics Society" or "Frog Force".
* city (text): Examples: "Seattle", "Pullman".
* state (text): Full name of state or province (do not use two-letter postal
   abbreviations), such as "Oregon" or "New South Wales".
* country (text): Name of country. Acronyms, such as USA or UK can be used if
  they are commonly understood.

events: each row represents a specific event.
* code (text): The code of the event given from TheBlueAlliance.
    Examples: "2020wasno".
* year (int): Examples: 2019, 2018, 2022.
* city (text): Examples: "Seattle", "Pullman".
* state (text): Full name of state or province (do not use two-letter postal
   abbreviations), such as "Oregon" or "New South Wales".
* start_date (text): A string in an ISO format of the start date.
    Example: "2021-08-27T00:21:03+00:00".
* end_date (text): A string in an ISO format of the end date.
    Example: "2021-08-27T00:21:03+00:00".

measures: each row represents an attempted task by a certain team
* id (int) PK: The id of the task.
* phase (text): The phase the task is attempted in. Examples: "AUTO", "TELEOP",
    and "END".
* measure_name (text): The name of the task. Examples: "Outer Goal", "Inner Goal",
    "Lower Goal".
* measure_time (text): A string in an ISO format when the certain task occurs.
    Example: "2021-08-27T00:21:03+00:00".
* match_id (int) FK: The id of the match in which the task occurred.
* team_number (int) FK: The number of the team that attempted the task.
########## NEW WAY ##########
* result (int): A number either 0 or 1, where 0 is a failed attempt and 1 is
    a successful attempt.
* score (int): The amount of points the task gives on completion
    regardless if the task is completed successfully.
* category (text): Categorical type of the task. Examples: "LEFT",
    "RIGHT", "CENTER", "LEVEL1", "LEVEL2", and "LEVEL3".
########## OLD WAY ##########
* attempts (int): The number of attempts made to complete the task.
    Counts both successes and failures.
* successes (int): The number of times the task was completed successfully.
    Successes will always be equal to or less than to attempts.

matches: each row represents a specific match.
* id (int) PK: The id of the specific match.
* level (text): The type of the match. Examples: "q", "qf", "sf", and "f".
* match_label (text): A string representing the match number retrieved from
    TheBlueAlliance's API. Examples: "1m1", "2m1", and "3m2".
* match_number (int): An integer in the same order the matches occur.
    THIS IS A PROPOSAL
    Qualifications: 1-1000
    Quarterfinals: 2000s
    Semifinals: 3000s
    Finals: 4000s
* alliance (text): Red or Blue
* station (int): 1, 2, or 3
* event_id (int) FK: The id of the event in which the match occurred taken
    from the events table.
* team_number (int) FK: The number of the team. Examples: 1318, 2976, 488.
* official (int): 1 (true) and 0 (false). True if the match counts towards official score.
    For example, if a match is replayed due to an error the original match will have
    a value of 0 and the replayed match will have a value of 1.
"""
import sqlite3
import pandas as pd

import server.config as config

# def get_con(dbfile=None): #TODO: instance in test_database.py is commented
#     """
#     Creates and returns a new connection to the SQLite database.

#     This function is used to establish a connection with the SQLite database.
#     The 'check_same_thread' parameter is set to False for compatibility with Flask's threading model.

#     Returns:
#         sqlite3.Connection: A connection object to the SQLite database.
#     """
#     if dbfile is None:
#         dbpath = config.get_db_path()
#     else:
#         repo_path = pathlib.Path(__file__).parents[2] 
#         dbpath = repo_path.joinpath(config.get_data_path(), dbfile)
#     print(dbpath)
#     con = sqlite3.connect(dbpath, check_same_thread=False)
#     con.row_factory = sqlite3.Row
#     return con
#     #sqlite3 requires the check_same_thread parameter to be set to false to run effectively with flask


# def connect(_func): #TODO: no test
#     """
#     Decorator function for managing database connections.

#     Args:
#         _func (function): The function to be wrapped by the decorator.

#     Returns:
#         function: The wrapped function with database connection management.
#     """
#     def conn_wrapper(*args, con=None, **kwargs): #TODO: no test
#         if con is None: 
#             curcon = get_con()
#         else:
#             curcon = con
#         kwargs["con"] = curcon
#         result = _func(*args, **kwargs)
#         if con is None:
#             curcon.close()
#         return result
#     return conn_wrapper


def get_con():
    """
    Creates and returns a new connection to the SQLite database.

    This function is used to establish a connection with the SQLite database.
    The 'check_same_thread' parameter is set to False for compatibility with Flask's threading model.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.
    """
    # sqlite3 requires the check_same_thread parameter to be set to false to run effectively with Flask
    return sqlite3.connect(config.get_db_path(), check_same_thread=False)

def connect(_func):
    """
    Decorator function for managing database connections.

    This decorator is used to wrap functions that interact with the database.
    It ensures that each function has a database connection, either by using an existing one
    or by creating a new connection. It also handles the closing of the connection if it was created by the decorator.

    Args:
        _func (function): The function to be wrapped by the decorator.

    Returns:
        function: The wrapped function with database connection management.
    """
    def con_wrapper(*args, con=None, **kwargs):
        """
        Wrapper function for database connections.

        Checks if a database connection is provided; if not, creates a new one.
        Passes the connection to the wrapped function and ensures it's closed if created here.

        Args:
            *args: Variable length argument list for the wrapped function.
            con (sqlite3.Connection, optional): An existing database connection.
            **kwargs: Arbitrary keyword arguments for the wrapped function.

        Returns:
            The result of the wrapped function call.
        """
        # Create a new connection if not provided
        if con is None: 
            curcon = get_con()
        else:
            curcon = con
        kwargs["con"] = curcon

        # Execute the wrapped function
        result = _func(*args, **kwargs)

        # Close the connection if it was created here
        if con is None:
            curcon.close()
        return result
    return con_wrapper


@connect
def create_db(con=None):
    
    """Creates a simple database with the main tables.

    Creates or connects to a database to create the main tables that will
    be used.

    Args:
        db_name: The name of the database file to be created or connected to.
    """

    cur = con.cursor()

    teams = """
    CREATE TABLE Teams (
        team_number int PRIMARY KEY,
        team_name text,
        city text,
        state text,
        country text
    );
    """
    cur.execute(teams)

    measures = """
    CREATE TABLE Measures (
        match text,
        team_number text,
        phase text,
        task text,
        measure1 text,
        measure2 text,
        measure_type text,
        PRIMARY KEY (match, team_number, phase, task)

    );
    """
    cur.execute(measures)

    matches = """
    CREATE TABLE Matches (
        match text,
        match_time text,
        alliance text,
        station int,
        team_number text,
        PRIMARY KEY (match, alliance, station)
    );
    """
    cur.execute(matches)

    status = """
    CREATE TABLE Status (
        key text PRIMARY KEY,
        value text
    );
    """
    cur.execute(status)

    set_status("match", "qm1")
    set_status("event", None)

    con.commit()
    cur.close()

@connect
def add_teams(teams, con=None):
    """Insert and Update data into the TEAMS table

    Using TheBlueAlliance API to retrieve team data of a particular event,
    and then insert the new values into the TEAMS table or if the certain
    row already exists, update the the columns to the latest data

    Args:
        db_name: The name of the database where the TEAMS table should
            be updated.
        event_key: The key of the event so the team data can be retrieved
            using TheBlueAlliance API. Examples: "2020wasno", "2019pncmp", 
            and "2019wayak".

    Raises:
        HTTPError: An error occurrs while trying to retrieve data from 
            TheBlueAlliance API. Either invalid arguments were provided or 
            the system was unable to establish a connection.
        sqlite3.Error: An error occurrs while trying to insert or update
            the data. The database does not exist, the TEAMS table does not
            exist, or the values were unable to be added.
    """
    
    delete_query = "DELETE FROM Teams;"

    con.execute(delete_query)

    teams_sql = """
    INSERT INTO Teams (team_number, team_name, city, state, country)
        VALUES (:team_number, :team_name, :city, :state, :country)
        ON CONFLICT(team_number) DO UPDATE SET
            team_name=excluded.team_name,
            city=excluded.city,
            state=excluded.state,
            country=excluded.country;
    """
    con.executemany(teams_sql, teams)
    con.commit()

    count_query = "SELECT COUNT(*) FROM Teams;"

    num_teams = con.execute(count_query).fetchone()[0]
    return num_teams

@connect
def insert_measure(match, team_number, phase, task, measure1, measure2, measure_type, con=None):
    #each of the elements in this list is sent to the Flask server
    measures_data = [match, team_number, phase, task, measure1, measure2, measure_type]
    measures_sql = """
    INSERT INTO Measures
    (match, team_number, phase, task, measure1, measure2, measure_type)
    VALUES (?,?,?,?,?,?,?)
    ON CONFLICT(match, team_number, phase, task) DO UPDATE SET
    measure1 = excluded.measure1,
    measure2 = excluded.measure2;"""

    con.execute(measures_sql, measures_data)
    con.commit()

@connect
def set_status(key, value, con=None):
    
    cur = con.cursor()
    
    statuslist = [key, value]

    insert_sql = """
    INSERT INTO Status(key, value)
        VALUES (?,?)
        ON CONFLICT(key) DO UPDATE SET
        value=excluded.value;
    """
    cur.execute(insert_sql, statuslist)

    con.commit()
    cur.close()

@connect
def insert_into_matches(matches, con=None):
    """Inserts schedule into Matches table
       and returns the number of rows inserted

    Args:
        matches: list of dictionaries containing schedule
        [{'match': 'f1m1', 'station': 1, 'team': 'frc2930',
        'alliance': 'blue', 'match_time': '2020-03-01 23:20:22'}]
    """

    delete_query = "DELETE FROM Matches;"
    con.execute(delete_query)

    insert_matches = """ INSERT INTO Matches (match, match_time,  alliance, station, team_number)
                         values(:match, :match_time, :alliance, :station, :team_number);"""
    con.executemany(insert_matches, matches)
    con.commit()

    count_query = "SELECT COUNT(*) FROM Matches;"
    num_matches = con.execute(count_query).fetchone()[0]
    return num_matches
    

@connect
def get_status(key, con=None): #TODO: no test
    cur = con.cursor()

    status_query = """
    SELECT value FROM Status WHERE key = ?;
    """
    
    cur.execute(status_query, (key,))
    return cur.fetchone()[0]

@connect
def get_dataframes(con=None):
    measures = pd.read_sql("SELECT * FROM Measures;", con)
    matches = pd.read_sql("SELECT * FROM Matches;", con)
    status = pd.read_sql("SELECT * FROM Status;", con)
    teams = pd.read_sql("SELECT * FROM Teams;", con)
    df_dict = {"measures": measures, "matches": matches, "status": status, "teams": teams}
    return df_dict

@connect
def get_measure(match, phase, team_number, task, measurenum, con = None):
    cur=con.cursor()
    query = f"""SELECT {measurenum} FROM Measures WHERE match = ?
                AND phase = ? AND team_number = ?
                AND task = ?;"""
    cur.execute(query, (match, phase, team_number, task))
    return cur.fetchone()[0]