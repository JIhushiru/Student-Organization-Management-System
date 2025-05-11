import bcrypt
from db_connection import get_connection

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def is_superadmin(username):
    return username == "superadmin"

def authenticate_user(action, username, password):
    try:
        conn = get_connection()
        cur = conn.cursor()

        if action == "login":
            cur.execute("SELECT username, password FROM userdata WHERE username = ?", (username,))
            user_record = cur.fetchone()
            if user_record:  
                stored_hash = user_record[1]  
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                    if is_superadmin(username):
                        return "SUPERADMIN_LOGIN_SUCCESS"
                    else:
                        return "LOGIN_SUCCESS"
                else:
                    return "Login failed!"
            else:
                return "User not found!"

        elif action == "register":
            cur.execute("SELECT * FROM userdata WHERE username = ?", (username,))
            if cur.fetchall():
                return "Username already exists!"
            else:
                cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, hash_password(password)))
                conn.commit()
                return "Registration successful!"
        return "Invalid action"
    except Exception as e:
        return f"Error: {e}"