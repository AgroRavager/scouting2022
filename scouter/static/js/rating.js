(function() {

    stars = document.querySelectorAll(".stars");
    let n = 0;

    for (let star of stars) {
        star.addEventListener("click", updateStars);
        star.value = n;
    }

    function updateStars(evt){
        const starArray = ["☆☆☆", "★☆☆", "★★☆", "★★★"];

        let phase, task;
        const starData = evt.currentTarget.id.split(";");
        phase = starData[0];
        task = starData[1];
        match = document.getElementById("current-match").innerHTML
        team_number = document.getElementById("team").innerHTML

        n = parseInt(evt.currentTarget.value);

        if (n<3){
            n = n+1;
        } else {
            n = 0;
        }
        evt.currentTarget.innerHTML = starArray[n];
        evt.currentTarget.value = n;

        sendMeasure(match, team_number, phase, task, n, "3", "rating");
    };
    
})();