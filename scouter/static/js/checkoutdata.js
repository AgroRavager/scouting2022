(function() {
    // COMPARING UI & DATABASE MEASURES
    function compare(ui, db){
        let indexui = 0;
        let indexdb = 0;
        for(let i = 0; i < ui.length; i++){

            let match = document.getElementById("current-match").innerHTML;
            let phase = ui[indexui].phase;
            let measure1 = ui[indexui].measure1;
            let measure2 = ui[indexui].measure2;
            let measure_type = ui[indexui].measuretype;
            let task = ui[indexui].task;
            let team_number = document.getElementById("team").innerHTML;

            if (db == false){
                console.log("db is false")
                sendMeasure(match, team_number, phase, task, measure1, measure2, measure_type);
                indexui++;
            } else if (ui[indexui].phase == db[indexdb].phase && ui[indexui].task == db[indexdb].task) {
                if (ui[indexui].measure1 == db[indexdb].measure1){
                    if (ui[indexui].measure2 == db[indexdb].measure2){
                        indexui++;

                        nextindex = indexdb+1
                        if (db[nextindex] == true) {
                            indexdb++;
                        }

                        console.log("this does something");
                    } else {
                        sendMeasure(match, team_number, phase, task, measure1, measure2, measure_type);
                        indexui++;

                        nextindex = indexdb+1
                        if (db[nextindex] == true) {
                            indexdb++;
                        }

                        console.log("hi"  + task);
                    }
                } else {
                    sendMeasure(match, team_number, phase, task, measure1, measure2, measure_type);
                    indexui++;

                    nextindex = indexdb+1
                    if (db[nextindex] == true) {
                        indexdb++;
                    }

                    console.log("not the same" + task);
                }
            } else {
                indexui++;
                console.log("resend measures")
                sendMeasure(match, team_number, phase, task, measure1, measure2, measure_type);
            }
        };
    };

    counting = 0;

    // Clicking on the finish button
    checkdataBtn = document.querySelector("#checkdata");
    checkdataBtn.addEventListener("click", function(){
        match = document.getElementById("current-match").innerHTML;
        team_number = document.getElementById("team").innerHTML;

        counting++
        station = document.querySelector(".station").innerHTML;

        function finished() {
            socket.emit("finished", station);
            socket.emit("notifyFinish");
        }
        
        finished();

        checkoutData(match, team_number);
        check();
    });
    

    // testing button (click on pick up h3)
    click = document.querySelector("h3");
    click.addEventListener("click", check);
    

    function check() {
        // SELECTING VALUES FROM UI
        uiMeasures = [];

        all_spinners = document.querySelectorAll(".spinnerAll");
        all_radios = document.querySelectorAll(".radio");
        all_checkbox = document.querySelectorAll(".checkbox");
        all_stars = document.querySelectorAll(".stars");
    
        for (let spinner of all_spinners){
            spinner1 = spinner.querySelector(".spinner1");
            spinner2 = spinner.querySelector(".spinner2");

            measure = {
                "match": document.getElementById("current-match").innerHTML,
                "measure1": spinner.querySelector('input.spinner1').value,
                "measure2":  (spinner.querySelector('input.spinner2') == null) ? "-1" : spinner.querySelector('input.spinner2').value,
                "measuretype": "count",
                "phase": spinner1.id.split(";")[0],
                "task": spinner1.id.split(";")[1],
                "team": document.getElementById("team").innerHTML,
            }
            
            uiMeasures.push(measure)
        }
    
        for (let radio of all_radios){
            if (radio.checked == true){
                measure = {
                    "match": document.getElementById("current-match").innerHTML,
                    "measure1": radio.value,
                    "measure2": "-1",
                    "measuretype": "categorical",
                    "phase": radio.id.split(";")[0],
                    "task": radio.id.split(";")[1],
                    "team": document.getElementById("team").innerHTML,
                }
                uiMeasures.push(measure);
            }
        }
    
        for (let checkbox of all_checkbox){
            measure = {
                "match": document.getElementById("current-match").innerHTML,
                "measure1": checkbox.checked.toString(),
                "measure2": "-1",
                "measuretype": "boolean",
                "phase": checkbox.id.split(";")[0],
                "task": checkbox.id.split(";")[1],
                "team": document.getElementById("team").innerHTML,
            }
            uiMeasures.push(measure);
        }
    
        for (let star of all_stars){
            measure = {
                "match": document.getElementById("current-match").innerHTML,
                "measure1": star.value.toString(),
                "measure2": "3",
                "measuretype": "rating",
                "phase": star.id.split(";")[0],
                "task": star.id.split(";")[1],
                "team": document.getElementById("team").innerHTML,
            }
            uiMeasures.push(measure);
        }


        // SORTING UI MEASURES
        uiMeasures.sort(function(a,b){
            var phaseA = a.phase;
            var phaseB = b.phase;
            var taskA = a.task;
            var taskB = b.task;

            if(taskA < taskB){
                return -1;
            }
            if(taskA > taskB){
                return 1;
            } else {
                if(phaseA < phaseB){
                    return -1;
                }
                if(phaseA > phaseB){
                    return 1;
                }
            }
            })

            console.log(uiMeasures);
    }

    // retrieving data from database
    function checkoutData(match, team) {
        fetch(`/checkoutdata/${match}/${team}`).then(function(response) {
            return response.text();
        }).then(function(text) {

            // array with what the database returns

            var arr = JSON.parse(text);

            var result = [];

            console.log(arr);

            for(var i in arr)
                result.push(arr[i]);

            compare(uiMeasures, result);
            
        }).catch(function(err) {
            document.querySelector("#testing").innerHTML = err;
        });
    };

})();