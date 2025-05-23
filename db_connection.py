import mariadb

def get_connection():
    try:
        return mariadb.connect(
            user="root",
            password="dubbuhaeun98",
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
        print("Database populated successfully.")

    except mariadb.Error as e:
        print(f"Error executing SQL script: {e}")
    except FileNotFoundError:
        print("studorg.sql not found.")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def run_views():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        with open("views.sql", encoding="utf-8") as file:
            sql_script = file.read()

        # Split the script into individual statements
        for statement in sql_script.split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)

        conn.commit()
        print("SQL views script executed successfully.")

    except mariadb.Error as e:
        print(f"Error executing SQL script: {e}")
    except FileNotFoundError:
        print("Views.sql not found.")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()