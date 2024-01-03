import os
import pathlib
import sqlite3

import pandas as pd
import pytest

import server.database as database
import server.config as config

import pytest

TEST_DB = "pytest.sqlite3"

@pytest.fixture(scope="module")
def set_test_db():
    """Creates new, empty database for unit testing."""
    # Verify that test sqlite3 file does not exist
    repo_path = pathlib.Path(__file__).parents[3]
    db_path = repo_path.joinpath(config.get_data_path(), TEST_DB)
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Get the current database filename so system can be restored to
    #   original configuration after tests.
    current_db = config.get_db_filename()

    # Configure system to use empty test database
    config.set_db_filename(TEST_DB)
    database.create_db()

    # Send name of current database to unit tests that use this fixture
    yield config.get_db_filename()

    # Restore original database configuration and delete sqlite3 file.
    config.set_db_filename(current_db)
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture(scope="module")
def test_db_con(set_test_db):
    """Gets a database connection to new, empty database."""
    assert set_test_db == config.get_db_filename()
    con = sqlite3.connect(config.get_db_path())
    yield con
    con.close()


# @pytest.fixture(scope="module")
# def set_test_delete():
#     repo_path = pathlib.Path(__file__).parents[3]
#     db_path = repo_path.joinpath(config.get_data_path(), TEST_DB)
#     if os.path.exists(db_path):
#         os.remove(db_path)
    
#     current_db = config.get_db_filename()

#     config.delete_db_filename()

#     yield config.get_db_filename()

#     config.set_db_filename(current_db)
#     if os.path.exists(db_path):
#         os.remove(db_path)

# @pytest.fixture(scope="module")
# def test_db_con(set_test_delete):
#     assert set_test_delete == config.get_db_filename()
#     con = sqlite3.connect(config.get_db_path())
#     yield con
#     con.close()