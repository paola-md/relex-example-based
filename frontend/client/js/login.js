
function setFormMessage(formElement, type, message) {
    const messageElement = formElement.querySelector(".form__message");

    messageElement.textContent = message;
    messageElement.classList.remove("form__message--success", "form__message--error");
    messageElement.classList.add(`form__message--${type}`);
}

function setInputError(inputElement, message) {
    inputElement.classList.add("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = message;
}

function clearInputError(inputElement) {
    inputElement.classList.remove("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = "";
}

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector("#login");
    console.log('form', loginForm)


    loginForm.addEventListener("submit", e => {
        e.preventDefault();

        console.log(document.getElementsByName('login'))

        var formData = {
            username: $("#username").val(),
            password: $("#password").val()
          };

        console.log(formData)     
        $.ajax({
            type: "POST",
            url: server + "token/",
            data: formData,
            processData: true,
            contentType: 'application/x-www-form-urlencoded',
            error: function (jqXHR, textStatus, errorMessage) {
                console.log(errorMessage); // Optional
                setFormMessage(loginForm, "error", "Invalid username/key combination");
            },
            success: function (data) { 
                console.log(data)
                console.log(data.access_token)
                console.log(data.token_type)
                var group  = data.token_type
                localStorage.setItem('mytoken', data.access_token)

                $.ajax({
                    type: "POST",
                    contentType: "application/json; charset=utf-8",
                    url: server + "trace/",
                    data: JSON.stringify({ user:  $("#username").val(),
                                           event: "login",
                                           details: {'group': group}
                                        }),
                    success: function (data) {
                        console.log("logged data")
                        console.log(data)           
                    },
                    error: function (jqXHR, textStatus, errorMessage) {
                        console.log(errorMessage); // Optional
                        setFormMessage(loginForm, "error", "Invalid key.");
                    },
                    dataType: "json",
                });

                window.location.replace("./recipe-"+group +".html");
            
            }
        });

    });


});



