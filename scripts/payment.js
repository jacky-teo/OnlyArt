paypal.Buttons({
    // Sets up the transaction when a payment button is clicked
    createOrder: function(data, actions) {
        return actions.order.create({
            intent: 'CAPTURE',
            purchase_units: [{
                amount: {
                    value: '77.44' // Can reference variables or functions. Example: `value: document.getElementById('...').value`
                },
                payee: {
                    email_address: 'sb-go47cv14389012@business.example.com' // Insert recipient's email account here
                },
                payment_instruction: {
                    platform_fees: [
                        {
                            amount: {
                                currency_code: "SGD",
                                value: "5.00"
                            },
                            payee: {
                                email_address: "sb-vrehs14346230@business.example.com",
                            }
                        }
                    ],
                    disbursement_mode: "INSTANT"
                }
            }]
        });

        //throw error if there is problem intiating transaction
        //throw new Error(errorMsg)
    },

    // Finalize the transaction after payer approval
    onApprove: function(data, actions) {
        return actions.order.capture().then(function(orderData) {
            // Successful capture! For dev/demo purposes:
                console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
                var transaction = orderData.purchase_units[0].payments.captures[0];
                // alert('Transaction '+ transaction.status + ': ' + transaction.id + '\n\nSee console for all available details');

            // When ready to go live, remove the alert and show a success message within this page. For example:
                var element = document.getElementById('paypal-button-container');
                element.innerHTML = '';
                element.innerHTML = '<h3>Thank you for your payment!</h3>';
                // Or go to another URL:  actions.redirect('thank_you.html');
        });
    }

    //add onCancel function to show cancellation page or return to creator's page in preview mode

    //add onError function for error handling and displaying error page to users

}).render('#paypal-button-container');



// For Paypal Javascript SDK

// Paypal Developer Dashboard: https://developer.paypal.com/developer/applications 
// Sandbox PayPal Environment: https://www.sandbox.paypal.com/ 
    // Use this to check sandbox account

// Sandbox Accounts
    // Customer 1 (SG)
    // Email: sb-y47azb14478818@personal.example.com
    // Pass: 9LHeM.z)
    // ID: DVGTPJTTXK4KC

    // Customer 2 (SG)
    // Email: sb-x47npc14478827@personal.example.com
    // Pass: qS|[24%h

    // Content Creator (SG)
    // Email: sb-go47cv14389012@business.example.com
    // Pass: hfAp.0jT
    // Account ID: MGPG8H9TFN528

    // Content Creator (US)
    // Email: sb-hcmzn14332506@business.example.com
    // Pass: aO=hx,N1
    // Account ID: B32XMXM3YDPQQ

// Sandbox Client ID of REST app
    // Email: sb-vrehs14346230@business.example.com
    // Pass: AYip4<3e
    // Client ID: Afx50ZFn0R7g2tyN0P08kc3fBR0Csy8w1J25MND90MVCnpbLwiaIS-UiNElzqypPKulongQDAcq41D0M
    // This App type is: Platform

// Resources
// PayPal Standard Integration: https://developer.paypal.com/docs/checkout/standard/integrate/
// JS SDK: https://developer.paypal.com/sdk/js/configuration/ 
    // See "Complete Reference" > Buttons: This allows us to modify the behaviour of the PayPal button
// Paypal Multiparty Payments (for Platform App type): https://developer.paypal.com/docs/multiparty/
    // Integrate sellers before payment: https://developer.paypal.com/docs/multiparty/seller-onboarding/before-payment/ 
    // Issue Refunds from Seller to Buyer: https://developer.paypal.com/docs/multiparty/issue-refund/ 