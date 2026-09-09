async function changePassword(){

    const message = document.getElementById("message");

    const new_password1 = document.getElementById("new_password1").value;

    const new_password2 = document.getElementById("new_password2").value;

    const old_password = document.getElementById("old_password").value;

    const csrftoken = document.querySelector(
        "[name=csrfmiddlewaretoken]",
    ).value;

    const URL = "/session/change-password/";

    const passwordChangeBtn = document.getElementById("passwordChangeBtn");

    if (new_password1 != new_password2) {
        message.innerHTML = `
        <div class="alert alert-warning alert-dismissible fade show" role="alert" style="margin-top:15px;">
                New passwords do not match
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        `;
        return;
    }
    else if(old_password == new_password1 || new_password2){
        message.innerHTML = `
        <div class="alert alert-warning alert-dismissible fade show" role="alert" style="margin-top:15px;">
                Your new password same as old password
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        `;
        return;
    }

    try{

        const response = await fetch(URL , {
            method:"POST",
            headers:{
                "X-CSRFToken":csrftoken,
                "Content-Type":"application/json",
            },
            body:JSON.stringify({
                "old_password":old_password,
                "new_password1":new_password1,
                "new_password2":new_password2,
            }),
        })

        const data =  await response.json();

        if(data.success == true){
            passwordChangeBtn.innerHTML = "Success";
            passwordChangeBtn.classList.replace("btn-secondary" , "btn-primary");
            window.location.href = "/session/user-login/";
        }
    }
    catch(error){
        message.innerHTML = `
        <div class="alert alert-warning alert-dismissible fade show" role="alert" style="margin-top:15px;">
                Something went wrong
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        `
    }

}