// Self-invoking function to attach 'change' event listeners to checkboxes.
// When a checkbox state changes, it sends measure data based on the checkbox's id, 
// current match, and team number.
(function() {
    const checkbox = document.querySelectorAll("input.checkbox");

    for (let box of checkbox) {
        box.addEventListener("change", function(evt){
            const checkboxData = evt.currentTarget.id.split(";");
            const phase = checkboxData[0];
            const task = checkboxData[1];
            const match = document.getElementById("current-match").innerHTML;
            const team_number = document.getElementById("team").innerHTML;
            
            sendMeasure(match, team_number, phase, task, box.checked, "-1", "boolean");
        });
    }
})();
