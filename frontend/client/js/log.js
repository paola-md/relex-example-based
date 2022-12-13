
function traceActions(event, details, reload, callback) {

    var curr_user = localStorage.getItem('mytoken')
    if (curr_user === null) {
        curr_user = 'visitor_' + (Math.random() * 100);
        localStorage.setItem('mytoken', curr_user)
      }

    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: server + "trace/",
        data: JSON.stringify({
            user: curr_user,
            event: event,
            details: details
        }),

        success: function (data) {
            console.log("logged data")
            console.log(data)
            if (callback) {
                callback();
            }
            if(reload){
                location.reload();
            }
        },
        error: function (jqXHR, textStatus, errorMessage) {
            console.log(data)
            console.log(event)
            console.log(details)
            console.log(errorMessage); // Optional

            if (callback) {
                callback();
            }
        },
        dataType: "json",
    });

}


