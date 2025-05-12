import bcrypt
from db_connection import get_connection

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def is_admin(organization):
    return organization == None

def authenticate_user(action, username, password):
    try:
        conn = get_connection()
        cur = conn.cursor()

        if action == "login":
            cur.execute("""SELECT u.username, u.password, u.organization, o.org_id, o.org_name, o.type
                           FROM userdata u
                           LEFT JOIN ORGANIZATION o ON u.organization = o.org_name
                           WHERE u.username = ?;
                        """, (username,))
            user_record = cur.fetchone()
            if user_record:
                stored_hash = user_record[1]
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                    organization = user_record[2]  # This is where we get the organization
                    org_id = user_record[3] if user_record[3] else 0  # If org_id is None, set to 0
                    if is_admin(organization):
                        return "SUPERADMIN_LOGIN_SUCCESS"
                    else:
                        return ("LOGIN_SUCCESS", organization, org_id)
                else:
                    return "Login failed!"
            else:
                return "User not found!"

        return "Invalid action"
    except Exception as e:
        return f"Error: {e}"

