Bckend use fastAPI + uvicorn + MariaDb (have documentation links to their docs in Reference folder)


## Major functionalities 
1. Real time chat (bckend + frnt end)
2. Automatic ordering cnt down with notification (bckend + frnt end) 
3. Membership points
4. Payments option
5. Preordering
6. Self service
7. Wait 2 call
8. Scan barcode
9. Pay by cash

## New Accomplishments
| Feature           | Does it support? |                    Status                     |
| ----------------- | -------- | --------------------------------------------- |
| *Real-time chat   | ✅        |    web socket but incomeplete                 |
| Login / register  | ✅        |                    working                    |
| Add to Cart       | ❌        |  missing on home.html, work in user           |
| Membership points | ✅        |                   working                     |
| Vouchers         | ✅         |                   working                     |
| Preordering       | ✅        |                   working                     |
| Self-service      |   ❌       |                                              |
| Waitlist          |   ✅       |                  working                     |
| QR Scan           |   ❌       |                                              |

---
* reason why real time chat not working stable is bc the message sent but have no receiver(s).

User membership registration & account register 
---

## What needs to get polish ? 
- Role based controll access authorization
- Back Navigation
- Redesign UI - UX, more interactive
- Makes it userfriendliness
- Checks typography, bckground colour and system architectures
- Rechecks threadings and concurrency

## What need to be replace ? 
- Replace menu sections -> Navbar with header and clear Section
- Implements the remaining features and core functionalities

## Network Protocol 
How does the backend connect to the frontend and vice versa? 
TCP 3 - Way Handshake 
1. DNS here is my local host (my own IP address, signalling at 127.0.0.1:3000)  
2. TCP handshake
   - browser assigns port number
   - it then sends SYN into DNS (which is at 127.0.0.1:3000)
3. Python responses using SYN-ACK
4. Next, my browser (computer connects to the backend, which is the server) uses ACK
   - It tells the server it is ready to connect
5. Now the connection is ready to open and established. The fascinating thing is that it listens for handshake packets
6. Now the user begins to interact, and it sends HTTP requests
7. Browser sends a GET method
8. Python backend finds the exact index.html, and it then reads through the file  
9. Server sends HTTP response [200: Status Code | OK: Status Message]
10. Browser renders index.html file
11. uvicorn
   - connects to port 8000
   --restart the server when the code is changed
   - main.py identifies the app variable
     
# User Authentication 
+ Role Base Access Control
+ User Session with permissions (what each user can do and cannot do)

## Confirmation:
+ Real time chat does not create a chat room between two users, but user can send their message
+ That means user can successfully chat but not send to many users or different user.
  
## Acknowledgement:
+ Due to limited time the program achieves 85% robustness and employee can add item / delete item and directly store in database
+ Must download HeidiSQL, and Create SQL Table for it to work
+ Total bugs detected: 80+, mostly annoying bugs come from the backend (and api end points, most mechanism works) and CORS (connect endpoint and sending real time message) 
+ Average bug length: 50 lines 






