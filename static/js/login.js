async function userLogin() {

    const URL = window.location.href;

    const username = document.getElementById("username").value;
    
    const password = document.getElementById("password").value;

    const csrftoken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;

    const message = document.getElementById("message");

    const signInBtn = document.getElementById("signInBtn");

    signInBtn.disabled = true;

    signInBtn.innerHTML = "Signing in..."


    try {

        const response = await fetch(URL, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                password: password,
                redirect_url:window.location.search,
            }),
        });


        const data = await response.json();

        message.innerHTML = `
            <div class="alert alert-${data.tags} alert-dismissible fade show"
                 role="alert"
                 style="margin-top:15px;">

                ${data.message}

                <button type="button"
                        class="btn-close"
                        data-bs-dismiss="alert">
                </button>

            </div>
        `;

        if (data.success === true) {
            window.location.href = data.redirect_url;
            return;
        }

        signInBtn.disabled = false;

        signInBtn.innerHTML = 'Sign In';


    } catch (error) {

        console.error(error);

        message.innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show"
                 role="alert"
                 style="margin-top:15px;">

                Something went wrong.

                <button type="button"
                        class="btn-close"
                        data-bs-dismiss="alert">
                </button>

            </div>
        `;

        signInBtn.disabled = false;

        signInBtn.innerHTML = "Signing In"

    }
}