import server.auth as auth
import urllib.request
import json
from datetime import datetime

def getheader():
    """ 
    Constructs the header for API requests to The Blue Alliance (TBA).

    Returns:
        dict: A dictionary containing the authentication key and user-agent for the API request.
    """
    return {"X-TBA-Auth-Key": auth.tba_key, "User-Agent": "frc1318scouting"}

def get(endurl):
    """
    Sends a GET request to a specified endpoint of the TBA API.

    Args:
        endurl (str): The specific endpoint of the TBA API to send the request to.

    Returns:
        str: The response text from the API request.
    """
    auth_hdr = getheader()
    url = f"https://www.thebluealliance.com/api/v3/{endurl}"
    req = urllib.request.Request(url, headers=auth_hdr)
    
    with urllib.request.urlopen(req) as resp:
        resp_text = resp.read()
    
    return resp_text

def get_districts(year):
    """
    Retrieves district information for a given year from the TBA API.

    Args:
        year (str): The competition year.

    Returns:
        list: A list of dictionaries, each containing information about a district.
    """
    districts_json = json.loads(get(f"districts/{str(year)}"))
    return districts_json

def get_events(district_key):
    """
    Retrieves event information for a given district key from the TBA API.

    Args:
        district_key (str): The key identifier for the district.

    Returns:
        list: A list of event data.
    """
    events_json = json.loads(get(f"district/{str(district_key)}/events"))
    return events_json

def get_my_events(team_key, year):
    """
    Retrieves event information for a specific team in a given year from the TBA API.

    Args:
        team_key (str): The key identifier for the team.
        year (str): The competition year.

    Returns:
        list: A list of events that the specified team is participating in.
    """
    return json.loads(get(f"team/{str(team_key)}/events/{str(year)}/simple"))

def get_events_year(year):
    """
    Retrieves all events for a given year from the TBA API.

    Args:
        year (str): The competition year.

    Returns:
        list: A list of all events for the specified year.
    """
    return json.loads(get(f"events/{str(year)}"))

def get_teams(event_key):
    """
    Retrieves team information for a given event from the TBA API.

    Args:
        event_key (str): The key identifier for the event.

    Returns:
        list: A list of dictionaries, each containing information about a team.
    """
    teams_json = json.loads(get(f"event/{str(event_key)}/teams/simple"))
    teams_dict = [{"team_number": "frc" + str(team["team_number"]), "team_name": team["nickname"], "city": team["city"], 
                   "state": team["state_prov"], "country": team["country"]} for team in teams_json]
    
    return teams_dict

def get_matches(event_key):
    """
    Retrieves match information for a given event from the TBA API.

    Args:
        event_key (str): The key identifier for the event.

    Returns:
        list: A list of dictionaries, each containing information about a match.
    """
    matches_json = json.loads(get(f"event/{str(event_key)}/matches/simple"))
    raw_match_key = matches_json[0]["key"]
    underscore = raw_match_key.find("_")
    
    matches_dict = [
        {"match": match["key"][underscore+1:], "station": idx+1, "team_number": team,
         "alliance": alliance, 
         "match_time": datetime.utcfromtimestamp(match["predicted_time"]).strftime("%Y-%m-%d %H:%M:%S")} 
        for match in matches_json
        for alliance in match["alliances"]
        for idx, team in enumerate(match["alliances"][alliance]["team_keys"])]

    matches_dict.sort(key=lambda match: match["match_time"])
    return matches_dict
