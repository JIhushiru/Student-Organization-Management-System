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


def run_studorg():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        with open("studorg.sql", "r") as file:
            sql_script = file.read()

        # Split the script into individual statements
        for statement in sql_script.split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)

        conn.commit()
        print("SQL script executed successfully.")

    except mariadb.Error as e:
        print(f"Error executing SQL script: {e}")
    except FileNotFoundError:
        print("studorg.sql not found.")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
