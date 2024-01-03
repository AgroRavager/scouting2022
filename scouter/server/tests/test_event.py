# Import required libraries and modules
import pytest
import pandas as pd
import os
import server.event as event
import server.database as database
import shutil
import pathlib

def test_current_match(set_test_db):
    """
    Test to verify setting and retrieving the current match.

    Args:
    set_test_db: Fixture to set up the test database.

    This function tests if the current match can be set and retrieved correctly.
    It changes the current match, checks the change, and then resets it.
    """
    cur_match = event.get_current_match()
    event.set_current_match("qm39")
    assert event.get_current_match() == "qm39"
    assert cur_match != event.get_current_match()
    event.set_current_match(cur_match)
    assert cur_match == event.get_current_match()

def test_current_event():
    """
    Test to verify setting and retrieving the current event.

    This function tests if the current event can be set and retrieved correctly.
    It changes the current event, checks the change, and then resets it.
    """
    cur_event = event.get_current_event()
    event.set_current_event("2020pnw")
    assert cur_event != event.get_current_event
    event.set_current_event(cur_event)
    assert cur_event == event.get_current_event()

def test_get_next_match():
    """
    Test to verify the functionality of getting the next match.

    This function tests if the next match is correctly calculated based on the current match.
    It checks the sequence of matches to ensure correct incrementation.
    """
    cur_match = event.get_current_match()
    next_match = event.get_next_match()
    
    cur_match_num = int(cur_match[2:])
    next_match_num = int(next_match[2:])    

    assert cur_match_num + 1 == next_match_num 

    cur_match_num = next_match_num

    next_match = event.get_next_match()

    next_match_num = int(next_match[2:])
    cur_match_num = int(cur_match[2:])

    assert cur_match_num + 1 == next_match_num

def get_matches(set_test_db):
    """
    Placeholder function to get matches.

    Args:
    set_test_db: Fixture to set up the test database.

    Currently, this function does not implement any testing logic.
    """
    matches = event.get_matches()

def test_team(set_test_db):
    """
    Placeholder function for testing team-related functionality.

    Args:
    set_test_db: Fixture to set up the test database.

    Currently, this function does not implement any testing logic.
    """
    assert True

def test_measures(set_test_db):
    """
    Test to verify the insertion and retrieval of measure data.

    Args:
    set_test_db: Fixture to set up the test database.

    This function tests inserting measure data into the database and retrieving it.
    It checks the length of the retrieved data and the type and content of the data.
    """
    database.insert_measure("qm4", "frc2522", "auto", "pickup-field", "6", "-1", "count")
    database.insert_measure("qm4", "frc2522", "auto", "start_pos", "center", "-1", "categorical")
    database.insert_measure("qm4", "frc2522", "teleop", "upper", "2", "1", "count")
    measures = event.get_measures("qm4", "frc2522")
    assert len(measures) == 3
    assert isinstance(measures[0], dict)
    assert measures[0].get("task") == "pickup-field"
    assert measures[1].get("measure_type") == "categorical"

    all_measures = event.get_all_measures()
    assert len(all_measures) == 3

    database.insert_measure("qm2", "frc4683", "teleop", "lower", "1", "1", "count")
    measures = event.get_measures("qm2", "frc4683")
    assert all_measures != measures

def test_csv(test_db_con):
    """
    Test to verify the import and export functionality for match data using CSV files.

    Args:
    test_db_con: SQLite3 connection object to the test database.

    This function tests copying a CSV file, importing match data from it,
    inserting additional data to the database, exporting the updated data back to a CSV,
    and then performing cleanup and validation of the data.
    """
    path1 = pathlib.Path(__file__).absolute().parent.joinpath("testmatches.csv")
    path2 = pathlib.Path(__file__).absolute().parents[2].joinpath("testmatches.csv")
    shutil.copyfile(path1, path2)
    event.import_matches(path2)
    query = """INSERT INTO Matches(match, match_time, alliance, station, team_number)
                VALUES (?,?,?,?,?);"""
    ins_list = [("qm2", "2020-02-28 19:06:04", "green", 3, "frc254"),
                ("qm3", "2020-02-28 19:06:04", "green", 3, "frc254")]
    test_db_con.executemany(query, ins_list)
    test_db_con.commit()
    event.export_matches(path2)
    matches_df = pd.read_csv(path2)
    os.remove(path2)
    delquery = "DELETE FROM Matches;"
    test_db_con.execute(delquery)
    test_db_con.commit()
    assert matches_df.shape == (7,5)
    assert matches_df.loc[5, "alliance"] == "green" and matches_df.loc[5, "team_number"] == "frc254"
    assert matches_df.loc[1, "alliance"] == "blue" and matches_df.loc[1, "team_number"] == "frc4089"
