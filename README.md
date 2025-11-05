# Coffee Shop Management System

This coffee shop management system will help users to achieve 10x in productivity 

User friendly, efficient and extremely easy to use. 

requirements.txt
```
Python 3.12.9        | python --version 
Mariadb              | pip show mariadb --version
fastapi 0.120.0      | pip show fastapi --version
pydantic 2.12.3      | pip show pydantic --version
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
- [ ] Pre-ordering  
- [ ] Self-service ordering  
- [ ] Wait 2 Call Update  
  - **Before:** Customer had to wait manually  
  - **After:** Automatic countdown with notifications and real-time chat with employee/manager  
- [ ] <Back navigation  

## 2. Payment & Transactions
- [ ] Payment options:  
  - Pay by cash  
  - Pay by credit card  
- [ ] Bank account transaction simulation  

## 3. User & Membership
 [PASS] Create Account, Login / Logout ✅ 
- [ ] Membership points system  
- [ ] Scan bar code  

## 4. Manager Controls
- [ ] Adjust sales records  
- [ ] View activities  
- [ ] Track ingredients
- [PASS] Manage user information ✅ 
- [ ] Check voucher usage  

## 5. System Capabilities
[PASS] Handle up to 30 user requests simultaneously  ✅


Completed Sections: 
- [PASS] Create Account, Login / Logout ✅ 
- [PASS] Manage user information ✅ 
- [PASS] Handle up to 30 user requests simultaneously  ✅

Member Registration 
<img width="1917" height="907" alt="image" src="https://github.com/user-attachments/assets/5d68a72f-85c5-4aa0-86ad-cc14b1b894d7" />

Home 
<img width="1916" height="872" alt="image" src="https://github.com/user-attachments/assets/90707c24-a545-4315-89b5-bd7faaea470a" />

User personal information (after registration and logon ) Preview 

<img width="1911" height="912" alt="image" src="https://github.com/user-attachments/assets/5eb6e264-a8ff-4eaa-91a1-3ff011dae0c4" />

TODO:
Member miss role base access
Home needs to add a logo and redesign the nav bar icon and redesign the search 



