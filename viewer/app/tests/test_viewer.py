import pytest
import sqlite3
import main

def test_con():
    measures, matches, status, teams = main.get_data()
    print(measures, matches, status, teams)
    # assert isinstance(con, sqlite3.Connection)
    assert measures.shape == (1165, 7)
    assert matches.shape == (534, 5)
    assert status.shape == (2,2)
    assert teams.shape == (37,5)

def test_hub_plot():
    measures, _, _, _ = main.get_data() 
    print(main.plot_hub(measures))
    
