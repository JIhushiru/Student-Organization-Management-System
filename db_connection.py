import mariadb

def get_connection():
    try:
        return mariadb.connect(
            user="root",
            password="kurt",
            host="localhost",
            database="studorg"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        raise