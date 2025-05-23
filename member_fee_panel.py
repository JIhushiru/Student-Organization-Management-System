import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import get_connection

def show_member_fee_panel(root, member_id):
    # Clear root and setup layout
    for widget in root.winfo_children():
        widget.destroy()

    # Title
    title_label = tk.Label(root, text="Your Organizations and Fees", font=("Segoe UI", 20, "bold"))
    title_label.pack(pady=10)

    # Organization information table
    org_columns = ("Org Name", "Active Status", "Semester", "Role", "Committee")
    org_tree = ttk.Treeview(root, columns=org_columns, show="headings", height=5)
    org_tree.pack(fill="x", padx=10, pady=(0, 10))

    for col in org_columns:
        org_tree.heading(col, text=col)
        org_tree.column(col, width=120)

    # Table for paid and unpaid fees
    # For paid fees
    paid_label = tk.Label(root, text="Paid Fees", font=("Segoe UI", 14, "bold"), fg="green")
    paid_label.pack(pady=(10, 0))
    fee_columns = ("Org Name", "Academic Year", "Fee Type", "Amount", "Due Date", "Fee Status")
    paid_tree = ttk.Treeview(root, columns=fee_columns, show="headings")
    paid_tree.pack(fill="x", padx=10, pady=(0, 10))

    for col in fee_columns:
        paid_tree.heading(col, text=col)
        paid_tree.column(col, width=120)

    # For unpaid fees
    unpaid_label = tk.Label(root, text="Unpaid Fees", font=("Segoe UI", 14, "bold"), fg="red")
    unpaid_label.pack(pady=(10, 0))
    unpaid_tree = ttk.Treeview(root, columns=fee_columns, show="headings")
    unpaid_tree.pack(fill="x", padx=10, pady=(0, 10))

    for col in fee_columns:
        unpaid_tree.heading(col, text=col)
        unpaid_tree.column(col, width=120)

    conn = get_connection()
    cur = conn.cursor()

    unpaid_count = 0  # Track if there are unpaid fees

    try:
        # Get all orgs and roles for this member
        cur.execute("""
            SELECT s.org_id, o.org_name, s.role, s.status, s.committee, s.semester, s.academic_year
            FROM SERVES s
            JOIN ORGANIZATION o ON s.org_id = o.org_id
            WHERE s.mem_id = %s
        """, (member_id,))
        orgs = cur.fetchall()

        # Fill the org summary table
        for org in orgs:
            org_id, org_name, role, status, committee, semester, academic_year = org
            org_tree.insert("", "end", values=(org_name, status, semester, role, committee))

        # Fill the fee tables
        for org in orgs:
            org_id, org_name, role, status, committee, semester, academic_year = org
            cur.execute("""
                SELECT fee_type, amount, due_date, status
                FROM FEE
                WHERE mem_id = %s AND org_id = %s
            """, (member_id, org_id))
            fees = cur.fetchall()
            for fee in fees:
                fee_type, amount, due_date, fee_status = fee
                row = (org_name, academic_year, fee_type, amount, due_date, fee_status)
                if fee_status == "Unpaid":
                    unpaid_tree.insert("", "end", values=row)
                    unpaid_count += 1
                elif fee_status == "Paid":
                    paid_tree.insert("", "end", values=row)

        # If there are no unpaid fees, display "none"
        if unpaid_count == 0:
            unpaid_tree.insert("", "end", values=("none", "", "", "", "", ""))

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching fees: {e}")

    finally:
        cur.close()
        conn.close()

    # Back button
    back_button = tk.Button(root, text="Back", command=root.destroy)
    back_button.pack(pady=10)