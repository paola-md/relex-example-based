

var allKeyPresses = [];
var allKeyPresses_q1 = [];
var allKeyPresses_q2 = [];



function onHoverSentenceClass(classID) {
    let sentenceClass = document.getElementsByClassName("sentence-class-" + classID);
    for (let i = 0; i < sentenceClass.length; i++) {
        sentenceClass[i].classList.add("sentence-class-background-" + classID);
    }
    let notiI = document.getElementById("noti-" + classID);


    if (notiI) {
        var name = "noti-" + classID
        var classlist = $("#" + name).attr("class").split(/\s+/)[1];

        if (classlist == 'is-warning') {
            notiI.style.borderColor = "#947600"
        } else if (classlist == 'is-success') {
            notiI.style.borderColor = "green";
        } else if (classlist == 'is-primary') {
            notiI.style.borderColor = "#00D1B2";
        } else if (classlist == 'is-link') {
            notiI.style.borderColor = "purple";
        } else if (classlist == 'is-info') {
            notiI.style.borderColor = "blue";
        } else if (classlist == 'is-danger') {
            notiI.style.borderColor = "red";
        }
    }
}

function onOutHoverSentenceClass(classID) {
    let sentenceClass = document.getElementsByClassName("sentence-class-" + classID);
    for (let i = 0; i < sentenceClass.length; i++) {
        sentenceClass[i].classList.remove("sentence-class-background-" + classID);
    }
    let notiI = document.getElementById("noti-" + classID);
    if (notiI) {
        notiI.style.borderColor = "transparent";
    }
}

function hideAllNotis() {
    for (let i = 0; i < number_of_rules; i++) {
        let notiI = document.getElementById("noti-" + i);
        notiI.style.display = "none";     
    }

}

function showNotiI(classID) {
    let notiI = document.getElementById("noti-" + classID);
    if (notiI) {
        notiI.style.display = "block";
        let hint = null 
        let i = parseInt(classID)
        // console.log(i)
        if (i>=0 & i<=2) {
            hint = document.getElementById("hint-1");   
        } else if (i>=3 & i<=32){
            hint = document.getElementById("hint-2");  
        } else if (i>=33 & i<=41){
           hint = document.getElementById("hint-3");  
        } else if (i>=42& i<=45){
            hint = document.getElementById("hint-4");  
        }
        if(hint){
            hint.style.display = "block";
        }
    }
}


function addElementsToTextEditor(elements, textEditor) {
    // console.log(elements)
    textEditor.innerHTML = "";
    let innerHTML = "";

    for (let i = 0; i < elements.length; i++) {
        showNotiI(elements[i].class);
        let newElementsI = elements[i].sentence;
        newElementsI = newElementsI.replaceAll(" \n", "\n");
        if (newElementsI.charCodeAt(0) == 10) {
            newElementsI = newElementsI.substring(1);
        }
        if (newElementsI.charCodeAt(0) == 32) {
            innerHTML += "<br />";
            newElementsI = newElementsI.substring(1);
        }
        if (newElementsI.charCodeAt(newElementsI.length - 1) == 10) {
            newElementsI = newElementsI.substring(0, newElementsI.length - 1);
        }
        let hasSpaceInTheEnd = false;
        if (newElementsI.charCodeAt(newElementsI.length - 1) == 32) {
            hasSpaceInTheEnd = true;
            newElementsI = newElementsI.substring(0, newElementsI.length - 1);
        }
        
        innerHTML += "<span onmouseover=\"onHoverSentenceClass(" + elements[i].class + ")\" onmouseout=\"onOutHoverSentenceClass(" + elements[i].class + ")\" class=\"sentence-class-" + elements[i].class + "\">" + newElementsI.replaceAll("\n\n", "\n").replaceAll("\n", "<br />") + "</span>";
        if (hasSpaceInTheEnd) {
            innerHTML += " ";
        }

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
    if (recipeTextArea_q1) {
        recipeTextArea_q1.onkeyup = function (e) {
            allKeyPresses_q1.push({ character: e.key, time: new Date().getTime() });
        }
    }

    let recipeTextArea_q2 = document.getElementById('q2');
    //recipeTextArea_q2.innerHTML = "";
    if (recipeTextArea_q2) {
        recipeTextArea_q2.onkeyup = function (e) {
            allKeyPresses_q2.push({ character: e.key, time: new Date().getTime() });
        }
    }


    // console.log('Document ready')

    var complete = function (source) {

        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: server + "example",
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

        let recipeTextEditor = document.getElementById("recipe");
        if (recipeTextEditor) addElementsToTextEditor(data.user_recipe, recipeTextEditor);
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

        for (let i = 0; i < number_of_rules; i++) {
            let notiI = document.getElementById("noti-" + i);
            notiI.style.display = "none";     
        }
        hint = document.getElementById("hint-1"); 
        hint.style.display = "none";  
        hint = document.getElementById("hint-2"); 
        hint.style.display = "none";  
        hint = document.getElementById("hint-3"); 
        hint.style.display = "none";  
        hint = document.getElementById("hint-4"); 
        hint.style.display = "none";  



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


    $(".delete").click(function () {
        var id = $(this).attr('id');
        // console.log(id)
        // console.log(id.split("-"))
        var noti_num = id.split("-")[1];

        // console.log("noti-num", noti_num);
        var x = document.getElementById("noti-" + noti_num);
        x.style.display = "none";

        // console.log("class name", 'sentence-class-' + noti_num)

        let elems = document.querySelectorAll('.sentence-class-' + noti_num)
        for (let i = 0; i < elems.length; i++) {
            let elem = elems[i]
            // console.log(i, elem.outerHTML)
            elem.classList.remove('sentence-class-' + noti_num);
            elem.classList.remove("sentence-class-background-" + noti_num);
            elem.setAttribute("onmouseover", ";");
            elem.setAttribute("onmouseout", ";");
        }

        traceActions("close notification", { 'number': noti_num })

    });






});