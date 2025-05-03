import bcrypt
from db_connection import get_connection

# Connect to the database
conn = get_connection()
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
        login_id INTEGER PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        mem_id INTEGER,  
        FOREIGN KEY (mem_id) REFERENCES member(mem_id)
    )
""")

# Add superadmin and a default password
username1, password1 = "superadmin", "lebron"
hashed_password = bcrypt.hashpw(password1.encode(), bcrypt.gensalt())

cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username1, hashed_password))

# Commit to the database
conn.commit()

username2, password2 = "student1", "pass"
hashed_password2 = bcrypt.hashpw(password2.encode(), bcrypt.gensalt())

cur.execute("INSERT INTO userdata (username, password, mem_id) VALUES (?, ?, ?)", (username2, hashed_password2,1001))

conn.commit()
cur.close()
conn.close()
