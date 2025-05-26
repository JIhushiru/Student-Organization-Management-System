"""Imports"""
import threading
import socket
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from db_connection import run_studorg, run_views
from authentication import authenticate_user
from superadmin_panel import open_superadmin_panel
from president_panel import open_president_panel
from member_fee_panel import show_member_fee_panel

# ========================== DATABASE INIT ==========================
run_studorg()  # Comment out after first run
run_views()

# ========================== GUI SETUP ==========================
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 650

root = ctk.CTk()
root.title("Organization Database Management")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(False, False)

position_top = int(root.winfo_screenheight() / 2 - WINDOW_HEIGHT / 2)
position_left = int(root.winfo_screenwidth() / 2 - WINDOW_WIDTH / 2)
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{position_left}+{position_top}')

main_frame = ctk.CTkFrame(root, corner_radius=20, fg_color="#ffffff")
main_frame.pack(fill="both", expand=True)

# ========================== SERVER ==========================
def server_program():
    """Server listener that handles login authentication requests."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 3001))
    server.listen()

    def handle_connection(client_socket):
        try:
            client_socket.send("READY".encode())
            action = client_socket.recv(1024).decode().strip().lower()
            username = client_socket.recv(1024).decode()
            password = client_socket.recv(1024).decode()

            result = authenticate_user(action, username, password)

            org_id = 0
            if isinstance(result, tuple):
                response, organization, org_id = result
            else:
                response = result
                organization = ""

            client_socket.send(f"{response}|{organization}|{org_id}".encode())

        except Exception as e:
            print(f"Error handling connection: {e}")
            try:
                client_socket.send("Server error.".encode())
            except Exception:
                pass
        finally:
            client_socket.close()

    print("Server listening on localhost:3001...")
    while True:
        client, _ = server.accept()
        threading.Thread(target=handle_connection, args=(client,), daemon=True).start()

# ========================== CLIENT ==========================
def send_request(action, username, password):
    """Send login request to the server."""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 3001))
        client.recv(1024)

        client.send(action.encode())
        client.send(username.encode())
        client.send(password.encode())

        response = client.recv(1024).decode()
        status, org_name, org_id = response.split('|', 2)
        return status, org_name, int(org_id)

    except Exception as e:
        return f"Error: {e}", "", 0

# ========================== LOGIN FUNCTIONS ==========================
def login():
    """Handle login logic and panel redirection."""
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter username and password.")
        return

    status, org_name, org_id = send_request("login", username, password)

    main_frame.pack_forget()

    if status == "SUPERADMIN_LOGIN_SUCCESS":
        open_superadmin_panel(root)
    elif status == "LOGIN_SUCCESS":
        open_president_panel(root, False, org_name, org_id)
    elif status == "MEMBER_LOGIN_SUCCESS":
        show_member_fee_panel(root, org_id)
    else:
        messagebox.showinfo("Login Result", status)
        main_frame.pack(fill="both", expand=True)  # Re-show on error

def clear_fields():
    """Clear username and password input fields."""
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

# ========================== LEFT PANEL (LOGIN FORM) ==========================
left_panel = ctk.CTkFrame(main_frame, corner_radius=20, fg_color="#ffffff", width=500)
left_panel.pack(side="left", fill="both", expand=True)

tk.Label(left_panel, text="Login to Your Account", font=("Arial", 24, "bold"), bg="#ffffff").pack(pady=(70, 70))

form_frame = tk.Frame(left_panel, bg="#ffffff")
form_frame.pack(pady=10)

# Username field
tk.Label(form_frame, text="Username", font=("Arial", 12), bg="#ffffff").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_username = ctk.CTkEntry(form_frame, width=300, height=30, font=("Arial", 16))
entry_username.grid(row=1, column=0, padx=10, pady=5, ipady=6)

# Password Label
tk.Label(
    form_frame,
    text="Password",
    font=("Arial", 12),
    bg="#ffffff"
).grid(row=2, column=0, padx=10, pady=5, sticky="w")

# Password Entry (full width)
entry_password = ctk.CTkEntry(
    form_frame,
    width=300,
    height=30,
    font=("Arial", 16),
    show="●"
)
entry_password.grid(row=3, column=0, padx=10, pady=5, ipady=6)

# Toggle button placed on top, inside the entry widget's right side
def toggle_password_visibility():
    if entry_password.cget("show") == "":
        entry_password.configure(show="●")
        btn_toggle_password.configure(text="🙈")
    else:
        entry_password.configure(show="")
        btn_toggle_password.configure(text="👁️")

btn_toggle_password = ctk.CTkButton(
    form_frame,
    text="👁️",
    width=30,
    height=28,
    fg_color="#cccccc",
    hover_color="#bbbbbb",
    command=toggle_password_visibility,
    font=("Arial", 12)
)

# Use .place() to position the button over the entry box, aligned right and centered vertically
btn_toggle_password.place(
    in_=entry_password,
    relx=1.0,  # right edge of entry
    rely=0.5,  # vertical center
    anchor="e",  # anchor east (right side)
    x=-5  # slight padding inside the right edge
)

# Buttons
button_frame = tk.Frame(left_panel, bg="#ffffff")
button_frame.pack(pady=20)

ctk.CTkButton(button_frame, text="Log In", command=login, fg_color="#020325", hover_color="#1a1a40").grid(row=0, column=0, padx=5, ipadx=10)
ctk.CTkButton(button_frame, text="Clear", command=clear_fields, fg_color="#020325", hover_color="#1a1a40").grid(row=0, column=1, padx=5, ipadx=10)

# ========================== RIGHT PANEL (INFO PANEL) ==========================
right_panel = ctk.CTkFrame(main_frame, corner_radius=0, fg_color="#020325", width=500)
right_panel.pack(side="right", fill="both", expand=True)

right_content = tk.Frame(right_panel, bg="#020325")
right_content.place(relx=0.3, rely=0.4, anchor="center")

tk.Label(right_content, text="studentary", font=("Palatino Linotype", 60, "bold"), bg="#020325", fg="white").pack(anchor="w", pady=(0, 1), padx=(20, 0))
tk.Label(right_content, text="Keeping everything in sync.", font=("Arial", 20, "italic"), bg="#020325", fg="white").pack(anchor="w", pady=(0, 1), padx=(22, 0))
tk.Label(
    right_content,
    text="Manage your student organization's data with ease.\nPlease log in to continue.",
    font=("Arial", 14),
    bg="#020325",
    fg="white",
    justify="left",
    wraplength=500
).pack(anchor="w", padx=(24, 0))

entry_username.focus()

# ========================== MAIN ==========================
if __name__ == "__main__":
    threading.Thread(target=server_program, daemon=True).start()
    root.mainloop()