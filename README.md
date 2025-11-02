# Coffee Shop Management System

This systems hope to offer a solution to help user overcome inconveniency and help boost productivity in selling coffee shop

requirements.txt
```
Python 3.12.9 | Check python version by typing python --version 
Mariadb
FastAPI
```

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
- [ ] Membership points system  
- [ ] Scan bar code  

## 4. Manager Controls
- [ ] Adjust sales records  
- [ ] View activities  
- [ ] Track ingredients  
- [ ] Manage user information  
- [ ] Check voucher usage  

## 5. System Capabilities
- [ ] Handle up to 30 user requests simultaneously  










