import tkinter as tk
from tkinter import ttk, messagebox
from authentication import hash_password
from db_connection import get_connection
from president_panel import open_president_panel
import mariadb

def open_superadmin_panel(root):
    # Tabs
    tab = ttk.Notebook(root)

    # Organizations Tab
    orgs_tab = ttk.Frame(tab)
    tab.add(orgs_tab, text='Organizations')

    def fetch_organizations():
        """Fetch organizations from the database"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT org_id, org_name FROM organization")
        organizations = cur.fetchall()
        conn.close()
        return organizations

    org_button_frame = ttk.Frame(orgs_tab)
    org_button_frame.pack(fill='x', anchor='w', padx=10, pady=10)
    def populate_organization_buttons():
        for widget in org_button_frame.winfo_children():
            widget.destroy()

        try:
            organizations = fetch_organizations()
            for org_id, org_name in organizations:
                btn = ttk.Button(org_button_frame, text=f"Manage: {org_name}",
                                command=lambda oid=org_id, oname=org_name: open_president_panel(root, True, oname, oid))
                btn.pack(pady=2, anchor="w")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load organizations: {e}")

        # Always include "Manage: All orgs"
        all_btn = ttk.Button(org_button_frame, text="Manage: All orgs",
            command=lambda oid=0, oname="All": open_president_panel(root, True, oname, oid))
        all_btn.pack(pady=2, anchor="w")

    populate_organization_buttons()
    
    def show_add_org_form():
        add_window = tk.Toplevel(root)
        add_window.title("Add New Organization")
        add_window.geometry("300x180")

        tk.Label(add_window, text="Organization Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        org_name_entry = tk.Entry(add_window, width=25)
        org_name_entry.grid(row=0, column=1, padx=10)

        tk.Label(add_window, text="Organization Type:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        org_type_entry = tk.Entry(add_window, width=25)
        org_type_entry.grid(row=1, column=1, padx=10)

        def submit_org():
            org_name = org_name_entry.get().strip()
            org_type = org_type_entry.get().strip()

            if not org_name or not org_type:
                messagebox.showwarning("Input Error", "All fields are required.")
                return

            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO ORGANIZATION (org_name, type) VALUES (?, ?)",
                    (org_name, org_type)
                )
                conn.commit()
                messagebox.showinfo("Success", f"'{org_name}' added successfully!")
                add_window.destroy()

                # Refresh org buttons and combobox
                populate_organization_buttons()
                
            except mariadb.Error as e:
                messagebox.showerror("Database Error", f"Failed to add organization:\n{e}")
            finally:
                if cursor: cursor.close()
                if conn: conn.close()


        submit_btn = tk.Button(add_window, text="Add Organization", command=submit_org)
        submit_btn.grid(row=2, column=0, columnspan=2, pady=20)
    btn = ttk.Button(orgs_tab, text="Add Organization",command=show_add_org_form)
    btn.pack(pady=5, anchor="w", padx=10)
    

    # User List Tab
    user_tab = ttk.Frame(tab)
    tab.add(user_tab, text='View Users')
    
    # Create User Tab
    create_tab = ttk.Frame(tab)
    tab.add(create_tab, text='Create User')

    tab.pack(expand=1, fill="both")
    
    list_frame = ttk.Frame(user_tab)
    list_frame.pack(pady=20, fill="both", expand=True)
    
    # Create treeview for users
    tree = ttk.Treeview(list_frame, columns=("ID", "Username", "User Type", "Organization"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("User Type", text="User Type")
    tree.heading("Organization", text="Organization")

    tree.column("ID", width=50)
    tree.column("Username", width=200)
    tree.column("User Type", width=100)
    tree.column("Organization", width=50)

    
    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def load_users():
        # Clear the current tree
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            # Get all users except superadmin
            cur.execute("SELECT user_id, username, user_type, organization FROM userdata WHERE username != 'superadmin'")
            
            for user in cur:
                tree.insert("", "end", values=user)
                
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load users: {e}")
             
             
    
    def delete_user():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a user to delete.")
             
             
            return
        
        user_id = tree.item(selected_item[0], "values")[0]
        username = tree.item(selected_item[0], "values")[1]
        
        # Confirmation Dialog
        confirm_dialog = tk.Toplevel(root)
        confirm_dialog.title("Confirm Deletion")
        confirm_dialog.geometry("300x150")
        confirm_dialog.resizable(False, False)
        confirm_dialog.transient(root)
        confirm_dialog.grab_set()
        
        dialog_x = root.winfo_x() + (root.winfo_width() // 2) - 150
        dialog_y = root.winfo_y() + (root.winfo_height() // 2) - 75
        confirm_dialog.geometry(f"+{dialog_x}+{dialog_y}")
        
        # Dialog content
        message = tk.Label(confirm_dialog, text=f"Are you sure you want to delete user '{username}'?", 
                          pady=15, padx=20)
        message.pack()
        
        # Button frame
        btn_frame = tk.Frame(confirm_dialog)
        btn_frame.pack(pady=10)
        
        # Function for Yes button
        def confirm_delete():
            try:
                conn = get_connection()
                cur = conn.cursor()
                
                cur.execute("DELETE FROM userdata WHERE id = ?", (user_id,))
                conn.commit()
                conn.close()
                
                confirm_dialog.destroy()
                messagebox.showinfo("Success", f"User '{username}' has been deleted.")
                load_users()
            except Exception as e:
                confirm_dialog.destroy()
                messagebox.showerror("Database Error", f"Failed to delete user: {e}")
        
        # Function for No button
        def cancel_delete():
            confirm_dialog.destroy()
        
        # Buttons
        yes_btn = ttk.Button(btn_frame, text="Yes", command=confirm_delete)
        yes_btn.pack(side=tk.LEFT, padx=10)
        
        no_btn = ttk.Button(btn_frame, text="No", command=cancel_delete)
        no_btn.pack(side=tk.LEFT, padx=10)
    
    # Button frame for operations
    btn_frame = ttk.Frame(user_tab)
    btn_frame.pack(pady=10)
    
    # Buttons
    ttk.Button(btn_frame, text="Refresh", command=load_users).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text="Delete User", command=delete_user).grid(row=0, column=1, padx=5)
    
    #Create User tab
    create_frame = ttk.Frame(create_tab)
    create_frame.pack(pady=50)
    

    # Username
    ttk.Label(create_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    new_username = ttk.Entry(create_frame, width=30)
    new_username.grid(row=0, column=1, padx=10, pady=10)
    
    # Password
    ttk.Label(create_frame, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    new_password = ttk.Entry(create_frame, width=30, show="●")
    new_password.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(create_frame, text="Organization:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    organizations = fetch_organizations()
    org_combobox = ttk.Combobox(create_frame, values=["None"] + [org[1] for org in organizations], width=30)
    org_combobox.grid(row=2, column=1, padx=10, pady=10)

    # User Type
    ttk.Label(create_frame, text="User Type:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    user_type_combobox = ttk.Combobox(create_frame, values=["admin", "president"], width=30, state="readonly")
    user_type_combobox.grid(row=3, column=1, padx=10, pady=10)
    user_type_combobox.current(0)  # Default to 'admin'

    def create_user():
        username = new_username.get()
        password = new_password.get()
        organization = org_combobox.get()
        user_type = user_type_combobox.get()
        
        # Validate input
        if not username or not password or not user_type:
            messagebox.showwarning("Input Required", "All fields are required.")
            return

        # If user is an admin, set organization to None
        if user_type == "admin":
            organization = None
            org_combobox.set('')  # Clear the combobox value when admin is selected

        # Check if username already exists
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            # Check if username already exists
            cur.execute("SELECT * FROM userdata WHERE username = ?", (username,))
            if cur.fetchall():
                messagebox.showwarning("Username Exists", "This username already exists.")
                conn.close()
                return

            # Insert new user into userdata table
            hashed_password = hash_password(password)
            cur.execute("INSERT INTO userdata (username, password, user_type, organization) VALUES (?, ?, ?, ?)", (username, hashed_password, user_type, organization))
            conn.commit()

            # Success message
            messagebox.showinfo("Success", f"User '{username}' has been created as an {user_type}.")

            # Clear the input fields
            new_username.delete(0, tk.END)
            new_password.delete(0, tk.END)
            org_combobox.set('')  # Reset combobox
            user_type_combobox.set('admin')  # Reset user type to admin

            load_users()  # Refresh the user list

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to create user: {e}")
            
    
    # Create button
    ttk.Button(create_frame, text="Create User", command=create_user).grid(row=10, column=0, columnspan=2, pady=20)
    close_btn = ttk.Button(root, text="Close Admin Panel", command=root.destroy)
    close_btn.pack(pady=10)
    
    load_users()
    
    def on_close():
        root.grab_release()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_close)
    
    # Wait until this window is closed before returning to the main window
    root.wait_window()