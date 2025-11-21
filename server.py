import socket
import threading
import json
import sqlite3
import bcrypt
import re

DB_NAME = "users.db"
HOST = "127.0.0.1"
PORT = 5000

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def is_strong_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*()_+\-=\\|[\]{};:'\",.<>/?]", password):
        return False
    if " " in password:
        return False
    return True

def add_user(username: str, hashed_password: str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def get_user_password(username: str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def handle_client(conn, addr):
    try:
        data = conn.recv(4096)
        if not data:
            return

        try:
            req = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            resp = {"status": "error", "message": "Invalid JSON"}
            conn.sendall(json.dumps(resp).encode("utf-8"))
            return

        action = req.get("action")
        if action == "signup":
            username = (req.get("username") or "").strip()
            password = req.get("password") or ""

            if not username or not password:
                resp = {"status": "error", "message": "Username and password required"}

            elif not is_strong_password(password):
                resp = {
                    "status": "weak_password",
                    "message": ("Password must include: "
                                "8+ chars, upper, lower, digit, special, no spaces")
                }

            else:
                hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                ok = add_user(username, hashed)
                if ok:
                    resp = {"status": "ok", "message": "Account created"}
                else:
                    resp = {"status": "error", "message": "User already exists"}

        elif action == "login":
            username = (req.get("username") or "").strip()
            password = req.get("password") or ""

            if not username or not password:
                resp = {"status": "error", "message": "Username and password required"}
            else:
                stored = get_user_password(username)
                if not stored:
                    resp = {"status": "error", "message": "User not found"}
                elif bcrypt.checkpw(password.encode(), stored.encode()):
                    resp = {"status": "ok", "message": "Login successful"}
                else:
                    resp = {"status": "error", "message": "Wrong password"}

        else:
            resp = {"status": "error", "message": "Unknown action"}

        conn.sendall(json.dumps(resp).encode("utf-8"))

    finally:
        conn.close()

def main():
    init_db()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Server listening on {HOST}:{PORT}")
    try:
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    finally:
        s.close()

if __name__ == "__main__":
    main()
