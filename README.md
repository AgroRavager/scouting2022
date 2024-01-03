# IRS Scouting 2022
A database-driven scouting system for the 2022 FRC competition season.
This application is being developed by the Issaquah Robotics Society (IRS).

## Features
* A client-server application. The server is written in Python and
uses the CherryPy HTTP server. The client uses the Angular framework and
is written in Typescript, HTML, and CSS.
* Data is stored in a Sqlite database
* Analysis and visualization is conducted in Python, using the Pandas
and Bokeh packages.

## Branch Management
Branch names will reflect the work that is being done within the branch.
Branches *will not* be named after the person who creates the branch.

### Active Branches as of 6 Sep 2021
* `dbdev`: Development of functions that interact with the Sqlite
database, mostly in `database.py`.
* `test`: For writing unit tests in pytest.
* `mentor_feedback`: This branch will contain comments and feedback from
IRS mentors. Students will not work on the `mentor-feedback` branch, and
as of 6 Sep 2021, mentors will not contribute code to any branches other
than `mentor_feedback`.