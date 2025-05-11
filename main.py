import threading
import socket
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from authentication import authenticate_user
from db_connection import get_connection
from superadmin_panel import open_superadmin_panel
from president_panel import open_president_panel

# SERVER
def server_program():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 3001))
    server.listen()

    def handle_connection(c):
        try:
            c.send("READY".encode())  

            action = c.recv(1024).decode().strip().lower()
            username = c.recv(1024).decode()
            password = c.recv(1024).decode()

            response = authenticate_user(action, username, password) 

            c.send(response.encode())  # Send response to client

        except Exception as e:
            print(f"Error handling connection: {e}")
            try:
                c.send("Server error.".encode())
            except:
                pass
        finally:
            c.close()

    print("Server listening on localhost:3001...")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_connection, args=(client,), daemon=True).start()

# CLIENT
def send_request(action, username, password):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 3001))
        client.recv(1024)  #Wait for ready

        client.send(action.encode())
        client.send(username.encode())
        client.send(password.encode())

        response = client.recv(1024).decode()
        return response
    except Exception as e:
        return f"Error: {e}"

def login():
    username = entry_username.get()
    password = entry_password.get()
    if not username or not password:
        messagebox.showerror("Error", "Please enter username and password.")
        return
    
    result = send_request("login", username, password)
    
    if result == "SUPERADMIN_LOGIN_SUCCESS":
        messagebox.showinfo("Login Result", "Superadmin login successful!")
        open_superadmin_panel(root)
    elif result == "LOGIN_SUCCESS":
        
        try:
            conn = get_connection()
            cur = conn.cursor()

            # Check if the username is in the `president_panel` table (this is where we check if the user is a president)
            cur.execute("SELECT mem_id FROM userdata WHERE username = ?", (username,))
            user = cur.fetchone()
            
            if user:
                member_id = user[0]
                
                # Check if this user is a president
                cur.execute("SELECT * FROM president_panel WHERE mem_id = ?", (member_id,))
                if cur.fetchone():
                    open_president_panel(root, member_id)
                else:
                    messagebox.showinfo("Welcome", "You are logged in, but not a president.")
            else:
                messagebox.showinfo("Error", "User not found.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error checking president status: {e}")

    else:
        messagebox.showinfo("Login Result", result)


def register():
    username = entry_username.get()
    password = entry_password.get()
    if not username or not password:
        messagebox.showerror("Error", "Please enter username and password.")
        return
    result = send_request("register", username, password)
    messagebox.showinfo("Registration Result", result)

def clear_fields():
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

window_width = 400
window_height = 250
root = tk.Tk()
root.title("Login/Register")
root.geometry(f"{window_width}x{window_height}")  
root.resizable(False, False)


position_top = int(root.winfo_screenheight() / 2 - window_height / 2)
position_left = int(root.winfo_screenwidth() / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')


title_label = tk.Label(root, text="Login/Register", font=("Arial", 16, "bold"))
title_label.pack(pady=(20, 10)) 

form_frame = tk.Frame(root)
form_frame.pack(pady=10)

# Username
tk.Label(form_frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
entry_username = ttk.Entry(form_frame, font=("Arial", 12))
entry_username.grid(row=0, column=1, padx=10, pady=5, ipady=6)

# Password
tk.Label(form_frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
entry_password = ttk.Entry(form_frame, show="●", font=("Arial", 12))
entry_password.grid(row=1, column=1, padx=10, pady=5, ipady=6)


button_frame = tk.Frame(root)
button_frame.pack(pady=10)


btn_login = ttk.Button(button_frame, text="Login", command=login)
btn_login.grid(row=0, column=0, padx=5, ipadx=10)

btn_register = ttk.Button(button_frame, text="Register", command=register)
btn_register.grid(row=0, column=1, padx=5, ipadx=10)

btn_clear = ttk.Button(button_frame, text="Clear", command=clear_fields)
btn_clear.grid(row=0, column=2, padx=5, ipadx=10)


entry_username.focus()


if __name__ == "__main__":
    threading.Thread(target=server_program, daemon=True).start()
    root.mainloop()