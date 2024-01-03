if (document.querySelector("#current-match")){
    station = document.querySelector(".station");
    station_id = station.id.split("-");
    alliance = station_id[0];
    station_number = station_id[1];
}

/** Resets values on UI. Gets the current match, team number, and team name. */
function reset(){
    if (document.querySelector("#team")){
        updateReset();
        getMatch();
        getTeam();
        getTeamName();
    }
}

reset();


/* SOCKETIO
auth (station) is the variable sent to main.py when there is a socketio connection. */
if (document.querySelector(".station")) {
    socket = io({
        auth: document.querySelector(".station").innerHTML
    });
} else {
    socket = io({
        auth: "server"
    })
}

/* Defines connectstation (current station) to be used in following functions */
if (document.querySelector(".station")) {
    connectstation = document.querySelector(".station").innerHTML;
}

/* Allows a socketio connection and runs when there is a connection. */
socket.on("connect", function() {
    console.log("connected");
    if (document.querySelector(".station")){
        /* Emits to main.py in order to display connections on command.html. auth (defined above) is sent as the station, which is added to a list. The list is then displayed on command.html. */
        socket.emit("displayConnect");
    }
    if (document.querySelector(".tabletfinish")) {
        socket.emit("notifyFinish");
    }
});

/* Socketio connection may fail if there is already a connection to the station. Even if there is no socketio connection, we still want to notify command.html, so it emits the same as "connect". */
socket.on("connect_error", () => {
    console.log("CONNECTION ERROR!!!")
    /* same as "connect" */
    if (document.querySelector(".station")){
        socket.emit("displayConnect");
    }
});

/** If a station loses connection (leaves or refreshes page), functions in main.py and command.js clear the array of current connections and replaces it with the stations of all connected stations. */
socket.on("ondisconnect", function () {
    if (socket.connected) {
        if (document.querySelector(".station")){
            socket.emit("disconarray", " "+connectstation)
        }
    }
    socket.emit("displayConnect");
})

/* manual refresh button */
if (document.querySelector("#reset")){
    document.querySelector("#reset").addEventListener("click", function() {
        socket.emit("refresh")
        console.log("clicked")
    })
}

/* FINISH
When all 6 tablets finish, (1) resets values on the UI (2) fetches & updates match, team number, and team name.

Refresh sends an emit to the server, which emits back to here (socket.on("chat")), where all 6 tablets run the reset() function.

socket.on("notifyFinish") - displays to command.html how many tablets are finished entering data */

socket.on("reset", function() {
    reset();
});

socket.on("notifyFinish", (station) => {
    station = station.split(" ")
    station = station[0] + "-" + station[1];
    if (document.querySelector(`.tabletfinish.${station}`)) {
        document.querySelector(`.tabletfinish.${station}`).classList.add("ready");
    }
    if (document.querySelector(".finishtext")) {
        document.querySelector(".finishtext").innerHTML = "ready for next match"
    }
});

socket.on("resetFinish", (station) => {
    station = station.split(" ")
    station = station[0] + "-" + station[1];
    if (document.querySelector(`.tabletfinish.${station}`)) {
        document.querySelector(`.tabletfinish.${station}`).classList.remove("ready");
    }
    if (document.querySelector(".finishtext")) {
        document.querySelector(".finishtext").innerHTML = "waiting for finish . . ."
    }
})


// CONNECTION NOTIFICATION
socket.on("changeConnect", (new_socket_stations) => {
    if (document.querySelector("#blue_connect")) {

        document.querySelector("#red_connect").innerHTML = " "
        document.querySelector("#blue_connect").innerHTML = " "
        
        for (let connection of new_socket_stations) {
            if (connection.includes("red")) {
                document.querySelector("#red_connect").append(connection+", ");
            } else if (connection.includes("blue")) {
                document.querySelector("#blue_connect").append(connection+", ");
            } else {
                document.querySelector("#other_connect").append(connection+", ");
            }
        }

    }
});