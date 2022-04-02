# OnlyFence
OnlyFence is a content subscription service that allows content creators to earn money from users who subscribe to their content. This is a similar concept to OnlyFans and Patreon.  

![Fences](https://cdn.vox-cdn.com/thumbor/NXI3rAC_jN7zEcdUbBM4K6bbBPM=/0x0:3000x2000/1200x0/filters:focal(0x0:3000x2000):no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/21760265/iStock_598783266.jpg)

## TO-DO
- [Done] Design UI page [Login & POST]
- [ ] Use of REST API 
- [Done] Set Up Database 
- [Done] Figure out Telegram Bot & Paypal API
- [Done] Finish Proposal Slides
- [ ] Design the HTML pages
- [ ] Integrate KongAPI
- [ ] Finish Complex Microservices

## How to set up OnlyFence
1. Start WAMP and run all SQL scripts under the "databases" folder.
2. Run Docker Compose (?)
3. Start using OnlyFence by accessing the "login.html" page.
4. Log in using the appropriate accounts (see **Test Accounts** for credentials)

## User Scenarios / Walkthrough
### 1) Consumer Searches for Creator to Subscribe to
1. blablabla
2. blebleble
3. blublublu
4. blobloblo

### 2a) Create Subscription Request
  1. On the **"creator_info.html"** page, if a user is not subscribed to the creator, a subscribe button will be present.
  2. Clicking on the subscribe button will call *subscribe.py* through the **"/subscribe"** API.
  3. *Subscribe.py* will request for the creator's payment information from *creator_account.py* through the **"/creator/price"** API.
  4. *Subscribe.py* will return the information to the UI.
  5. The UI will redirect the user to **"payment.html"** page, which holds the Paypal components.
  6. Clicking on the Paypal button will call the Paypal API which receives the creator information from the UI.
  7. Paypal API will generate an order on their servers and generate a pop-up window for the user to provide their payment information and approve the transaction.

### 2b) Confirm Subscription Payment
  8. Once a user approves the transaction on the Paypal pop-up window, Paypal will immediately capture the transaction. Funds will be transferred from the user's account, to the creator account, platform account and to Paypal for service fees.
  9. Paypal API will return a JSON with an order summary and status, to the UI.
  10. Upon receiving the JSON, the UI will call *subscribe.py* through the **"/confirmSubscription"** API.
  11. *Subscribe.py* will send the subscription information to *subscription_link.py* through the **"/subscription/add"** API.
  12. *Subscription_link.py* will create a new record in the *subscription_link* database.
  13. *Subscribe.py* will send the subscription information to payment_log.py through the **"/payments/log"** API.
  14. *Payment_log.py* will create a new record in the *payment_log* database.
  15. *Subscribe.py* will return a successful status to the UI.
  16. UI shows a confirmation message and a button that allows the user to return to **"creator_info.html"**.

### 3) Creator Posts New Content
1. fencefencefence
2. fancefancefance
3. funcefuncefunce
4. foncefoncefonce

## Tools Available
- Docker
- Flask (Micro Web Framework for Python)
- Flask_CORS (Cross-origin AJAX)
- FlaskSQLAlchemy (Python SQL Toolkit)
- RabbitMQ (AMQP)
- Firebase_admin
- PayPal API
- Telegram Bot

## Accounts
**For Sandbox Accounts**    
user: G03T02@gmail.com  
password: SubwayEatFresh123  

## Test Accounts
### OnlyFence
##### Customer Accounts
  @jackyteojianqi  
Username: imnew  
Password: pass123  

  @erlynnehazey  
Username: logi  
Password: pass123  

##### Creator Accounts
  Username: jackyteo  
  Password: pass123  

 ### PayPal
 ##### Customer Paypal
  Email:    sb-y47azb14478818@personal.example.com  
  Password: 9LHeM.z)  
 ##### Creator Paypal
  Email:    sb-go47cv14389012@business.example.com  
  Password: hfAp.0jT
##### Platform Paypal
  Email:    sb-vrehs14346230@business.example.com  
  Password: AYip4<3e  

*You can check Paypal balance from the sandbox environment: https://www.sandbox.paypal.com/*  

*This is a school project.*
