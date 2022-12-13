function highlightRulesIngredients() {
    var elem_list = []

    var x = document.getElementById("noti-0");
    if (x.style.display == 'block') {
        let elem = {
            highlight: /ingredients?/gi,
            className: 'yellow'
        }
        elem_list.push(elem)
    }
    var x = document.getElementById("noti-2");
    if (x.style.display == 'block') {
        let elem = {
            highlight: / -/gi,
            className: 'yellow'
        }
        elem_list.push(elem)
    }

    var x = document.getElementById("noti-6");
    if (x.style.display == 'block') {
        let elem = {
            highlight: /bonned?|boneless|skinned?|shelled|deveined/gi,
            className: 'blue'
        }
        elem_list.push(elem)
    }

    var x = document.getElementById("noti-7");
    if (x.style.display == 'block') {
        let elem = {
            highlight: /unsalted butter|salted butter|butter/gi,
            className: 'blue'
        }
        elem_list.push(elem)
    }

    var x = document.getElementById("noti-8");
    if (x.style.display == 'block') {
        let elem = {
            highlight: /compressed yeast|dry yeast|active yeast|active dry yeast|quick-rising yeast|quick yeast|yeast/gi,
            className: 'blue'
        }
        elem_list.push(elem)
    }

    console.log(elem_list)
    return elem_list
};

function highlightRulesSteps() {
    var elem_list = []

    var x = document.getElementById("noti-0");
    if (x.style.display == 'block') {
        let elem = {
            highlight: /steps?|method?|description/gi,
            className: 'yellow'
        }
        elem_list.push(elem)
    }
    var x = document.getElementById("noti-3");
    if (x.style.display == 'block') {
        let elem = {
            highlight: /[0-9]+\./gi,
            className: 'yellow'
        }
        elem_list.push(elem)
    }

    var x = document.getElementById("noti-4");
    if (x.style.display == 'block') {
        let elem = {
            highlight: /(will|must|should) (be|look|feel)/gi,
            className: 'green'
        }
        elem_list.push(elem)
    }

    var x = document.getElementById("noti-5");
    if (x.style.display == 'block') {
        let elem = {
            highlight: /to prevent|to remove|in order to|so that|in order that/gi,
            className: 'green'
        }
        elem_list.push(elem)
    }

    var x = document.getElementById("noti-9");
    if (x.style.display == 'block') {
        let elem = {
            highlight: /(small|medium|large|big) (saucepan|skillet|pan|pot)/gi,
            className: 'blue'
        }
        elem_list.push(elem)
    }

    var x = document.getElementById("noti-10");
    if (x.style.display == 'block') {
        let elem = {
            highlight: /(covered|uncovered) (saucepan|skillet|pan|pot)/gi,
            className: 'blue'
        }
        elem_list.push(elem)
    }

    var x = document.getElementById("noti-11");
    if (x.style.display == 'block') {
        let elem = {
            highlight: /(low|medium|high) \W+ (?:\w+\W+){0,5}?(heat|simmer)/gi,
            className: 'blue'
        }
        elem_list.push(elem)
    }



    console.log(elem_list)
    return elem_list
};

function highlightRulesRecipe() {
    var elem_list = []

    var x = document.getElementById("noti-0");
    if (x.style.display == 'block') {
        let elem = {
            highlight: /ingredient?|step?|method?|description/gi,
            className: 'yellow'
        }
        elem_list.push(elem)
    }


    console.log(elem_list)
    return elem_list
};