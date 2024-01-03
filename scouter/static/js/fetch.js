/* Global fetch functions used in other js files. */

function sendMeasure(match, team_number, phase, measure_name, measure1, measure2, measure_type) {
    /* The current match must include qm and the team must include frc.
    This ensures that data is being entered into a valid match/team, and issues like TypeErrors will not show up in the database or graphs. */
    if (document.getElementById("current-match").innerHTML.includes("qm") == true && document.getElementById("team").innerHTML.includes("frc") == true) {
        fetch(`/set-measure/${match}/${team_number}/${phase}/${measure_name}/${measure1}/${measure2}/${measure_type}`).then(function(response) {
            return response.text();
        }).then(function(text) {
            document.querySelector("#test").innerHTML = text;
        }).catch(function(err) {
            document.querySelector("#test").innerHTML = err;
        });
    } else {
        alert("ERROR. CHECK WITH SCOUTING TECHNICIAN.")
    }
};

/* The following 3 functions fetch the current match, team, and team name to display on the UI and use when sending measures. */
function getMatch() {
    fetch(`/currentmatch`).then(function(response) {
        return response.text();
    }).then(function(text) {
        document.querySelector("#current-match").innerHTML = text;
    }).catch(function(err) {
        document.querySelector("#current-match").innerHTML = err;
    });
};

function getTeam() {
    fetch(`/team/${alliance}/${station_number}`).then(function(response) {
        return response.text();
    }).then(function(text) {
        document.querySelector("#team").innerHTML = text;
    }).catch(function(err) {
        document.querySelector("#team").innerHTML = err;
    });
};

function getTeamName() {
    fetch(`/teamname/${alliance}/${station_number}`).then(function(response) {
        return response.text();
    }).then(function(text) {
        document.querySelector("#teamname").innerHTML = text;
    }).catch(function(err) {
        document.querySelector("#teamname").innerHTML = err;
    });
};


/* updateReset clears all values on the UI, setting them to default.
Selects each of the 4 types of data and sets them to their default values. */
function updateReset() {
    allSpinners = document.querySelectorAll("input.spinner");        
    for (let spinner of allSpinners) {
        spinner.value = 0;
    }

    allRadio = document.querySelectorAll("input.radio");
    for (let radio of allRadio) {
        radio.checked = radio;
    }

    allBool = document.querySelectorAll("input.checkbox");
    for (let bool of allBool) {
        bool.checked = false;
    }

    allRating = document.querySelectorAll("div.stars")
    for (let rating of allRating) {
        rating.innerHTML = "☆☆☆";
    }
};


/* Manually setting the match in command.html. */
function setMatch(match){
    fetch(`/command/match/${match}`).then(function(response) {
        return response.text();
    }).then(function(text) {
        document.querySelector("#currentmatch").innerHTML = text;
    }).catch(function(err) {
        document.querySelector("#currentmatch").innerHTML = err;
    });
};