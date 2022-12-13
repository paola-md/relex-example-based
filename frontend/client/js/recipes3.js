


var allKeyPresses = [];
var allKeyPresses_q1 = [];
var allKeyPresses_q2 = [];



function addElementsToTextEditor(elements, textEditor) {
    textEditor.innerHTML = "";
    let innerHTML = "";
    for (let i = 0; i < elements.length; i++) {

        //showNotiI(elements[i].class);
        innerHTML += "<span>" + elements[i].sentence.replaceAll("\n", "<br />") + "</span>";
    }
    textEditor.innerHTML = innerHTML;
}

function appearTopDialog() {
    let topDialog = document.getElementById("top-dialog-container");
    topDialog.classList.add("top-dialog-shown");
}


$(document).ready(function () {

    let recipeTextArea = document.getElementById('recipe');
    recipeTextArea.innerHTML = "";
    recipeTextArea.onkeyup = function (e) {
        allKeyPresses.push({ character: e.key, time: new Date().getTime() });
    }

    let recipeTextArea_q1 = document.getElementById('q1');
    //recipeTextArea_q1.innerHTML = "";
    recipeTextArea_q1.onkeyup = function (e) {
        allKeyPresses_q1.push({ character: e.key, time: new Date().getTime() });
    }

    let recipeTextArea_q2 = document.getElementById('q2');
    //recipeTextArea_q2.innerHTML = "";
    recipeTextArea_q2.onkeyup = function (e) {
        allKeyPresses_q2.push({ character: e.key, time: new Date().getTime() });
    }


    // console.log('Document ready')
    var complete = function (source) {

        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: server + "example3",
            data: JSON.stringify({
                recipe: source,
                user: localStorage.getItem('mytoken')
            }),
            success: function (data) {
                let button = document.getElementById("submit-button");
                button.innerHTML = "Analyze"

                // console.log("Data");
                // console.log(data);

                doActions(data);
                let noReflection = document.getElementById("no-reflection");
                if (!noReflection) {
                    appearTopDialog();
                }
            },
            dataType: "json",
        });
    }


    function doActions(data) {
        // console.log(data);

        // Show the example recipe div
        var x = document.getElementById("example-recipe-div");
        if (x) x.style.display = "block";


        // Show explanations
        var x = document.getElementById("explain-button");
        x.style.display = "inline";

        // Show reset button
        var x = document.getElementById("reset-button");
        x.style.display = "inline";

        // Show the recipe
        let exampleStepsTextEditor = document.getElementById("example_steps");
        if (exampleStepsTextEditor) addElementsToTextEditor(data.example_recipe, exampleStepsTextEditor);

    };





    $("#submit-button").click(function () {

        // console.log("Handler for .click() called.")
        var source = document.getElementById("recipe").innerText;
        if (!source || source.length == 0) {
            alert("You should first enter a recipe and then click on the 'Analyze' button.");
            return;
        }
        let button = document.getElementById("submit-button");
        button.innerHTML = "<div class=\"lds-ring\"><div></div><div></div><div></div><div></div></div>&nbsp;Analyze</button>" // Adding loading spinner

        traceActions("submit", { 'recipe': source, 'ks-recipe': allKeyPresses }, false, () => {
            allKeyPresses = []
            complete(source);
        })




    });



    $("#save-button").click(function () {
        // log user clicks submit
        // console.log("Save button clicked")

        var source = document.getElementById("recipe").innerText;
        var q1 = $("#q1").val();
        var q2 = $("#q2").val();
        if (!source || source.length == 0) {
            alert("You should first enter a recipe and then click on the Save button.");
            return;
        }
        // console.log(q1, q2, "Q1 and Q2")

        if (!q1 || q1.length < 2 || !q2 || q2.length < 2) {
            alert("Please answer both questions.");
            return;
        }

        let topDialog = document.getElementById("top-dialog-container");
        topDialog.classList.remove("top-dialog-shown");

        traceActions("save", {
            'recipe': source,
            'ks-recipe': allKeyPresses,
            "q1": q1,
            'ks-q1': allKeyPresses_q1,
            "q2": q2,
            'ks-q2': allKeyPresses_q2
        }, false)

        // console.log('cleaning variables')
        // Clean variables and keypresses 

        $('#q1').val('');
        $('#q2').val('');
        allKeyPresses_q1 = []
        allKeyPresses_q2 = []



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
            'ks-q1': allKeyPresses_q1,
            "q2": q2,
            'ks-q2': allKeyPresses_q2
        }, true)


    });








});