# Import the pytest module for writing test cases
import pytest

# Import the tba module from the server package
import server.tba as tba

def test_get_events():
    """
    Test to verify the retrieval of events from the server.

    This test fetches events for a specific region and year (2020pnw) using the tba module.
    It then checks:
    - The number of events retrieved is as expected (10).
    - Essential keys ('key', 'event_code', 'name') are present in the event data.
    """
    events = tba.get_events("2020pnw")
    assert len(events) == 10
    event_keys = events[0].keys()
    assert "key" in event_keys
    assert "event_code" in event_keys
    assert "name" in event_keys

def test_get_matches():
    """
    Test to verify the retrieval of match information from the server.

    This test fetches match data for a specific event (2020wasno) using the tba module.
    It checks:
    - The number of matches retrieved is as expected (534).
    - The first match's data contains the expected values and structure.
    """
    matches = tba.get_matches("2020wasno")
    assert len(matches) == 534
    print(matches[0])
    assert matches[0]["match"] == "qm1"
    assert len(matches[0].keys()) == 5
    assert matches[0]["match_time"] == "2020-02-29 19:06:04"
    assert isinstance(matches[0]["station"], int)
