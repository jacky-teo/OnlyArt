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

## User Scenarios
### 1) Consumer Searches for Creator to Subscribe to

### 2a) Create Subscription Request

### 2b) Confirm Subscription Payment

### 3) Creator Posts New Content


-Consumer Logs In  
-Content creator signs in to their account  
-Consumer subscribes to content creator  
-Content creator posts to their profile  
-Consumer views content of the subscribed content creator  
-Content creator views post statistics  

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
