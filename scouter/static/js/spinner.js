(function() {
    function updateSpinner(evt){
        let phase, task, direction, match, team_number, showMisses, measureNum;
        const spinnerData = evt.currentTarget.id.split(";");
        phase = spinnerData[0];
        task = spinnerData[1];
        direction = spinnerData[2];
        showMisses = spinnerData[3];
        match = document.getElementById("current-match").innerHTML;
        team_number = document.getElementById("team").innerHTML;

        if(showMisses == 'true'){
          measureNum = spinnerData[4];

          const textInput = document.getElementById(phase + ";" + task + ";"  + measureNum);
          let curVal = parseInt(textInput.value);
          
          if (task != "hangar-level"){
              if (direction == "up"){
                  curVal += 1
              } else if (textInput.value > 0) {
                  curVal -= 1
              }
          }else{
              if (direction == "up"&&textInput.value < 4){
                  curVal += 1

              } else if (direction == "down"&&textInput.value > 0) {
                  curVal -= 1
              }
          }

          miss = 0;
          make = 0;
          textInput.value = curVal;
          
          if(measureNum == '2'){
            // define value of opposite measure
            const spinner = document.getElementById(phase+";"+task+";"+"1");
            var spinvalue = spinner.value;           
            
            // define make and miss (measure 1 & 2 respectively)
            var miss = curVal;
            var make = spinvalue;

          } else {
            // define value of opposite measure
            const spinner = document.getElementById(phase+";"+task+";"+"2");
            var spinvalue = spinner.value;

            // define make and miss (measure 1 & 2 respectively)
            var make = curVal;
            var miss = spinvalue;
          }
          
          sendMeasure(match, team_number, phase, task, make, miss, "count");
        } else {

          const textInput = document.getElementById(phase + ";" + task + ";" + "1");
          let curVal = parseInt(textInput.value);

          if (task != "hangar_level_start"&&task != "hangar_level_end"){
              if (direction == "up"){
                  curVal += 1
              } else if (textInput.value > 0) {
                  curVal -= 1
              }
          } else if (task == "hangar_level_start") {
            if (direction == "up"&&textInput.value < 2){
                curVal += 1
            } else if (direction == "down"&&textInput.value > 0) {
                curVal -= 1
            }
        } else {
              if (direction == "up"&&textInput.value < 4){
                  curVal += 1
              } else if (direction == "down"&&textInput.value > 0) {
                  curVal -= 1
              }
          }

          textInput.value = curVal;
          sendMeasure(match, team_number, phase, task, curVal, "-1", "count");
        }

    }

    all_spinners = document.querySelectorAll("button.spinnerbutton");

    for (let button of all_spinners) {
        button.addEventListener("click", updateSpinner);
    }
})();
