async function loadThanas(){
    const districtId = document.getElementById("district").value;
    const thanaSelect = document.getElementById("thana");

    thanaSelect.innerHTML = '<option value="">Loading..</option>';

    try {
        const response = await fetch(`/site-setting/thana-list/?district_id=${districtId}`);
        const data = await response.json();

        if(Object.keys(data.thanas).length > 0 ){
            thanaSelect.innerHTML = '<option value="">Select Thana</option>';
        }
        else{
            thanaSelect.innerHTML = '<option>No Thana Found</option>';
            return;
        }
        data.thanas.forEach(thana => {
            thanaSelect.innerHTML += `
                <option value="${thana.id}">${thana.name}</option>
            `;
        });

    } catch (error) {
        console.error(error);
        thanaSelect.innerHTML = '<option value="">Failed to load</option>';
    }
}

async function loadShippingCharge(){
    const thanaId = document.getElementById("thana").value;
    const shippingCharge = document.getElementById("shippingCharge");
    const subTotal = document.getElementById("subtotal").innerHTML;
    const grandTotal = document.getElementById("grand-total");
    if(thanaId){

        try{
            const response = await fetch(`/site-setting/shipping-charge/?thana_id=${thanaId}`);
            const data = await response.json();

            if(data.success){
                shippingCharge.innerHTML = data.charge;
                grandTotal.innerHTML = Number(data.charge)+Number(subTotal)
            }
            
        }
        catch(error){
            
        }
    }

}