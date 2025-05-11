import tkinter as tk
from tkinter import ttk, messagebox
from authentication import hash_password
from db_connection import get_connection
from president_panel import open_president_panel

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

    def populate_organization_buttons():
        try:
            organizations = fetch_organizations()
            for org_id, org_name in organizations:
                btn = ttk.Button(orgs_tab, text=f"Manage: {org_name}",
                                command=lambda oid=org_id, oname=org_name: open_president_panel(root, oid, oname))
                btn.pack(pady=5, anchor="w", padx=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load organizations: {e}")

    populate_organization_buttons()

    
    # User List Tab
    user_tab = ttk.Frame(tab)
    tab.add(user_tab, text='User Management')
    
    # Create User Tab
    create_tab = ttk.Frame(tab)
    tab.add(create_tab, text='Create User')

    autocreate_tab = ttk.Frame(tab)
    tab.add(autocreate_tab, text='Autocreate User')

    tab.pack(expand=1, fill="both")
    
    list_frame = ttk.Frame(user_tab)
    list_frame.pack(pady=20, fill="both", expand=True)
    
    # Create treeview for users
    tree = ttk.Treeview(list_frame, columns=("ID", "Username", "Member Id", "Org"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Member Id", text="Member ID")
    # tree.heading("Org", text="Username")
    tree.column("ID", width=50)
    tree.column("Username", width=200)
    tree.column("Member Id", width=50)
    # tree.column("Org", width=200)
    
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
            cur.execute("SELECT username, organization FROM userdata WHERE username != 'superadmin'")
            
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
    
    def autocreate_user():
        organization = org_combobox_autocreate.get()

        # Validate input
        if not organization:
            messagebox.showwarning("Input Required", "Organization is required.")
            return

        try:
            conn = get_connection()
            cur = conn.cursor()

            # Get the org_id for the selected organization
            cur.execute("SELECT org_id FROM organization WHERE org_name = ?", (organization,))
            org_id = cur.fetchone()
            
            if not org_id:
                messagebox.showwarning("Invalid Organization", "Organization does not exist.")
                conn.close()
                return
            
            org_id = org_id[0] 
            
            # Get the mem_ids for members associated with the selected organization
            cur.execute("""
                SELECT m.mem_id, m.deg_prog 
                FROM member m
                JOIN serves s ON m.mem_id = s.mem_id
                WHERE s.org_id = ?
            """, (org_id,))
            
            mem_ids = cur.fetchall()

            
            # Iterate over the mem_ids and check if they already have userdata
            for mem_id, deg_prog in mem_ids:
                # Check if user already exists in userdata
                cur.execute("SELECT * FROM userdata WHERE mem_id = ?", (mem_id,))
                existing_user = cur.fetchone()
                
                if not existing_user:  
                    username = f"{mem_id}_{deg_prog}"
                    cur.execute("SELECT * FROM userdata WHERE username = ?", (username,))
                    if cur.fetchall():
                        messagebox.showwarning("Username Exists", f"Username '{username}' already exists.")
                        continue  # Skip if the username already exists in userdata
                    
                    # Default password is "pass"
                    hashed_password = hash_password("pass")

                    # Insert the new user into userdata table
                    cur.execute("INSERT INTO userdata (username, password, mem_id) VALUES (?, ?, ?)", (username, hashed_password, mem_id))
                    conn.commit()

                    messagebox.showinfo("Success", f"User '{username}' has been created.")

            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to autocreate user: {e}")


    # Autocreate User Tab
    autocreate_frame = ttk.Frame(autocreate_tab)
    autocreate_frame.pack(pady=50)
    
    # Organization Combobox for Autocreate
    ttk.Label(autocreate_frame, text="Organization:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    organizations = fetch_organizations()
    org_combobox_autocreate = ttk.Combobox(autocreate_frame, values=[org[1] for org in organizations], width=30)
    org_combobox_autocreate.grid(row=0, column=1, padx=10, pady=10)

    ttk.Button(autocreate_frame, text="Autocreate User", command=autocreate_user).grid(row=1, column=0, columnspan=2, pady=20)

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
    org_combobox = ttk.Combobox(create_frame, values=[org[1] for org in organizations], width=30)
    org_combobox.grid(row=2, column=1, padx=10, pady=10)


    ttk.Label(create_frame, text="Role:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    roles = ["President", "Vice President", "Treasurer", "Member", "Secretary", "Treasurer", "Committee Head", "Alumni"] 
    role_combobox = ttk.Combobox(create_frame, values=roles, width=30)
    role_combobox.grid(row=3, column=1, padx=10, pady=10)

    ttk.Label(create_frame, text="Semester:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
    semesters = ["1st", "2nd", "Midyear"]
    semester_combobox = ttk.Combobox(create_frame, values=semesters, width=30)
    semester_combobox.grid(row=4, column=1, padx=10, pady=10)


    ttk.Label(create_frame, text="Academic Year:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
    acadyears = [f"202{i}-202{i+1}" for i in range(4)]
    academic_year_combobox = ttk.Combobox(create_frame, values=acadyears, width=30)
    academic_year_combobox.grid(row=5, column=1, padx=10, pady=10)


    ttk.Label(create_frame, text="Degree Program:").grid(row=6, column=0, padx=10, pady=10, sticky="e")
    dp = ["BSAM","BSSTAT","BSCS"]
    deg_prog_combobox = ttk.Combobox(create_frame, values =dp,width=30)
    deg_prog_combobox.grid(row=6, column=1, padx=10, pady=10)

    ttk.Label(create_frame, text="Gender:").grid(row=7, column=0, padx=10, pady=10, sticky="e")
    gender = ["M", "F"]
    gender_combobox = ttk.Combobox(create_frame, values =gender,width=30)
    gender_combobox.grid(row=7, column=1, padx=10, pady=10)

    ttk.Label(create_frame, text="Batch:").grid(row=8, column=0, padx=10, pady=10, sticky="e")
    batch = [i + 1 for i in range(2000,2030)]
    batch_combobox = ttk.Combobox(create_frame, values =batch,width=30)
    batch_combobox.grid(row=8, column=1, padx=10, pady=10)

    def create_user():
        username = new_username.get()
        password = new_password.get()
        organization = org_combobox.get()
        role = role_combobox.get()
        semester = semester_combobox.get()
        academic_year = academic_year_combobox.get()
        deg_prog = deg_prog_combobox.get()
        gender = gender_combobox.get()
        batch = batch_combobox.get()
        
        # Validate input
        if not username or not password or not organization or not role or not semester or not academic_year:
            messagebox.showwarning("Input Required", "All fields are required.")
            return
        
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
            

            cur.execute("SELECT MAX(mem_id) FROM member")
            max_mem_id = cur.fetchone()[0]
            new_mem_id = max_mem_id + 1 if max_mem_id is not None else 1

            cur.execute("""
                INSERT INTO member (mem_id, deg_prog, gender, batch) VALUES (?, ?, ? , ?)
            """, (new_mem_id, deg_prog, gender, batch ))
            conn.commit()

            # Insert new user into userdata table
            hashed_password = hash_password(password)
            cur.execute("INSERT INTO userdata (username, password, mem_id) VALUES (?, ?, ?)", (username, hashed_password, new_mem_id))
            conn.commit()

            # Fetch org_id from the organization selected
            org_id = None
            for org in organizations:
                if org[1] == organization:
                    org_id = org[0]
                    break
            # Fetch org_id from the organization table
            cur.execute("SELECT org_id FROM organization WHERE org_name = ?", (organization,))
            org_id_row = cur.fetchone()

            if org_id_row:
                org_id = org_id_row[0] 
                print(new_mem_id, org_id, organization, role, "Active", semester, academic_year)
                try:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS president_panel (
                            mem_id INT,
                            org_id INT,
                            org_name VARCHAR(255),
                            role VARCHAR(255),
                            status VARCHAR(255),
                            semester VARCHAR(255),
                            academic_year VARCHAR(255),
                            PRIMARY KEY(mem_id, org_id)
                        )
                    """)
                    conn.commit()

                    # Insert data into 'president_panel' if the role is "President"
                    if role == "President":
                        cur.execute("""
                            INSERT INTO president_panel (mem_id, org_id, org_name, role, status, semester, academic_year)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (new_mem_id, org_id, organization, role, "Active", semester, academic_year))
                        conn.commit()

                except Exception as e:
                    print(f"Error occurred: {e}")

            else:
                print(f"Organization {organization} not found in the database.")

            # Insert the new user into serves table
            cur.execute("""
                INSERT INTO serves (mem_id, org_id, role, semester, academic_year)
                VALUES (?, ?, ?, ?, ?)
            """, (new_mem_id, org_id, role, semester, academic_year))
            conn.commit()
            conn.close()


            # Success message
            messagebox.showinfo("Success", f"User '{username}' has been created and assigned to '{organization}' as {role}.")

            
            # Clear the input fields
            new_username.delete(0, tk.END)
            new_password.delete(0, tk.END)
            org_combobox.delete(0, tk.END)
            role_combobox.delete(0, tk.END)
            semester_combobox.delete(0, tk.END)
            academic_year_combobox.delete(0, tk.END)
            deg_prog_combobox.delete(0, tk.END)
            gender_combobox.delete(0, tk.END)
            batch_combobox.delete(0,tk.END)

            load_users()  # Refresh the user list (if you have a function to load users)

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