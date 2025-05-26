"""Imports"""
from tkinter import messagebox
import customtkinter as ctk
import mariadb
from db_connection import get_connection
from authentication import hash_password
from president_panel import open_president_panel

BUTTON_COLOR = "#020325"
BUTTON_TEXT_COLOR = "white"
TITLE_FONT = ("Arial", 12, "bold")
ITEMS_PER_PAGE = 16

def open_superadmin_panel(root):
    """Load panel for admin"""
    # ----------------- Window -------------------
    root.title("Admin View")
    root.geometry("1300x650")
    root.configure(fg_color="white")

    # ------------------- Header ----------------------
    # Header Frame
    header_frame = ctk.CTkFrame(root, fg_color="#020325")
    header_frame.pack(fill="x")

    # Header Label
    header = ctk.CTkLabel(
        header_frame,
        text="ORGANIZATIONS DASHBOARD",
        font=("Palatino Linotype", 40, "bold"),
        text_color="white",
        anchor="center"
    )
    header.pack(pady=3)

    # ------------------------ Sidebar --------------------
    main_frame = ctk.CTkFrame(root, fg_color="white")
    main_frame.pack(fill="both", expand=True)

    sidebar_frame = ctk.CTkFrame(main_frame, width=200, fg_color="#f0f0f0")
    sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)

    content_frame = ctk.CTkFrame(main_frame, fg_color="white")
    content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Add organization function
    def show_add_org_form():
        add_window = ctk.CTkToplevel(root)
        add_window.attributes('-topmost', True)
        add_window.title("Add New Organization")
        add_window.geometry("350x150")
        add_window.configure(fg_color="white")

        # Center the window on screen
        add_window.update_idletasks()
        root.update_idletasks()
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        width = 350
        height = 150

        x = root_x + (root_width // 2) - (width // 2)
        y = root_y + (root_height // 2) - (height // 2)

        add_window.geometry(f"{width}x{height}+{x}+{y}")

        form_frame = ctk.CTkFrame(add_window, fg_color="white")
        form_frame.pack(padx=10, pady=10)

        ctk.CTkLabel(form_frame,
            text="Organization Name: ",
            font=("Arial", 12),
            text_color="black").grid(row=0, column=0, sticky="w", pady=5
        )
        org_name_entry = ctk.CTkEntry(form_frame, width=200)
        org_name_entry.grid(row=0, column=1, pady=5)

        ctk.CTkLabel(form_frame,
            text="Organization Type: ",
            font=("Arial", 12),
            text_color="black").grid(row=1, column=0, sticky="w", pady=5
        )
        org_type_entry = ctk.CTkEntry(form_frame, width=200)
        org_type_entry.grid(row=1, column=1, pady=5)

        def submit_org():
            org_name = org_name_entry.get().strip()
            org_type = org_type_entry.get().strip()
            if not org_name or not org_type:
                messagebox.showwarning("Input Error", "All fields are required.")
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                        INSERT INTO ORGANIZATION (org_name, type) VALUES (?, ?)
                    """,
                    (org_name, org_type)
                )
                conn.commit()
                messagebox.showinfo("Success", f"'{org_name}' added successfully!")
                add_window.destroy()
                refresh_data()
            except mariadb.Error as e:
                messagebox.showerror("Database Error", f"Failed to add organization:\n{e}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        btn_submit = ctk.CTkButton(
            form_frame,
            text="Submit",
            command=submit_org,
            fg_color="#020325",
            hover_color="#1a1a40",
            text_color="white"
        )
        btn_submit.grid(row=2, column=0, columnspan=2, pady=15)

    # ------------------------------ Organization Functions----------------------------
    def show_delete_org_dialog():
        delete_window = ctk.CTkToplevel(root)
        delete_window.attributes('-topmost', True)
        delete_window.title("Delete Organization")
        delete_window.geometry("400x180")
        delete_window.configure(fg_color="white")

        # Center the window on screen
        delete_window.update_idletasks()
        root.update_idletasks()
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        width = 400
        height = 180

        x = root_x + (root_width // 2) - (width // 2)
        y = root_y + (root_height // 2) - (height // 2)

        delete_window.geometry(f"{width}x{height}+{x}+{y}")

        ctk.CTkLabel(delete_window,
            text="Select an organization to delete:",
            font=("Arial", 14)).pack(pady=10)

        org_var = ctk.StringVar()
        org_dropdown = ctk.CTkComboBox(delete_window,
            variable=org_var,
            width=300,
            values=[f"{name} (ID: {oid})" for oid, name in organizations]
        )
        org_dropdown.pack(pady=5)

        def delete_selected():
            selected = org_var.get()
            if not selected:
                messagebox.showwarning("Selection Error",
                    "Please select an organization to delete.")
                return
            org_id = int(selected.split("ID: ")[1].rstrip(")"))
            confirm = messagebox.askyesno("Confirm Delete",
                "Are you sure you want to delete this organization?",
                 parent=delete_window)
            if confirm:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM fee WHERE org_id = ?", (org_id,))
                    cursor.execute("DELETE FROM serves WHERE org_id = ?", (org_id,))
                    cursor.execute("DELETE FROM organization WHERE org_id = ?", (org_id,))
                    conn.commit()
                    messagebox.showinfo("Deleted", "Organization deleted successfully.", parent=delete_window)
                    delete_window.destroy()
                    refresh_data()
                except mariadb.Error as e:
                    messagebox.showerror("Database Error", f"Failed to delete organization:\n{e}")
                finally:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()

        ctk.CTkButton(delete_window,
            text="Delete",
            command=delete_selected,
            fg_color="#c0392b",hover_color="#1a1a40").pack(pady=10)
    # ------------------------------ User Functions----------------------------
    # Add user function
    def show_add_user_form():
        add_window = ctk.CTkToplevel(root)
        add_window.attributes('-topmost', True)
        add_window.title("Add New User")
        add_window.geometry("350x150")
        add_window.configure(fg_color="white")

        # Center the window on screen
        add_window.update_idletasks()
        root.update_idletasks()
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        width = 325
        height = 225

        x = root_x + (root_width // 2) - (width // 2)
        y = root_y + (root_height // 2) - (height // 2)

        add_window.geometry(f"{width}x{height}+{x}+{y}")

        form_frame = ctk.CTkFrame(add_window, fg_color="white")
        form_frame.pack(padx=10, pady=10)

        ctk.CTkLabel(form_frame,
            text="Username: ",
            font=("Arial", 12),
            text_color="black").grid(row=0, column=0, sticky="w", pady=0
        )
        username_entry = ctk.CTkEntry(form_frame, width=200)
        username_entry.grid(row=0, column=1, pady=0)

        ctk.CTkLabel(form_frame,
            text="Password: ",
            font=("Arial", 12),
            text_color="black").grid(row=1, column=0, sticky="w", pady=0
        )
        pass_entry = ctk.CTkEntry(form_frame, width=200)
        pass_entry.grid(row=1, column=1, pady=5)

        ctk.CTkLabel(form_frame,
            text="User Type: ",
            font=("Arial", 12),
            text_color="black").grid(row=2, column=0, sticky="w", pady=2
        )
        type_entry = ctk.CTkEntry(form_frame, width=200)
        type_entry.grid(row=2, column=1, pady=5)

        ctk.CTkLabel(form_frame,
            text="Organization: ",
            font=("Arial", 12),
            text_color="black").grid(row=3, column=0, sticky="w", pady=2
        )
        org_entry = ctk.CTkEntry(form_frame, width=200)
        org_entry.grid(row=3, column=1, pady=5)

        def submit_user():
            username = username_entry.get().strip()
            password = hash_password(pass_entry.get().strip())
            user_type = type_entry.get().strip()
            organization = org_entry.get().strip()

            if not username or not password or not organization:
                messagebox.showwarning("Input Error", "All fields are required.")
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                        INSERT INTO userdata (username, password, user_type, organization) VALUES (?, ?, ?, ?)
                    """,
                    (username, password, user_type, organization)
                )
                conn.commit()
                messagebox.showinfo("Success", f"'{username}' added successfully!")
                add_window.destroy()
                display_users()
            except mariadb.Error as e:
                messagebox.showerror("Database Error", f"Failed to add organization:\n{e}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        btn_submit = ctk.CTkButton(
            form_frame,
            text="Submit",
            command=submit_user,
            fg_color="#020325",
            hover_color="#1a1a40",
            text_color="white"
        )
        btn_submit.grid(row=5, column=0, columnspan=2, pady=15)

    def load_users():
        try:
            conn = get_connection()
            cur = conn.cursor()
            # Fetch users except superadmin
            cur.execute("""SELECT user_id,
                username, 
                user_type, 
                organization 
                FROM userdata 
                WHERE username != 'superadmin'
            """)
            users = cur.fetchall()
            cur.close()
            conn.close()
            return users
        except mariadb.Error as e:
            messagebox.showerror("Database Error", f"Failed to load users: {e}")
            return []

    def display_users():
        users = load_users()
        # Clear existing widgets
        for widget in users_container.winfo_children():
            widget.destroy()

        if not users:
            ctk.CTkLabel(users_container,
                text="No users found",
                font=("Arial", 10),
                text_color="gray").pack()
            return

        for _, username, user_type, _ in users:
            # Create a button or label for each user, customize as needed
            user_text = f"{username} ({user_type})"
            ctk.CTkLabel(users_container,
                text=user_text,
                font=("Arial", 12),
                anchor="w").pack(padx=0, pady=0)

    # ------------------------------ User Delete Function ----------------------------
    def show_delete_user_dialog():
        delete_window = ctk.CTkToplevel(root)
        delete_window.attributes('-topmost', True)
        delete_window.title("Delete User")
        delete_window.geometry("400x180")
        delete_window.configure(fg_color="white")

        # Center the window on screen
        delete_window.update_idletasks()
        root.update_idletasks()
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        width = 400
        height = 180

        x = root_x + (root_width // 2) - (width // 2)
        y = root_y + (root_height // 2) - (height // 2)

        delete_window.geometry(f"{width}x{height}+{x}+{y}")

        ctk.CTkLabel(delete_window,
            text="Select a user to delete:",
            font=("Arial", 14)).pack(pady=10)

        # Load users excluding superadmin
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username FROM userdata WHERE username != 'superadmin'")
            users = cursor.fetchall()
        except mariadb.Error as e:
            messagebox.showerror("Database Error", f"Failed to load users:\n{e}")
            delete_window.destroy()
            return
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        user_var = ctk.StringVar()
        user_dropdown = ctk.CTkComboBox(delete_window,
            variable=user_var,
            width=300,
            values=[f"{username} (ID: {uid})" for uid, username in users]
        )
        user_dropdown.pack(pady=5)

        def delete_selected_user():
            selected = user_var.get()
            if not selected:
                messagebox.showwarning("Selection Error", "Please select a user to delete.")
                return
            user_id = int(selected.split("ID: ")[1].rstrip(")"))
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?",
                parent=delete_window)
            if confirm:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM userdata WHERE user_id = ?", (user_id,))
                    conn.commit()
                    messagebox.showinfo("Deleted", "User deleted successfully.", parent=delete_window)
                    delete_window.destroy()
                    display_users()
                except mariadb.Error as e:
                    messagebox.showerror("Database Error", f"Failed to delete user:\n{e}")
                finally:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()

        ctk.CTkButton(delete_window,
            text="Delete",
            command=delete_selected_user,
            fg_color="#c0392b",
            hover_color="#1a1a40").pack(pady=10)

    # ----------------------- Organization Buttons ---------------------------
    ctk.CTkButton(sidebar_frame,
        text="Add Organization",
        command=show_add_org_form,
        hover_color="#1a1a40",
        fg_color=BUTTON_COLOR,
        text_color=BUTTON_TEXT_COLOR).pack(pady=(10, 3), padx=15)
    ctk.CTkButton(sidebar_frame,
        text="All Organizations",
        command=lambda: open_president_panel(root, True, "All", 0),
        hover_color="#1a1a40",
        fg_color=BUTTON_COLOR,
        text_color=BUTTON_TEXT_COLOR).pack(pady = 3, padx = 15)

    ctk.CTkButton(sidebar_frame,
        text="Delete Organization",
        command=show_delete_org_dialog,
        hover_color="#c33f31",
        fg_color="#942d22",
        text_color="white").pack(pady = 3, padx = 15)

    ctk.CTkLabel(sidebar_frame,
        text="___________________",
        font=("Arial", 12),
        text_color="black",
        anchor="center",
        justify="center"
    ).pack(fill="x", pady=(0, 1))

    ctk.CTkLabel(sidebar_frame,
        text="Users",
        font=("Arial", 12, "bold"),
        text_color="black",
        anchor="center",
        justify="center"
    ).pack(fill="x", pady=0)

     # ---------------------------------- User buttons ----------------------------------------
    users_container = ctk.CTkScrollableFrame(sidebar_frame, fg_color="#f0f0f0", width=150)
    users_container.pack(pady=0, padx=0)

    display_users()

    ctk.CTkButton(sidebar_frame,
        text="Create User",
        command=show_add_user_form,
        hover_color="#1a1a40",
        fg_color=BUTTON_COLOR,
        text_color=BUTTON_TEXT_COLOR).pack(pady = (1,3), padx = 15)
    
    ctk.CTkButton(sidebar_frame,
        text="Delete User",
        command=show_delete_user_dialog,
        hover_color="#c33f31",
        fg_color="#942d22",
        text_color="white").pack(pady=3, padx=15)
    
    # -------------------------------- Organization Grid --------------------------------
    ctk.CTkLabel(content_frame,
        text="Select an organization:",
        font=("Arial", 20, "bold"),
        text_color="black",
        anchor="center",
        justify="center"
    ).pack(fill="x", pady=(0, 10))

    org_frame = ctk.CTkFrame(content_frame, fg_color="white")
    org_frame.pack(fill="both", expand=True)

    pagination_frame = ctk.CTkFrame(content_frame, fg_color="white")
    pagination_frame.pack(pady=5)

    organizations = []
    current_page = [0]

    def fetch_organizations():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT org_id, org_name FROM organization ORDER BY org_name ASC")
        orgs = cur.fetchall()
        conn.close()
        return orgs

    def set_page(page_num):
        current_page[0] = page_num
        populate_organization_buttons()

    def refresh_data():
        nonlocal organizations
        organizations = fetch_organizations()
        set_page(0)

    def populate_organization_buttons():
        for widget in org_frame.winfo_children():
            widget.destroy()
        for widget in pagination_frame.winfo_children():
            widget.destroy()

        if not organizations:
            return

        total_orgs = len(organizations)
        total_pages = (total_orgs + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        page = current_page[0]

        start_index = page * ITEMS_PER_PAGE
        end_index = min(start_index + ITEMS_PER_PAGE, total_orgs)
        current_orgs = organizations[start_index:end_index]

        cols = 4
        for index, (org_id, org_name) in enumerate(current_orgs):
            row, col = divmod(index, cols)
            btn = ctk.CTkButton(org_frame,
                text=org_name,
                font=("Arial", 20, "bold"),
                command=lambda oid=org_id,
                oname=org_name: open_president_panel(root, True, oname, oid),
                fg_color=BUTTON_COLOR,
                text_color=BUTTON_TEXT_COLOR,
                width=100, height=100,
                corner_radius=10,
                hover_color="#1a1a40"
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        for c in range(cols):
            org_frame.grid_columnconfigure(c, weight=1)

        if total_pages > 1:
            if page > 0:
                ctk.CTkButton(pagination_frame,
                    text="Previous",
                    command=lambda: set_page(page - 1),
                    hover_color="#1a1a40",
                    fg_color=BUTTON_COLOR,
                    text_color=BUTTON_TEXT_COLOR).pack(side="left", padx=5)
            ctk.CTkLabel(pagination_frame,
                    text=f"Page {page + 1} of {total_pages}",
                    font=("Arial", 10)).pack(side="left", padx=10)
            if page < total_pages - 1:
                ctk.CTkButton(pagination_frame,
                    text="Next",
                    command=lambda: set_page(page + 1),
                    hover_color="#1a1a40",
                    fg_color=BUTTON_COLOR,
                    text_color=BUTTON_TEXT_COLOR).pack(side="left", padx=5)

    # Initial Load
    refresh_data()

    def on_close():
        root.grab_release()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.wait_window()
