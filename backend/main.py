# import mariadb 
from fastapi import FastAPI, HTTPException, Body
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional  
from fastapi import FastAPI
import datetime as datetime
import logging 
import mariadb 
import uvicorn 
import logging 
from uuid import UUID, uuid4 
import sys 
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.responses import FileResponse
"""
references: 
https://mariadb.com/docs
https://github.com/mariadb-corporation/Developer-Examples?
"""


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# implements Model here 
# data models in simple term is what type of information we are trying to describe

class User(BaseModel): 
    id: Optional[UUID] = None 
    name: str
    email: str 
    role: str 
    created_at: Optional[datetime.datetime] = None
    
"""
class addToCart(user, employee):
    pass 
   
class ():
"""    

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="coffee_shop_db"
    )
except mariadb.Error as e:
    logger.error(f"Error connecting to MariaDB Platform: {e}")
    raise HTTPException(status_code=500, detail="Db connection decline")
else:
    print("Connection Success!")
    

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/dashboard")
async def dashboard():
    return FileResponse("dashboard.html")

@app.get("/dashboard.html")
async def dashboard_html():
    return FileResponse("dashboard.html")
# API endpoint need 
# Goal: defines a URL at /api/menu that frontend can call 
# Get Cursor

class UserData(BaseModel):
    name: str
    email: str
    password: str 

@app.post("/send")
async def receive_request(user: UserData):
    created_at = datetime.datetime.now() 
 
    
    cur=conn.cursor() 
    cur.execute("INSERT INTO user(name, email, password, created_at) VALUES (?, ?, ?, ?)", (user.name, user.email, user.password, created_at))
    conn.commit()
    cur.close()
    return {
       "success": True,
       "message": "Successfully stored user information into database",
    }


@app.post("/login")
async def login(data: dict):
    email = data.get("email")  
    password = data.get("password")
    
    # Validate input
    if not email or not password:
        raise HTTPException(status_code=400, detail="Both fields are required!")
    
    try: 
        cur = conn.cursor()
        cur.execute("SELECT email, password, name FROM user WHERE email = ? AND password = ?", (email, password))
        result = cur.fetchone()
        cur.close()

        if result is None:
            raise HTTPException(status_code=401, detail="Invalid name or password")
        
        # Extract data
        db_email = result[0]
        db_password = result[1]
        db_name = result[2]
        
        if password != db_password:
            raise HTTPException(status_code=401, detail="Incorrect password")
        
        return {
            "success": True,
            "message": f"Welcome back! {db_name}",
            "user": {
                "name": db_name,
                "email": db_email
            }
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")
    

@app.get("/")
def root(): 
    return {"message": "API is running"} 
    
@app.get("/api/users")
def get_users():
    #Get user in db 
    cur = conn.cursor() 
    cur.execute("SELECT * FROM user")
    
    users = [] 
    
    for row in cur: 
        users.append({
        "name": row[1],
        "email": row[2],
        "password": row[3],
        "created_at": str(row[4])
        })

    cur.close() 
    return {"users": users}
    

#No query ! Problem
# Setup cursor : cur = conn.cursor()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    


 
"""
#Update user information -> sends to database
Todo:
Create| PUT [item]    / [multi items]
Read  | GET [item]    / [multi items]
Update| POST [item]   / [multi items]
Delete| DELETE [item] / [multi items] 
"""