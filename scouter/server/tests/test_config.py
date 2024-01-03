# Importing the pytest module for writing test cases
import pytest

# Importing the config module from the server package
import server.config as config

def test_data_path():
    """
    Test to verify the functionality of getting and setting the data path in the configuration.

    This test first retrieves the current data path from the configuration,
    then changes it to a new value and checks if the change was successful.
    Finally, it resets the data path to its original value and verifies this reset.
    """
    # Storing the current data path to restore it later
    current_data_path = config.get_data_path()

    # Changing the data path to a new value and asserting the change
    config.set_data_path("Hello World")
    assert config.get_data_path() == "Hello World"

    # Resetting the data path to its original value and asserting the reset
    config.set_data_path(current_data_path)
    assert config.get_data_path() == current_data_path
