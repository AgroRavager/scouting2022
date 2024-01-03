import server.database as database
import sqlite3
import pandas as pd

def get_current_match():
    """ Retrieves the current match status from the database. """
    return database.get_status("match")

def set_current_match(match):
    """ Sets the current match status in the database. 
    Args:
        match (str): The match identifier to be set as current.
    """
    database.set_status(key="match", value=match)

def get_next_match():
    """ Calculates and returns the identifier of the next match. """
    cur_match = get_current_match()
    match_num = int(cur_match[2:])
    next_match_num = match_num + 1
    return "qm" + str(next_match_num)

def get_current_event():
    """ Retrieves the current event status from the database. """
    return database.get_status("event")

def set_current_event(event):
    """ Sets the current event status in the database.
    Args:
        event (str): The event identifier to be set as current.
    """
    database.set_status(key="event", value=event)

@database.connect
def get_matches(con=None):
    """ Retrieves all match records from the database.
    Args:
        con (sqlite3.Connection, optional): Database connection object.
    Returns:
        list: A list of tuples representing match records.
    """
    cur = con.cursor()
    query = "SELECT * FROM Matches ORDER BY match_time;"
    cur.execute(query)
    results = cur.fetchall()
    return results

@database.connect
def get_teams(db_name, con=None):
    """ Retrieves all team records from the database.
    Args:
        db_name (str): The name of the database (currently unused).
        con (sqlite3.Connection, optional): Database connection object.
    Returns:
        list: A list of tuples representing team records.
    """
    cur = con.cursor()
    query = "SELECT * FROM Teams;"
    cur.execute(query)
    results = cur.fetchall()
    return results

@database.connect
def get_team(match, alliance, station, con=None, ind=0):
    """ Retrieves a specific team based on match, alliance, and station.
    Args:
        match (str): The match identifier.
        alliance (str): The alliance identifier.
        station (int): The station number.
        con (sqlite3.Connection, optional): Database connection object.
        ind (int, optional): Index to select specific column from the result.
    Returns:
        tuple: A tuple representing the team record.
    """
    cur = con.cursor()
    query = """
    SELECT Matches.team_number, Teams.team_name FROM Matches LEFT JOIN Teams
    ON Matches.team_number = Teams.team_number
    WHERE Matches.match = ?
    AND Matches.station = ?
    AND Matches.alliance = ?;
    """
    cur.execute(query, (match, station, alliance))
    team = cur.fetchone()
    return team[ind]

@database.connect
def get_measures(match, team_number=None, alliance=None, station=None, con=None):
    """ Gets measures for a specific match and optionally a specific team.
    Args:
        match (str): The match identifier.
        team_number (str, optional): The team number. If not provided, derived from alliance and station.
        alliance (str, optional): The alliance identifier.
        station (int, optional): The station number.
        con (sqlite3.Connection, optional): Database connection object.
    Returns:
        list: A list of dictionaries representing measure records.
    """
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    query = """
    SELECT * FROM Measures
    WHERE match = ?
    AND team_number = ?
    ORDER BY task, phase;
    """
    if team_number is None and alliance is not None and station is not None:
        team_number = get_team(match, alliance, station, con)
    cur.execute(query, (match, team_number))
    rows = cur.fetchall()
    measures = [dict(row) for row in rows]
    con.row_factory = None
    return measures

@database.connect
def get_all_measures(con=None):
    """ Fetches all measure records from the Measures table in the database.
    Args:
        con (sqlite3.Connection, optional): Database connection object.
    Returns:
        list: A list of dictionaries representing all measure records.
    """
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    query = "SELECT * FROM Measures;"
    cur.execute(query)
    rows = cur.fetchall()
    measures = [dict(row) for row in rows]
    con.row_factory = None
    return measures

@database.connect
def export_matches(csv_file, con=None):
    """ Exports match data to a CSV file.
    Args:
        csv_file (str): The file path to export the data.
        con (sqlite3.Connection, optional): Database connection object.
    """
    matches_df = pd.read_sql("SELECT * FROM Matches;", con)
    matches_df.to_csv(csv_file, index=False)

@database.connect
def import_matches(csv_file, con=None):
    """ Imports match data from a CSV file.
    Args:
        csv_file (str): The file path from which to import the data.
        con (sqlite3.Connection, optional): Database connection object.
    """
    matches_df = pd.read_csv(csv_file)
    matches_df.to_sql("Matches", con, if_exists="append", index=False)

@database.connect
def export_measures(csv_file, con=None):
    """ Exports measure data to a CSV file.
    Args:
        csv_file (str): The file path to export the data.
        con (sqlite3.Connection, optional): Database connection object.
    """
    measures_df = pd.read_sql("SELECT * FROM Measures;", con)
    measures_df.to_csv(csv_file, index=False)

@database.connect
def import_measures(csv_file, con=None):
    """ Imports measure data from a CSV file.
    Args:
        csv_file (str): The file path from which to import the data.
        con (sqlite3.Connection, optional): Database connection object.
    """
    measures_df = pd.read_csv(csv_file)
    measures_df.to_sql("Measures", con, if_exists="replace", index=False)
