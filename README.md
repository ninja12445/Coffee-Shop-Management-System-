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

Main Features:
[] Pre-ordering
[] Self-service ordering
[] Payment features (pay by cash or pay by credit card)
[] Manager can adjust sales record 
[] Manager can view activities, adjust sales, track ingredients, manage user info, check voucher usage
[] Handle 30 user requests at the same time  
[] <Back navigation 
[] Wait 2 Call Update | Before: Customer have to wait | After: Automatic countdown with notifications and connects to employee / manager real-time chat 
[] Membership point 
[] Scan bar code 
[] Bank Account transaction simulation 










