import threading
import socket
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db_connection import run_studorg
from authentication import authenticate_user
from superadmin_panel import open_superadmin_panel
from president_panel import open_president_panel
from member_fee_panel import show_member_fee_panel

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

            result = authenticate_user(action, username, password)  # Get result from authenticate_user

            # Initialize org_id to a default numeric value (e.g., 0)
            org_id = 0

            # Handle cases based on the result format
            if isinstance(result, tuple):  # If it's a tuple, unpack
                response, organization, org_id = result
            else:  # Otherwise, it's just a string (status)
                response = result
                organization = ""

            # Send the status, organization, and org_id as a formatted string
            c.send(f"{response}|{organization}|{org_id}".encode())  # Concatenate response, org_name, and org_id

        except Exception as e:
            print(f"Error handling connection: {e}")
            try:
                c.send("Server error.".encode())
            except:
                pass
        finally:
            c.close()  # Ensure we close the connection at the end of the process

    print("Server listening on localhost:3001...")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_connection, args=(client,), daemon=True).start()

# CLIENT
def send_request(action, username, password):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 3001))
        client.recv(1024)  # Wait for ready signal

        client.send(action.encode())
        client.send(username.encode())
        client.send(password.encode())

        response = client.recv(1024).decode()  # Receive the response (status|organization|org_id)
        status, org_name, org_id = response.split('|', 2)  # Split the status, organization, and org_id
        org_id = int(org_id)  # Ensure org_id is numeric
        return status, org_name, org_id  # Return the org_id as a numeric value

    except Exception as e:
        return f"Error: {e}", "", 0  # Return 0 as default for org_id if error occurs


def login():
    username = entry_username.get()
    password = entry_password.get()
    if not username or not password:
        messagebox.showerror("Error", "Please enter username and password.")
        return
    
    status, org_name, org_id = send_request("login", username, password)  # Include org_id in the response
    
    if status == "SUPERADMIN_LOGIN_SUCCESS":
        title_label.pack_forget()
        form_frame.pack_forget()
        button_frame.pack_forget()
        open_superadmin_panel(root)
    elif status == "LOGIN_SUCCESS":
        title_label.pack_forget()
        form_frame.pack_forget()
        button_frame.pack_forget()
        open_president_panel(root, False, org_name, org_id)  # Pass org_id to the president panel
    elif status == "MEMBER_LOGIN_SUCCESS":
        title_label.pack_forget()
        form_frame.pack_forget()
        button_frame.pack_forget()
        show_member_fee_panel(root, org_id)
    else:
        messagebox.showinfo("Login Result", status)



def clear_fields():
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

run_studorg() #Use only on first run 

window_width = 1300
window_height = 650
root = tk.Tk()
root.title("Organization Database Management")
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

btn_clear = ttk.Button(button_frame, text="Clear", command=clear_fields)
btn_clear.grid(row=0, column=2, padx=5, ipadx=10)


entry_username.focus()


if __name__ == "__main__":
    threading.Thread(target=server_program, daemon=True).start()
    root.mainloop()