//checks if user has logged in; redirect to login.html if not logged in
if (!sessionStorage.getItem('ConsumerID')) {
    window.location.href = "./login.html";
}

creator_id = "CR001"
creator_name = "jackyteo"
sessionStorage.setItem('creatorID',"CR001")
sessionStorage.setItem('ConsumerID',"CON001")
// sessionStorage.setItem('creatorName',"John Doe")

document.getElementById('payment-information').innerHTML = `
    <b>Creator: </b> ${creator_name}
    `;

// Function for Subscribe Button
async function redirectPayment() {
    console.log("--- JS FUNCTION redirectPayment() ---")
    
    var subscribeURL = "http://localhost:5101/subscribe"
    var data = {CREATORID: sessionStorage.getItem('creatorID')}
    var otherParams = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }

    try {
        console.log('LOADING...')
        // Call Subscribe.py to request for payment information
        const response = 
            await fetch(
                subscribeURL, otherParams
            );
        
        const result = await response.json();
            if (response.status === 200) {
                // Success Case
                console.log('SUCCESS CASE')
                console.log(result)

                // Redirect to payment html with payment information
                code = result.code
                creatorUsername = result.creatorUsername
                creatorEmail = result.creatorEmail
                creatorID = result.creatorID
                price = result.price
                
                sessionStorage.setItem('creatorUsername',creatorUsername)
                sessionStorage.setItem('creatorEmail',creatorEmail)
                sessionStorage.setItem('price',price)

                window.location.href = "./payment.html"; 
            } else if (response.status === 404) {
                // Error
                console.log('Error: Response 404')
            } else {
                // Error
                console.log('Error: Response ???')
                throw response.status
            }
    } catch (error) {
        console.log('Error: Error in the service')
    }

}