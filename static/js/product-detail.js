  // Quantity Plus & Minus functionality
  const qtyInput = document.getElementById('qty');
  document.getElementById('btn-plus').addEventListener('click', () => {
    let currentVal = parseInt(qtyInput.value) || 1;
    if (currentVal < parseInt(qtyInput.max)) qtyInput.value = currentVal + 1;
  });
  
  document.getElementById('btn-minus').addEventListener('click', () => {
    let currentVal = parseInt(qtyInput.value) || 1;
    if (currentVal > parseInt(qtyInput.min)) qtyInput.value = currentVal - 1;
  });

async function deleteReview(reviewID) {
    const productReview = document.getElementById(`productReview-${reviewID}`);

    const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    const URL = `/product/delete-review/${reviewID}/`;

    const message = document.getElementById("message");

    try{
      const response = await fetch(URL , {
        method:"POST",
        headers:{
          "X-CSRFToken":csrftoken,
          "Content-Type":"application/json",
        }
      })

      const data = await response.json();

      if(data.success == true){
        productReview.remove();
        message.innerHTML = `
            <div class="alert alert-${data.tags} alert-dismissible fade show" role="alert" style="margin-top:15px;">
                ${data.message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
      }
      else{
        message.innerHTML = `
            <div class="alert alert-${data.tags} alert-dismissible fade show" role="alert" style="margin-top:15px;">
                ${data.message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
      }
    }
    catch(error){
      message.innerHTML = `
            <div class="alert alert-${data.tags} alert-dismissible fade show" role="alert" style="margin-top:15px;">
                ${data.message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
    }

}