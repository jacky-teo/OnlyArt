creator_id = "CR001"
creator_name = "jackyteo"
sessionStorage.setItem('creatorID',"CR001")
// sessionStorage.setItem('creatorName',"John Doe")

document.getElementById('payment-information').innerHTML = `
    <b>Creator: </b> ${creator_name}
    `;

async function redirectPayment() {
    console.log("--- JS FUNCTION redirectPayment() ---")
    
    // const Http = new XMLHttpRequest();
    // const url='http://localhost:5002/creator/price?CREATORID=CR001';
    // Http.open("GET", url);
    // Http.send();

    // Http.onreadystatechange = (e) => {
    //     console.log(Http.responseText)
    // }
    
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
        const response = 
            await fetch(
                subscribeURL, otherParams
            );
        
        const result = await response.json();
            if (response.status === 200) {
                // Success Case
                console.log('SUCCESS CASE')
                console.log(result)

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



// $('subscribe').click(function(){
//     $.ajax({
//         url: subscribeURL,
//         type: "GET",
//         success: function(result){
//             console.log(result)
//         },
//         error: function(error){
//             console.log(`Error ${error}`)
//         }
//     })
// })

// $(async() => {
//     var subscribeURL = "http://localhost:5101/subscribe"

//     try {
//         const response = 
//             await fetch(
//                 subscribeURL, { method: 'GET' }
//             );
//         const result = await response.json();
//             if (response.status === 200) {
//                 // Success Case
//                 console.log('SUCCESS CASE')
//             } else if (response.status === 404) {
//                 // Error
//                 console.log('Error: Response 404')
//             } else {
//                 // Error
//                 console.log('Error: Response ???')
//                 throw response.status
//             }
//     } catch (error) {
//         console.log('Error: Error in the service')
//     }
// })
