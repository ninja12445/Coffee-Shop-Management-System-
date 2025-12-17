## Terminology and Structural Conventions

| Term / Section            | Purpose / Usage Description                                |
|---------------------------|------------------------------------------------------------|
| Add                       | Introduces a new feature, component, or capability         |
| Remove                    | Deletes an existing feature, file, or dependency           |
| Improve                   | Enhances performance, usability, or readability            |
| Fix / Fixed               | Resolves bugs, errors, or unintended behavior              |
| Release                   | Marks a versioned deployment or public availability        |
| Table (Main Section)      | Core structured data display using `| - | - | - |` format  |
| Separation                | Logical division of sections for clarity and readability   |
| Resources                 | References, links, documentation, or external materials    |

# PROJECT TASKS

---

## TASK 1: Database Setup
Seed the database and add basic user information

---

## TASK 2: User Account Creation
Modify account creation for employee and manager users

**Important:** Verify employees and managers can log into database AND backend

---

## TASK 3: Homepage Images
Change product images on homepage (images currently not displaying)

---

## TASK 4: Single-Page Application
Combine User Authentication + Dashboard + Home Page

Add role-based access control

---

## TASK 5: Employee Functions
Give employees basic CRUD operations:
- Add products
- Edit products
- Retrieve product names
- Delete products

---

## TASK 6: Manager Functions
Give managers access to:
- View revenue
- View charts
- Chat with employees and customers
- Inventory management

---

## TASK 7: Time Display
Add time display function to the system

---

## TASK 8: Order Countdown (Admin)
Add automatic order countdown with notifications (Admin section + User Interface)

---

## TASK 9: Member Points System
**Customer rewards:**
- Customers earn 50-100 random points per purchase
- Customers can redeem points for discount vouchers

---

## TASK 10: Payment Options
**Employee CRUD access:**
- Manage discount vouchers
- Manage products

**Payment modes:**
- **Cash** - Automatic ordering mode: calculates total, change, prints receipt
- **Cash** - Staff mode: calculates total, change, prints receipt
- **Credit Card** - User enters 6 digits for verification

---

## TASK 11: Order Countdown (Repeat)
Add automatic order countdown with notifications (Admin + User Interface)

---

## TASK 12: Pre-Order Function
- Select drinks
- Schedule date and time

---

## TASK 13: Self-Service Function
Add self-service functionality

---

## TASK 14: Payment Methods
Add the following:
- Cash payment
- Bank card payment
- Barcode scanning payment

---

## TASK 15: Online Chat
Users can chat with staff (Admin + User Interface)

---

## TASK 16: Order Countdown (Final)
Automatic order countdown with notifications (Admin + User Interface)

---

## OPTIMIZATION PHASE

**Database:**
- Optimize queries
- Optimize structure

**Performance:**
- Optimize threading and concurrency
- Make app lighter and more reliable
- Reduce crashes and unresponsiveness

**Interface:**
- Optimize UI/UX

---

## BUG TESTING

**Required:**
- Add log functionality
- Test normal cases
- Test edge cases

---

## FINAL DEMO

**Goal:** 100% test case coverage

## Bugs
API Requests

### Products
- `GET /api/products` → **200 OK**
  - Client: `127.0.0.1:56829`
- `GET /api/products` → **200 OK**
  - Client: `127.0.0.1:52668`
    **Error Logged**: `cannot access local variable 'products' where it is not associated with a value`

### Vouchers
- `GET /api/vouchers/customer2@gmail.com` → **200 OK**
  - Client: `127.0.0.1:56829`
- `GET /api/vouchers/customer2@gmail.com` → **200 OK**
  - Client: `127.0.0.1:52668`

### User Data
- `GET /api/user/customer2@gmail.com` → **200 OK**
  - Client: `127.0.0.1:58909`
- `GET /api/user/customer2@gmail.com` → **200 OK**
  - Client: `127.0.0.1:62311`
- `GET /api/user/customer2@gmail.com` → **200 OK**
  - Client: `127.0.0.1:52668`

---

## 💬 WebSocket Chat Activity

### Connection
- **Accepted**
  - Endpoint: `/ws/chat/customer2@gmail.com`
  - Client: `127.0.0.1:53873`
  - Timestamp: `2025-12-16 23:53:58`
- Status: `connection open`
- Log: `User customer2@gmail.com connected to chat`

### Disconnection
- Timestamp: `2025-12-17 00:03:29`
- Log: `User customer2@gmail.com disconnected from chat`
- Status: `connection closed`

---

## Errors

### Product Fetching Error
- **Timestamp**: `2025-12-17 00:03:29`
- **Source**: `main`
- **Level**: `ERROR`
- **Message**:
Error fetching products: cannot access local variable 'products' where it is not associated with a value


- **Repeated Error Logged**

---

## Real time log

| Time (UTC)              | Event |
|-------------------------|-------|
| 2025-12-16 23:53:58     | WebSocket chat connected |
| 2025-12-17 00:03:29     | Chat disconnected |
| 2025-12-17 00:03:29     | Product fetching error occurred |

---

## Notes
- All API endpoints returned **200 OK**, but img product fetching from db sending errors.
- Product errors suggest a **local variable scope issue**.
- WebSocket lifecycle work normally and reliable.

---
 
<img width="550" height="350" alt="image" src="https://github.com/user-attachments/assets/b4189468-8d2e-492f-8468-3e59848dd559" />
