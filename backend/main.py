from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import datetime
import logging
import mariadb
import uvicorn
import json
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
        "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# WebSocket connection manager for real-time chat
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, user_email: str):
        await websocket.accept()
        self.active_connections[user_email] = websocket
        logger.info(f"User {user_email} connected to chat")
        
    def disconnect(self, user_email: str):
        if user_email in self.active_connections:
            del self.active_connections[user_email]
            logger.info(f"User {user_email} disconnected from chat")
            
    async def send_personal_message(self, message: str, user_email: str):
        if user_email in self.active_connections:
            await self.active_connections[user_email].send_text(message)
            
    async def broadcast(self, message: str, sender_role: str):
        disconnected = []
        for email, connection in self.active_connections.items():
            try:
                await connection.send_text(message)
            except:
                disconnected.append(email)
        
        for email in disconnected:
            self.disconnect(email)

manager = ConnectionManager()

# Data Models
class UserData(BaseModel):
    name: str
    email: str
    password: str
    role: str = "customer"

class LoginData(BaseModel):
    email: str
    password: str

class ProductData(BaseModel):
    name: str
    price: float
    description: str = ""

class OrderData(BaseModel):
    user_email: str
    items: List[dict]
    total: float
    voucher_code: Optional[str] = None
    payment_method: str = "cash"

class VoucherRedeem(BaseModel):
    user_email: str
    points_cost: int
    voucher_code: str
    discount: int

class ProfileUpdate(BaseModel):
    email: str
    name: str
    password: Optional[str] = None

class PreOrderData(BaseModel):
    user_email: str
    product_id: int
    quantity: int
    pickup_time: str
    notes: Optional[str] = None

class WaitListData(BaseModel):
    order_id: int
    status: str

# Database connection
def get_db_connection():
    try:
        return mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database="coffee_shop_db"
        )
    except mariadb.Error as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# Static file routes
@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/home.html")
async def home():
    return FileResponse("home.html")

@app.get("/user.html")
async def user_page():
    return FileResponse("user.html")

# WebSocket endpoint for real-time chat
@app.websocket("/ws/chat/{user_email}")
async def websocket_endpoint(websocket: WebSocket, user_email: str):
    await manager.connect(websocket, user_email)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Broadcast to all connected users
            broadcast_msg = json.dumps({
                "sender": message_data.get("sender", "Anonymous"),
                "message": message_data.get("message", ""),
                "timestamp": datetime.datetime.now().isoformat(),
                "role": message_data.get("role", "customer")
            })
            
            await manager.broadcast(broadcast_msg, message_data.get("role", "customer"))
            
    except WebSocketDisconnect:
        manager.disconnect(user_email)

# Registration endpoint
@app.post("/send")
async def register_user(user: UserData):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT email FROM user WHERE email = ?", (user.email,))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")

        cur.execute(
            "INSERT INTO user(name, email, password, role, points) VALUES (?, ?, ?, ?, 0)",
            (user.name, user.email, user.password, user.role)
        )
        conn.commit()

        return {"success": True, "message": "Registration successful"}

    except HTTPException:
        raise
    except Exception as e:
        print("REGISTER ERROR:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        if cur:
            try: cur.close()
            except: pass
        if conn:
            try: conn.close()
            except: pass

# Login endpoint
@app.post("/login")
async def login(credentials: LoginData):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "SELECT email, password, name, role, points FROM user WHERE email = ?", 
            (credentials.email,)
        )
        result = cur.fetchone()
        cur.close()
        conn.close()

        if not result:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        db_email, db_password, db_name, db_role, db_points = result
        
        if credentials.password != db_password:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        logger.info(f"Login successful: {credentials.email} as {db_role}")
        
        return {
            "success": True,
            "message": f"Welcome back, {db_name}!",
            "user": {
                "name": db_name,
                "email": db_email,
                "role": db_role,
                "points": db_points or 0
            }
        }
    except HTTPException as he:
        if conn:
            conn.close()
        raise he
    except Exception as e:
        if conn:
            conn.close()
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

# Products endpoints
@app.get("/api/products")
async def get_products():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id, name, price, description, image FROM products")

        products.append({
            "id": row[0],
            "name": row[1],
            "price": float(row[2]),
            "description": row[3] or "",
            "image": row[4]
        })
        
        cur.close()
        conn.close()
        
        if not products:
            products = [
                {"id": 1, "name": "Espresso", "price": 3.25, "description": "Rich and bold"},
                {"id": 2, "name": "Cappuccino", "price": 2.80, "description": "Creamy foam"},
                {"id": 3, "name": "Latte", "price": 4.50, "description": "Smooth and milky"},
                {"id": 4, "name": "Americano", "price": 3.00, "description": "Classic coffee"}
            ]
        
        return {"products": products}
    except Exception as e:
        if conn:
            conn.close()
        logger.error(f"Error fetching products: {str(e)}")
        return {"products": []}

@app.post("/api/products")
async def add_product(product: ProductData):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO products(name, price, description) VALUES (?, ?, ?)",
            (product.name, product.price, product.description)
        )
        conn.commit()
        product_id = cur.lastrowid
        cur.close()
        conn.close()
        
        return {
            "success": True,
            "id": product_id,
            "message": "Product added successfully"
        }
    except Exception as e:
        if conn:
            conn.close()
        logger.error(f"Error adding product: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/products/{product_id}")
async def update_product(product_id: int, product: ProductData):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE products SET name = ?, price = ?, description = ? WHERE id = ?",
            (product.name, product.price, product.description, product_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        return {"success": True, "message": "Product updated"}
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        cur.close()
        conn.close()
        
        return {"success": True, "message": "Product deleted"}
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=str(e))

# Orders endpoint with payment methods
@app.post("/api/orders")
async def create_order(order: OrderData):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Calculate points earned (20 points per dollar)
        points_earned = int(order.total * 20)
        
        # Mark voucher as used if provided
        if order.voucher_code:
            cur.execute(
                "UPDATE vouchers SET used = 1 WHERE code = ? AND user_email = ?",
                (order.voucher_code, order.user_email)
            )
        
        # Update user points
        cur.execute(
            "UPDATE user SET points = points + ? WHERE email = ?",
            (points_earned, order.user_email)
        )
        
        # Create order record
        created_at = datetime.datetime.now()
        cur.execute(
            "INSERT INTO orders(user_email, total, voucher_code, payment_method, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (order.user_email, order.total, order.voucher_code, order.payment_method, 'pending', created_at)
        )
        order_id = cur.lastrowid
        
        # Insert order items
        for item in order.items:
            cur.execute(
                "INSERT INTO order_items(order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                (order_id, item['id'], item['quantity'], item['price'])
            )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            "success": True,
            "order_id": order_id,
            "points_earned": points_earned,
            "message": f"Order placed! You earned {points_earned} points."
        }
    except Exception as e:
        if conn:
            conn.close()
        logger.error(f"Order error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Wait list endpoints
@app.get("/api/waitlist")
async def get_waitlist():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT o.id, o.user_email, u.name, o.total, o.status, o.created_at
            FROM orders o
            JOIN user u ON o.user_email = u.email
            WHERE o.status IN ('pending', 'preparing', 'ready')
            ORDER BY o.created_at ASC
        """)
        
        waitlist = []
        for row in cur:
            waitlist.append({
                "id": row[0],
                "email": row[1],
                "name": row[2],
                "total": float(row[3]),
                "status": row[4],
                "created_at": row[5].isoformat() if row[5] else None
            })
        
        cur.close()
        conn.close()
        return {"waitlist": waitlist}
    except Exception as e:
        if conn:
            conn.close()
        logger.error(f"Error fetching waitlist: {str(e)}")
        return {"waitlist": []}

@app.put("/api/waitlist/{order_id}")
async def update_waitlist_status(order_id: int, data: WaitListData):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE orders SET status = ? WHERE id = ?",
            (data.status, order_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        return {"success": True, "message": f"Order status updated to {data.status}"}
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=str(e))

# Pre-order endpoints
@app.post("/api/preorders")
async def create_preorder(preorder: PreOrderData):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO preorders(user_email, product_id, quantity, pickup_time, notes, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (preorder.user_email, preorder.product_id, preorder.quantity, preorder.pickup_time, preorder.notes, 'pending', datetime.datetime.now())
        )
        preorder_id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            "success": True,
            "preorder_id": preorder_id,
            "message": "Pre-order placed successfully!"
        }
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/preorders")
async def get_preorders():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id, p.user_email, u.name, pr.name as product_name, p.quantity, 
                   p.pickup_time, p.notes, p.status, p.created_at
            FROM preorders p
            JOIN user u ON p.user_email = u.email
            JOIN products pr ON p.product_id = pr.id
            WHERE p.status != 'completed'
            ORDER BY p.pickup_time ASC
        """)
        
        preorders = []
        for row in cur:
            preorders.append({
                "id": row[0],
                "email": row[1],
                "name": row[2],
                "product": row[3],
                "quantity": row[4],
                "pickup_time": row[5],
                "notes": row[6],
                "status": row[7],
                "created_at": row[8].isoformat() if row[8] else None
            })
        
        cur.close()
        conn.close()
        return {"preorders": preorders}
    except Exception as e:
        if conn:
            conn.close()
        return {"preorders": []}

@app.put("/api/preorders/{preorder_id}/confirm")
async def confirm_preorder(preorder_id: int):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE preorders SET status = 'confirmed' WHERE id = ?",
            (preorder_id,)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        return {"success": True, "message": "Pre-order confirmed"}
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=str(e))

# Vouchers endpoints
@app.get("/api/vouchers/{user_email}")
async def get_vouchers(user_email: str):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT code, discount, used FROM vouchers WHERE user_email = ?",
            (user_email,)
        )
        
        vouchers = []
        for row in cur:
            vouchers.append({
                "code": row[0],
                "discount": row[1],
                "used": bool(row[2]),
                "selected": False
            })
        
        cur.close()
        conn.close()
        return {"vouchers": vouchers}
    except Exception as e:
        if conn:
            conn.close()
        logger.error(f"Error fetching vouchers: {str(e)}")
        return {"vouchers": []}

@app.post("/api/vouchers/redeem")
async def redeem_voucher(data: VoucherRedeem):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT points FROM user WHERE email = ?", (data.user_email,))
        result = cur.fetchone()
        
        if not result or result[0] < data.points_cost:
            cur.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Not enough points")
        
        cur.execute(
            "UPDATE user SET points = points - ? WHERE email = ?",
            (data.points_cost, data.user_email)
        )
        
        cur.execute(
            "INSERT INTO vouchers(user_email, code, discount, used) VALUES (?, ?, ?, 0)",
            (data.user_email, data.voucher_code, data.discount)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            "success": True,
            "message": f"Voucher {data.voucher_code} redeemed!"
        }
    except HTTPException as he:
        if conn:
            conn.close()
        raise he
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=str(e))

# User profile endpoints
@app.get("/api/user/{email}")
async def get_user(email: str):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT name, email, role, points FROM user WHERE email = ?",
            (email,)
        )
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "name": result[0],
            "email": result[1],
            "role": result[2],
            "points": result[3] or 0
        }
    except HTTPException as he:
        if conn:
            conn.close()
        raise he
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/user/update")
async def update_profile(data: ProfileUpdate):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if data.password:
            cur.execute(
                "UPDATE user SET name = ?, password = ? WHERE email = ?",
                (data.name, data.password, data.email)
            )
        else:
            cur.execute(
                "UPDATE user SET name = ? WHERE email = ?",
                (data.name, data.email)
            )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"success": True, "message": "Profile updated"}
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=str(e))

# Sales reports
@app.get("/api/sales/daily")
async def get_daily_sales():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        today = datetime.date.today()
        cur.execute(
            "SELECT COALESCE(SUM(total), 0) FROM orders WHERE DATE(created_at) = ? AND status = 'completed'",
            (today,)
        )
        result = cur.fetchone()
        daily_sales = float(result[0]) if result else 0
        
        cur.close()
        conn.close()
        
        return {"daily_sales": daily_sales}
    except Exception as e:
        if conn:
            conn.close()
        return {"daily_sales": 0}

@app.get("/api/sales/monthly")
async def get_monthly_sales():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "SELECT COALESCE(SUM(total), 0) FROM orders WHERE MONTH(created_at) = MONTH(CURDATE()) AND YEAR(created_at) = YEAR(CURDATE()) AND status = 'completed'"
        )
        result = cur.fetchone()
        monthly_sales = float(result[0]) if result else 0
        
        cur.close()
        conn.close()
        
        return {"monthly_sales": monthly_sales}
    except Exception as e:
        if conn:
            conn.close()
        return {"monthly_sales": 0}

@app.get("/api/sales/yearly")
async def get_yearly_sales():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "SELECT COALESCE(SUM(total), 0) FROM orders WHERE YEAR(created_at) = YEAR(CURDATE()) AND status = 'completed'"
        )
        result = cur.fetchone()
        yearly_sales = float(result[0]) if result else 0
        
        cur.close()
        conn.close()
        
        return {"yearly_sales": yearly_sales}
    except Exception as e:
        if conn:
            conn.close()
        return {"yearly_sales": 0}

@app.get("/api/sales/bestselling")
async def get_best_selling():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT p.name, SUM(oi.quantity) as total_sold, SUM(oi.quantity * oi.price) as revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            JOIN orders o ON oi.order_id = o.id
            WHERE o.status = 'completed'
            GROUP BY p.id, p.name
            ORDER BY total_sold DESC
            LIMIT 10
        """)
        
        items = []
        for row in cur:
            items.append({
                "name": row[0],
                "units_sold": row[1],
                "revenue": float(row[2])
            })
        
        cur.close()
        conn.close()
        
        return {"best_selling": items}
    except Exception as e:
        if conn:
            conn.close()
        return {"best_selling": []}

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)