# Coffee Shop Management System

This coffee shop management system will help users to achieve 10x in productivity 

User friendly, efficient and extremely easy to use. 

requirements.txt
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
mariadb==1.1.8
pydantic==2.5.0
python-multipart==0.0.6
websockets==12.0
```
pydantic library 

Run via Frontend
```
python -m http.server 3000
```
# what does this do ? 
> It starts an http server for the client at port 3000 

---
Run via backend
```
.venv\foldername\activate   |  run virtual environment 
```
---
```
uvicorn main:app --reload 
```
Here the server will run backend at port 8000

# Main Features

## 1. Ordering Features
- [ ] Pre-ordering  ✅
- [ ] Self-service ordering  
- [ ] Wait 2 Call Update  
  - **Before:** Customer had to wait manually  
  - **After:** Automatic countdown with notifications and real-time chat with employee/manager  
- [ ] <Back navigation  

## 2. Payment & Transactions
- [ ] Payment options:  
  - Pay by cash  ✅ 
  - Pay by credit card  ✅ 
- [ ] Bank account transaction simulation  

## 3. User & Membership
 [PASS] Create Account, Login / Logout ✅ 
- [ ] Membership points system  ✅
- [ ] Scan bar code  

## 4. Manager Controls
- [ ] Adjust sales records  ✅
- [ ] View activities  
- [ ] Track ingredients
- [PASS] Manage user information ✅ 
- Check voucher usage ✅

## 5. System Capabilities
- [PASS] Create Account, Login / Logout ✅ 
- [PASS] Manage user information ✅ 
- [PASS] Handle up to 30 user requests simultaneously  ✅
  
## Member Registration Screen 
## After 
<img width="1917" height="872" alt="LoginScreenUI" src="https://github.com/user-attachments/assets/ba70255c-44f7-416d-b255-63f96a7093c7" />

## Login Screen
<img width="1911" height="861" alt="CreateAccountScreenUI" src="https://github.com/user-attachments/assets/36f496b8-dcbb-4c6e-8bdb-54e23cef737f" />


## Home 
<img width="1914" height="909" alt="image" src="https://github.com/user-attachments/assets/0df54820-d98e-435a-9a64-1a67e20d0b53" />


## User Account  
<img width="1917" height="907" alt="image" src="https://github.com/user-attachments/assets/fdb5d1be-24ef-4ebd-ae4f-22e0dfd54152" />

## Voucher Redeem
<img width="1121" height="521" alt="image" src="https://github.com/user-attachments/assets/71831d2c-ebc8-403a-b497-c4737b5b5d2a" />

## Preorder 
<img width="1149" height="725" alt="image" src="https://github.com/user-attachments/assets/5014cb20-8145-4263-80eb-6742e545faac" />

## Update Personal 
<img width="1129" height="534" alt="image" src="https://github.com/user-attachments/assets/a6248d1a-78f6-4309-ab86-1316f8528d6e" />

## Real time chat with employee and Manager 
<img width="1110" height="621" alt="image" src="https://github.com/user-attachments/assets/30343650-f08c-4478-a567-cbed6ca32cbe" />

TODO:
Member miss role base access
Home needs to add a logo and redesign the nav bar icon and upgrades the search can find exact products



