import tkinter as tk
import os
import sys
from tkinter import ttk, messagebox
from setup.authentication import hash_password
from setup.db_connection import get_connection
from main_panels.president_panel import show_summary_reports_panel

def show_member_fee_panel(root, member_id, username, return_func=None, admin=None, org_name=None, org_id=None):
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # --- COLOR SCHEME & FONTS ---
    primary_color = "#020325"
    main_area_bg = "#FFFFFF"
    title_font = ("Segoe UI", 16, "bold")

    # --- TOP NAVIGATION BAR ---
    top_nav = tk.Frame(root, bg=primary_color, height=50)
    top_nav.pack_propagate(False)
    top_nav.pack(side="top", fill="x")
    input_text = "Welcome " + username + "!"
    top_nav_title = tk.Label(top_nav, text=input_text, fg="white", bg=primary_color, font=title_font)
    top_nav_title.pack(side="left", padx=15)

    # --- HOME BUTTON (only for presidents) ---
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM serves WHERE mem_id = %s AND role = 'President'", (member_id,))
    is_president = cur.fetchone()[0] > 0
    cur.close()
    conn.close()

    if is_president:
        def go_home():
            for widget in root.winfo_children():
                widget.destroy()
            if return_func:
                return_func(root, admin, org_name, org_id, username)
            else:
                messagebox.showerror("Error", "Cannot return to president panel.")

        home_btn = tk.Button(
            top_nav,
            text="Home",
            command=go_home,
            fg="white",
            bg="#009688",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            bd=0
        )
        home_btn.pack(side="right", pady=10, padx=(0, 5), ipady=5, ipadx=5)


    # --- MAIN AREA FRAME ---
    main_area = tk.Frame(root, bg=main_area_bg)
    main_area.pack(expand=True, fill="both")

 
    title_label = tk.Label(main_area, text="Your Organizations and Fees", font=("Palatino Linotype", 20, "bold"), bg=main_area_bg)
    title_label.pack(pady=10)

    # Organization information table
    org_columns = ("Org Name", "Active Status", "Semester", "Role", "Committee")
    org_tree = ttk.Treeview(main_area, columns=org_columns, show="headings", height=5)
    org_tree.pack(fill="x", padx=10, pady=(0, 10))

    for col in org_columns:
        org_tree.heading(col, text=col)
        org_tree.column(col, width=120)

    # Table for paid and unpaid fees
    # For paid fees
    paid_label = tk.Label(main_area, text="Paid Fees", font=("Arial", 14, "bold"), fg="green", bg=main_area_bg)
    paid_label.pack(pady=(10, 0))
    fee_columns = ("Org Name", "Academic Year", "Fee Type", "Amount", "Due Date", "Fee Status")
    paid_tree = ttk.Treeview(main_area, columns=fee_columns, show="headings")
    paid_tree.pack(fill="x", padx=10, pady=(0, 10))

    for col in fee_columns:
        paid_tree.heading(col, text=col)
        paid_tree.column(col, width=120)

    # For unpaid fees
    unpaid_label = tk.Label(main_area, text="Unpaid Fees", font=("Arial", 14, "bold"), fg="red", bg=main_area_bg)
    unpaid_label.pack(pady=(10, 0))
    unpaid_tree = ttk.Treeview(main_area, columns=fee_columns, show="headings")
    unpaid_tree.pack(fill="x", padx=10, pady=(0, 10))

    for col in fee_columns:
        unpaid_tree.heading(col, text=col)
        unpaid_tree.column(col, width=120)

    conn = get_connection()
    cur = conn.cursor()

    unpaid_count = 0

    try:
        cur.execute("""
            SELECT s.org_id, o.org_name, s.role, s.status, s.committee, s.semester, s.academic_year
            FROM SERVES s
            JOIN ORGANIZATION o ON s.org_id = o.org_id JOIN userdata u on s.mem_id = u.mem_id 
            WHERE u.username = %s
        """, (username,))
        orgs = cur.fetchall()

        for org in orgs:
            org_id, org_name, role, status, committee, semester, academic_year = org
            org_tree.insert("", "end", values=(org_name, status, semester, role, committee))

        for org in orgs:
            org_id, org_name, role, status, committee, semester, academic_year = org
            cur.execute("""
                SELECT f.fee_type, f.amount, f.due_date, f.status
                FROM FEE f
                JOIN userdata u ON f.mem_id = u.mem_id
                WHERE u.username= %s AND f.org_id = %s
            """, (username, org_id))
            fees = cur.fetchall()
            for fee in fees:
                fee_type, amount, due_date, fee_status = fee
                row = (org_name, academic_year, fee_type, amount, due_date, fee_status)
                if fee_status == "Unpaid":
                    unpaid_tree.insert("", "end", values=row)
                    unpaid_count += 1
                elif fee_status == "Paid":
                    paid_tree.insert("", "end", values=row)

        if unpaid_count == 0:
            unpaid_tree.insert("", "end", values=("none", "", "", "", "", ""))

    except ImportError as e:
        messagebox.showerror("Error", f"An error occurred while fetching fees: {e}")

    finally:
        cur.close()
        conn.close()

    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            root.destroy()
            os.execl(sys.executable, sys.executable, *sys.argv)

    def open_edit_account_window():
        edit_win = tk.Toplevel(root)
        edit_win.title("Edit Account")
        edit_win.geometry("300x200")
        edit_win.grab_set()

        tk.Label(edit_win, text="New Username:").pack(pady=(10, 0))
        new_username_entry = tk.Entry(edit_win, width=30)
        new_username_entry.pack(pady=(0, 10))

        tk.Label(edit_win, text="New Password:").pack()
        new_password_entry = tk.Entry(edit_win, width=30, show="*")
        new_password_entry.pack(pady=(0, 10))

        def update_account():
            new_username = new_username_entry.get().strip()
            new_password = hash_password(new_password_entry.get().strip())

            if not new_username or not new_password:
                messagebox.showerror("Error", "Both fields are required.")
                return

            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    UPDATE userdata
                    SET username = %s, password = %s
                    WHERE mem_id = %s
                """, (new_username, new_password, member_id))
                conn.commit()
                cur.close()
                conn.close()

                messagebox.showinfo("Success", "Account updated successfully.")
                edit_win.destroy()
                # Refresh the panel with the new username
                show_member_fee_panel(root, member_id, new_username)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update account: {e}")

        save_btn = tk.Button(edit_win, text="Save Changes", command=update_account, bg="#2980b9", fg="white")
        save_btn.pack(pady=10)

    # --- Add Buttons to Top Nav ---

    logout_button = tk.Button(top_nav, text="Log Out", command=logout, fg="white", bg="#c0392b", font=("Segoe UI", 12), relief="flat", bd=0)
    logout_button.pack(side="right", pady=10, padx=(5, 10), ipady=5, ipadx=5)
    edit_btn = tk.Button(top_nav, text="Edit Account", command=open_edit_account_window, fg="white", bg="#c0392b", font=("Segoe UI", 12), relief="flat", bd=0)
    edit_btn.pack(side="right", pady=10, padx=(0, 5), ipady=5, ipadx=5)

    def refresh_panel():
        show_member_fee_panel(root, member_id, username, return_func, admin, org_name, org_id)

    refresh_btn = tk.Button(
        top_nav,
        text="Refresh",
        command=refresh_panel,
        fg="white",
        bg="#2980b9",
        font=("Segoe UI", 12, "bold"),
        relief="flat",
        bd=0
    )
    refresh_btn.pack(side="right", pady=10, padx=(0, 5), ipady=5, ipadx=5)

