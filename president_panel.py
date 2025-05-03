import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from db_connection import get_connection
from fee import show_fee_table
from members import show_member_table
from organization import show_organization_table
from serves import show_serves_table

# Establish connection with the database
conn = get_connection()
cur = conn.cursor()

def open_president_panel(root, member_id):
    # Set window title and size
    root.title("President Panel")
    root.geometry("1300x650")

    # Main content area (Initially empty, will be populated later)
    main_area = tk.Frame(root)
    main_area.pack(expand=True, fill="both")

    # Add content to main area (homepage)
    show_homepage(root)

def show_homepage(root):
    # Clear any existing widgets in the root
    for widget in root.winfo_children():
        widget.destroy()

    # Create header for the page
    header = tk.Label(root, text="President Panel - Organization Management",
                      font=("Bell Gothic Std Black", 40, "bold"), fg="#0d0d0d")
    header.pack(pady=5)

    # Create subtext for the page
    subtext = tk.Label(root, text="Manage Members, Fees, and More! Sana All",
                       font=("Bell Gothic Std Light", 14), fg="black")
    subtext.pack(pady=5)

    # Button section for various management features
    buttons = [
        ("Manage Members", "member"),
        ("View Fees", "fee"),
        ("Manage Organizations", "organization"),
        ("Manage Services", "serves"),
    ]
    
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=40)
    
    for text, table in buttons:
        btn = tk.Button(btn_frame, text=text, width=20, height=2,
                        font=("Bell Gothic Std Black", 12, "bold"), bg="#cfd1e3", fg="black",
                        command=lambda t=table: load_table(root, t))
        btn.pack(pady=10)

def load_table(root, table_name):
    # Clear the main content area
    for widget in root.winfo_children():
        widget.destroy()

    # Create the Home button in each table view
    top_nav = tk.Frame(root, bg="#06044d", height=50)
    top_nav.pack(side="top", fill="x")

    home_btn = tk.Button(top_nav, text="Home", command=lambda: show_homepage(root),
                         fg="white", bg="#f0b505", font=("Malgun Gothic", 12), relief="sunken")
    home_btn.pack(side="left", padx=10, pady=10)

    if table_name == "member":
        show_member_table(root,cur)

    elif table_name == "fee":
        show_fee_table(root,cur)

    elif table_name == "organization":
        show_organization_table(root,cur)

    elif table_name == "serves":
        show_serves_table(root,cur)



if __name__ == "__main__":
    root = tk.Tk()
    open_president_panel(root, member_id=1)  # Sample member ID
    root.mainloop()
