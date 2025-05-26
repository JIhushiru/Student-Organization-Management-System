import bcrypt
from db_connection import get_connection

def hash_password(password):
    """Password hash"""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def is_admin(organization):
    """Checker if admin"""
    return organization is None

def authenticate_user(action, username, password):
    """User Authentication"""
    try:
        conn = get_connection()
        cur = conn.cursor()

        if action == "login":
            cur.execute("""
                        SELECT 
                                u.username, 
                                u.password, 
                                u.user_type,
                                o.org_name,
                                u.mem_id, 
                                o.org_id
                            FROM USERDATA u
                            LEFT JOIN SERVES s ON u.mem_id = s.mem_id
                            LEFT JOIN ORGANIZATION o ON s.org_id = o.org_id
                            WHERE u.username = ?
                        """, (username,))
            user_record = cur.fetchone()
            if user_record:
                stored_hash = user_record[1]
                user_type = user_record[2]
                organization = user_record[3]
                mem_id = user_record[4]
                org_id = user_record[5]
                if org_id is None:
                    org_id = 0
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                    if user_type == "admin":
                        return "ADMIN_LOGIN_SUCCESS"
                    elif user_type == "president":
                        return ("PRESIDENT_LOGIN_SUCCESS", organization, org_id)
                    elif user_type!= "Member":
                        return ("MEMBER_LOGIN_SUCCESS", "", mem_id)
                    else:
                        return "Unknown user type!"
                else:
                    return "Login failed!"
            else:
                return "User not found!"

        return "Invalid action"
    except ImportError as e:
        return f"Error: {e}"
