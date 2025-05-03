import mariadb

def get_connection():
    try:
        return mariadb.connect(
            user="root",
            password="pwmo",
            host="localhost",
            database="studorg"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        raise