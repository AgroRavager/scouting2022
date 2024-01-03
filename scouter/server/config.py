"""
Module Description:
This module is the only file that accesses and modifies the values in 'config.json'.
It provides functions to get and set database paths and filenames, as well as to delete these configurations.
"""

import json
import pathlib

def _get_value(key):
    """
    Internal function to retrieve a value from the config.json file.

    Args:
    key (str): The key for which the value is to be retrieved from the config file.

    Returns:
    The value associated with the given key in the config file.
    """
    folder = pathlib.Path(__file__).parents[1]
    file_path = str(folder) + "/config.json"
    with open(file_path, "r") as cfile:
        config = json.load(cfile)
        return config.get(key)

def _set_value(key, value):
    """
    Internal function to set a value in the config.json file.

    Args:
    key (str): The key for which the value is to be set in the config file.
    value: The value to be set for the given key.
    """
    folder = pathlib.Path(__file__).parents[1]
    file_path = str(folder) + "/config.json"
    with open(file_path, "rt") as cfile:
        config = json.load(cfile)
    with open(file_path, "wt") as cfile:
        config[key] = value
        json.dump(config, cfile)

def _delete(key):
    """
    Internal function to delete a key-value pair from the config.json file.

    Args:
    key (str): The key to be deleted from the config file.

    Note:
    This function is marked with 'TODO' indicating a need for further implementation or consideration,
    especially regarding its usage in 'test_config.py' and 'test_database.py'.
    """
    folder = pathlib.Path(__file__).parents[1]
    file_path = str(folder) + "/config.json"
    with open(file_path, "rt") as cfile:
        config = json.load(cfile)
    with open(file_path, "wt") as cfile:
        del config[key]
        json.dump(config, cfile)

def get_db_filename():
    """
    Get the current database filename from the config file.

    Returns:
    The filename of the database as stored in the config file.
    """
    return _get_value("db_filename")

def get_db_path():
    """
    Construct and return the full path to the database file.

    Returns:
    The full path (directory and filename) to the database.
    """
    repo_path = pathlib.Path(__file__).parents[2] 
    return repo_path.joinpath(get_data_path(), get_db_filename())
    
def get_data_path():
    """
    Get the database directory path from the config file.

    Returns:
    The path to the directory where the database is stored.
    """
    return _get_value("data_path")

def set_db_filename(fname):
    """
    Set a new database filename in the config file.

    Args:
    fname (str): The new filename to be set for the database.

    Returns:
    The updated database filename after modification.
    """
    _set_value("db_filename", fname)
    return get_db_filename()

def set_data_path(dpath): 
    """
    Set a new path for the database in the config file.

    Args:
    dpath (str): The new path to be set for the database.

    Returns:
    The updated database path after modification.
    """
    _set_value("data_path", dpath)
    return get_data_path()

def delete_db_filename():
    """
    Delete the database filename from the config file.
    """
    _delete("db_filename")

def delete_data_path():
    """
    Delete the database path from the config file.
    """
    _delete("data_path")

