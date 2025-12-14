## Run unit Test 
How to run the unit tests, program code and test case running 

# Unit Test Cases

| Test Case ID | Description                | Input        | Expected Output | Status |
|--------------|----------------------------|-------------|----------------|--------|
| TC1         | Create Account, Login / Logout | username, password   | access / logout   | Pass ✅|
| TC2         | Connects Bckend & Frnt End     |  CORS, PORT Listen   | Successfully Server sent a 200  GET from uvicorn | Pass✅ |
| TC3         | Manage user information        | User clicks button   | View & Edit Settings   | Pass ✅|
| TC4         | 30 User Requests Handling      | sending multiple user requests |  30 Users successfully connect and use the program   | Pass✅ |


## Edge Test Cases

| Test Case ID | Description                   | Input           | Expected Output | Status |
|--------------|-------------------------------|----------------|----------------|--------|
| EC1         |  Unauthorize Login         | user types the Dashboard URL to gain access             |    System blocks and sends back error message, prevents access            | Pass✅ |
| EC2         |  
| EC3         |    
| EC4         |  
| EC5         |        


