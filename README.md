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
2. Run Docker-Compose up
3. Start using OnlyFence by accessing the "login.html" page.
4. Log in using the appropriate accounts (see **Test Accounts** for credentials)

## How to set up Telegram Notifications
1. Start telebot.py. This bot will record consumer's telegram tag (e.g. @onlyfenceuser) and chat id in the Notification database to be referenced for future messages to be sent. 
2. Consumer sends https://t.me/onlyfence_bot a /start message so that the chat id of the consumer can be recorded.
3. When a content creator posts a message using the post_content.py complex microservice, the notification.py microservice will first retrieve the chatid of subscribed consumers based on their telegram tags, by referencing from the Notification database.
4. The notification.py microservice will then send each subscribed consumer a notification message using a telegram API link and the chatid of the consumer.

## User Scenarios / Walkthrough
### 1) Consumer Searches for Creator to Subscribe to
1. Starting from **"view_content.html"*** page, the user searches for a creator
2. *view_content.py* will request for the subscription status of the consumer from the *subscription_link.py* through the **"/subscription/status"** API.
3. *view_content.py* will request for the subscription price of the creator from the *creator_account.py* through the **"/creator/price"** API. (assumed that consumer is not subscribed)
4. *view_content.py* will request for the content of the creator from the *content.py* and display it on the UI for the consumer through the **"/unsubbed"** API. It shows the latest 3 results since the consumer is not subscribed.

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
1. Starting from **"upload.html"*** page, the creator selects an image to upload and a message to write. The creator will the click upload to post new content
2.  *post_content.py* will send the content information to *content.py* which will upload the content into firebase and return the upload status through the **"/upload"** API
3. *post_content.py* will request for the subscription status of the consumer from the *subscription_link.py* through the **"/subscription/status"** API.
4. *post_content.py* will request for the creator name from *creator_account.py* through **"/creator/getinfo/<string:creatorid>"** API 
5. *post_content.py* will send the creator name and subscriber information to *notification.py* through the **"/notify/<string:creatorname>"** API
6. *notification.py* will invoke the telegram API using telegram tag and telegram chat id recorded by *telebot.py* to notify subscribed consumers that the creator has posted new content
7. *notification.py* will return the notification status to *post_content.py*
8. *post_content.py* will returnt the status of the notification and content upload status to the UI so the creator can view it.

## Tools Available
- Docker
- Flask (Micro Web Framework for Python)
- Flask_CORS (Cross-origin AJAX)
- FlaskSQLAlchemy (Python SQL Toolkit)
- RabbitMQ (AMQP)
- Firebase_admin
- PayPal API
- Telegram API/Bot

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
