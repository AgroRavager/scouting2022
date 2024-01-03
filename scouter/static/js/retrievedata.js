(function (){

    function retrieveData () {
        function checkoutData(match, team) {
            fetch(`/checkoutdata/${match}/${team}`).then(function(response) {
                return response.text();
            }).then(function(text) {

                /* Retrieving the list of all the measures in the database. */
                var arr = JSON.parse(text);
                var result = [];
                for(var i in arr) {
                    result.push(arr[i]);
                }

                for (let i = 0; i < result.length; i++){
                    phase = result[i].phase;
                    task = result[i].task;
                    id = phase+";"+task;
                    measure = result[i].measure1;
                    measure2 = result[i].measure2;

                    if (result[i].measure_type == "count") {
                        /* Retrieves all the spinner inputs and changes the value to the measure in the database */
                        document.getElementById(id+";1").value = measure;

                        /* If there is a measure2 (miss), changes the value of the spinner input to measure2 */
                        if (document.getElementById(id+";2")) {
                            document.getElementById(id+";2").value = measure2;
                            console.log(measure2 + id)
                        }

                    } else if (result[i].measure_type == "categorical") {
                        /* Retrieves the radio button that corresponds with the database measures and sets it to checked. */
                        document.getElementById(id+";"+measure).checked = true;
                        
                    } else if (result[i].measure_type == "boolean") {
                        /* If measure is true in the database, the checkbox will be checked on the UI, otherwise it will be set to false. */
                        if (result[i].measure1 == "true") {
                            document.getElementById(id).checked = true;
                        } else {
                            document.getElementById(id).checked = false;
                        }

                    } else {
                        /* Sets star ratings to display the correct # of stars.
                        
                        Sets the element's value to the db measure (incrementing will function normally later when pressing on the stars) */
                        const starArray = ["☆☆☆", "★☆☆", "★★☆", "★★★"];
                        document.getElementById(id).innerHTML = starArray[measure];
                        document.getElementById(id).value = measure;
                    }

                }
            }).catch(function(err) {
                document.querySelector("#testing").innerHTML = err;
            });
        };

        match = document.querySelector("#current-match").innerHTML;
        team = document.querySelector("#team").innerHTML;
        checkoutData(match, team);
    }

    document.querySelector("#buttontest").addEventListener("click", retrieveData)

})();