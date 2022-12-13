
const allKeyPresses = [];



$(document).ready(function () {
    let recipeTextArea = document.getElementById('recipe');
    recipeTextArea.innerHTML = "";
    recipeTextArea.onkeyup = function (e) {
        allKeyPresses.push({ character: e.key, time: new Date().getTime() });
    }
    // console.log('Document ready')

    



    function doActions() {
  
        // Show the example recipe div
        var x = document.getElementById("example-recipe-div");
        x.style.display = "block";


        // Show explanations modal
        var x = document.getElementById("example_steps");
        x.style.display = "block";

        // Show button
        var x = document.getElementById("explain-button");
        x.style.display =  "inline";

        // Show reset button
        var x = document.getElementById("reset-button");
        x.style.display = "inline";

       
    };





    $("#submit-button").click(function () {
        // log user clicks submit
        // console.log("Handler for .click() called.")
        var source = document.getElementById("recipe").innerText;
        if (!source || source.length == 0) {
            alert("You should first enter a recipe and then click on the 'Next' button.");
            return;
        }

        // Call API
        doActions()

        traceActions("submit", {'recipe': source, 'ks-recipe': allKeyPresses }, false, () => {
            allKeyPresses = []

        })

    });

    

    $("#save-button").click(function () {
        // log user clicks submit
        // console.log("Save button clicked")

        var source = $("#recipe").val();
        var q1 = "Empty"
        var q2 = "Empty"

        // log user clicks submit
        // console.log("Save button clicked")

        var source = $("#recipe").val();
        if (!source || source.length == 0) {
            alert("You should first enter a recipe and then click on the Save and Reset button.");
            return;
        }
        
        traceActions("save", { 
            'recipe':source,
            'ks-recipe': allKeyPresses, 
            "q1": q1,
            'ks-q1': {},
            "q2": q2,  
            'ks-q2': {}}, true)

    });




    $("#reset-button").click(function () {
        // log user clicks submit
        // console.log("Save button clicked")

        var source = document.getElementById("recipe").innerText;
        var q1 = $("#q1").val();
        var q2 = $("#q2").val();


        traceActions("save", {
            'recipe': source,
            'ks-recipe': allKeyPresses,
            "q1": q1,
            'ks-q1': [],
            "q2": q2,
            'ks-q2': []
        }, true)


    });






});