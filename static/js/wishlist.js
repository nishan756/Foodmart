async function addToWishlist(productID){
    const message = document.getElementById("message");

    const csrftoken = document.querySelector(
        "[name=csrfmiddlewaretoken]",
    ).value;

    const URL = `/wishlist/add/${productID}/`

    try{
        const response = await fetch(URL , {
            method:"POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json",
            },
        })

        const data = await response.json();


        message.innerHTML = `
            <div class="alert alert-${data.tags} alert-dismissible fade show" role="alert">
                ${data.message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
    }
    catch(error){

    }   
}

async function removeFromWishlist(wishlistID){
    const message = document.getElementById("message");

    const csrftoken = document.querySelector(
        "[name=csrfmiddlewaretoken]",
    ).value;

    const URL = `/wishlist/delete/${wishlistID}/`

    const wishlistItem = document.getElementById(`wishlist-${wishlistID}`);

    try{
        const response = await fetch(URL , {
            method:"POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json",
            },
        })

        const data = await response.json();


        message.innerHTML = `
            <div class="alert alert-${data.tags} alert-dismissible fade show" role="alert">
                ${data.message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        if (data.status == 200){
            wishlistItem.remove();
        }
    }
    catch(error){
        message.innerHTML = `
            <div class="alert alert-error alert-dismissible fade show" role="alert">
                Something went wrong
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
    }   
}