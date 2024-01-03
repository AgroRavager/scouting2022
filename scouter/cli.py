import argparse
import server.tba as tba
import pandas as pd
import pathlib
import server.config as config
import server.database as database
import server.event as event

def match(args):
    """
    Handles match-related commands.

    If 'set' argument is provided, it sets the current match.
    If 'import_csv' is provided, it imports matches from a CSV file.
    If 'export_csv' is provided, it exports matches to a CSV file.
    """
    # Set the current match
    if args.set is not None:
        event.set_current_match(args.set)
        print(f"Set the current match to {args.set}")
    
    # Import matches from CSV
    if args.import_csv is not None:
        path = pathlib.Path(__file__).absolute().parent.joinpath(args.import_csv)
        event.import_matches(path)
        print(f"Matches have been imported from {args.import_csv}")
    
    # Export matches to CSV
    elif args.export_csv is not None:
        path = pathlib.Path(__file__).absolute().parent.joinpath(args.export_csv)
        event.export_matches(path)
        print(f"Matches have been exported to {args.export_csv}")

def schedule(args):
    """
    Manages event schedules.

    Downloads schedules from TBA and optionally views or sets them.
    """
    if hasattr(args, "tba"):
        schedule = tba.get_matches(args.tba)
        # View schedule
        if args.view:  
            print(pd.DataFrame(schedule))  
        # Set schedule in the database
        elif args.set:
            event.set_current_event(args.tba)
            num_rows = database.insert_into_matches(schedule)
            print(f"Successfully inserted {num_rows} records into Matches table")

def create(args):
    """
    Creates a new database file.

    If 'file' argument is provided, creates a new database with the given filename.
    """
    if args.file is not None:
        config.set_db_filename(args.file)
        database.create_db()
        print("Created new db file:", config.get_db_filename())

def teams(args):
    """
    Handles team-related operations.

    Downloads team information from TBA and optionally views or updates them in the database.
    """
    if hasattr(args, "tba"):
        teams = tba.get_teams(args.tba)
        # View teams
        if args.view:  
            print(pd.DataFrame(teams))  
        # Update teams in the database
        elif args.set:
            num_rows = database.add_teams(teams)
            print(f"Successfully inserted {num_rows} records into Teams table")

if __name__ == "__main__":
    # CLI setup using argparse
    parser = argparse.ArgumentParser(
        prog="irs",
        description="sets up the IRS scouting system")
    subparsers = parser.add_subparsers(title="sub commands for system")

    # Match command parser setup
    match_parser = subparsers.add_parser("match", help="Get or Set the current match")
    match_group = match_parser.add_mutually_exclusive_group()
    match_parser.add_argument("-s","--set", help="Set the current match")
    match_group.add_argument("-i", "--import_csv", help="Import schedule from CSV file")
    match_group.add_argument("-e", "--export_csv", help="Export schedule to CSV file")
    match_parser.set_defaults(func=match)

    # Schedule command parser setup
    schedule_parser = subparsers.add_parser("schedule", help="Manages event schedule")
    schedule_parser.add_argument("--tba", help="Download schedules from The Blue Alliance")
    schedule_parser.add_argument("--view", action="store_true", help="View schedule")
    schedule_parser.add_argument("--set", action="store_true", help="Set schedule")
    schedule_parser.set_defaults(func=schedule)

    # Database creation command parser setup
    create_parser = subparsers.add_parser("create", help="Creates database")
    create_parser.add_argument("--file", help="Creates database with the file name")
    create_parser.set_defaults(func=create)

    # Teams command parser setup
    teams_parser = subparsers.add_parser("teams", help="Updates teams in the database")
    teams_parser.add_argument("--tba", help="Downloads teams from The Blue Alliance")
    teams_parser.add_argument("--view", action="store_true", help="View teams")
    teams_parser.add_argument("--set", action="store_true", help="Set teams")
    teams_parser.set_defaults(func=teams)

    args = parser.parse_args()

    # Execute the appropriate function based on the provided arguments
    if hasattr(args, "func"):
        args.func(args)
