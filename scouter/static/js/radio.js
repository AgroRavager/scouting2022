(function() {
    const all_radio = document.querySelectorAll(".radio");

    for (let radio of all_radio) {
        radio.addEventListener("change", function(evt){
            let phase, task;
            const radioData = evt.currentTarget.id.split(";");
            phase = radioData[0];
            task = radioData[1];
            match = document.getElementById("current-match").innerHTML;
            team_number = document.getElementById("team").innerHTML;

            sendMeasure(match, team_number, phase, task, radio.getAttribute('value'), "-1", "categorical");
        });
    }
})();