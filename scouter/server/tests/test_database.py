# Import necessary modules
import os
import sqlite3

# Pandas for data manipulation, pytest for testing
import pandas as pd
import pytest

# Importing specific modules from the server package
import server.database as database
import server.tba as tba
import server.event as event
import server.config as config

def test_tables_exist(test_db_con):
    """
    Test to verify that the necessary tables exist in the database.

    Args:
    test_db_con: SQLite3 connection object to the test database.

    This function queries the database to check the existence of certain
    tables and asserts their presence.
    """
    test_query = "SELECT * FROM sqlite_master WHERE type ='table';"
    table_df = pd.read_sql(test_query, test_db_con)
    tables = set(table_df.tbl_name)
    assert "Measures" in tables
    assert "Matches" in tables
    assert "Status" in tables
    assert "Teams" in tables

def test_curmatch(set_test_db):
    """
    Test to verify setting and retrieving the current match.

    Args:
    set_test_db: Fixture to set up the test database.

    This function checks the functionality of setting and retrieving
    the current match in the event module.
    """
    curr_match = event.get_current_match()
    event.set_current_match("qm10")
    assert event.get_current_match() == "qm10"
    event.set_current_match("qm99")
    assert event.get_current_match() == "qm99"
    event.set_current_match(curr_match)

def test_matches_entry(test_db_con):
    """
    Test to verify the entry of match data into the database.

    Args:
    test_db_con: SQLite3 connection object to the test database.

    This function retrieves match data, inserts it into the database,
    and then queries the database to check the correctness of the inserted data.
    It also cleans up the Matches table after the test.
    """
    wasno_matches = tba.get_matches("2020wasno")
    database.insert_into_matches(wasno_matches)
    matches_query = "SELECT * FROM Matches;"
    matches = pd.read_sql(matches_query, test_db_con)
    assert matches.shape == (534, 5)
    pdqry = "match == 'f1m1' and alliance == 'blue' and station == 1"
    assert matches.query(pdqry).iloc[0, 4] == "frc2930"
    qry = "DELETE FROM Matches;"
    test_db_con.execute(qry)
    test_db_con.commit()

def test_initial_status(set_test_db):
    """
    Test to verify the initial status of the event.

    Args:
    set_test_db: Fixture to set up the test database.

    This function checks the initial status of the current match and event,
    expecting the first match and no current event.
    """
    assert event.get_current_match() == "qm1"
    assert event.get_current_event() == None

def test_teams_entry(test_db_con):
    """
    Test to verify the entry of team data into the database.

    Args:
    test_db_con: SQLite3 connection object to the test database.

    This function retrieves team data, adds it to the database,
    and then queries the database to check the correctness of the inserted data.
    """
    database.add_teams(tba.get_teams("2020wasno"))
    teams_df = pd.read_sql("SELECT * FROM Teams", test_db_con)
    assert "frc1318" in set(teams_df.team_number)
    assert "Issaquah Robotics Society" in set(teams_df.team_name)
    assert teams_df.shape[0] == 37
    assert teams_df.shape[1] == 5

def test_pickle(test_db_con):
    """
    Test to verify the functionality of getting dataframes.

    Args:
    test_db_con: SQLite3 connection object to the test database.

    This function tests the retrieval of dataframes from the database
    and checks the shape of the 'measures' dataframe.
    """
    df_dict = database.get_dataframes()
    assert df_dict["measures"].shape == (0,7)
