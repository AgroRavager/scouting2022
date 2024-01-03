(function (){
    // SETTING NEXT MATCH
    function settingnextm (){
        socket.on("setNextMatch", () => {

            function nextMatch(){
                fetch(`/nextmatch`).then(function(response) {
                    return response.text();
                }).then(setMatch) 
                .catch(function(err) {
                    document.querySelector("#currentmatch").innerHTML = err;
                });
            };
           
            nextMatch();

            socket.emit("refresh");
        })
    }

    
    function createMatchTable(matchData){

        // CREATING MATCH BUTTONS
        matches = JSON.parse(matchData);
    
        let table = document.createElement("table");

        for (let match of matches){
            if (match[2] == "blue" && match[3] == 1){
                row = table.insertRow();
                cellA = row.insertCell();
                cellA.classList.add("button", "cell");
                cellA.innerHTML = match[0];

                cellB = row.insertCell();
                cellB.className = "cell";
                cellB.innerHTML = match[1];
            }

            if (match[2] == "blue"){
                cellC = row.insertCell();
                cellC.className = "cell";
                cellC.innerHTML = match[4];
                if (match[4] == "frc1318"){
                    cellC.classList.add("highlightcell");
                }
            }

            if (match[2] == "red"){
                cellD = row.insertCell();
                cellD.className = "cell";
                cellD.innerHTML = match[4];
                if (match[4] == "frc1318"){
                    cellD.classList.add("highlightcell");
                }
            }
        }

        document.querySelector("#matches").appendChild(table);

        const select = document.getElementsByClassName("button");

        for (let selection of select){
            selection.addEventListener("click", function(evt){
                match = evt.currentTarget.innerHTML;
                setMatch(match);
                socket.emit("refresh");
            });
        };
    }


    /* Creates the table displayed in command.html containing the matches and teams. */
    function getMatch(){
        fetch(`/matches`).then(function(response) {
            return response.text();
        }).then(createMatchTable)
        // initial getnextmatch load
        .then(settingnextm)
        .catch(function(err) {
            document.querySelector("#currentmatch").innerHTML = err;
        });
    };
    getMatch();

})();