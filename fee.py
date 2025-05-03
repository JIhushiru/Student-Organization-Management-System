import tkinter as tk
from tkinter import ttk

def show_fee_table(root, cur):
    # Wrapper frame for filters + sort/reset
    top_frame = tk.Frame(root, pady=10)
    top_frame.pack(fill="x")

    # Left filter section
    filter_frame = tk.Frame(top_frame)
    filter_frame.pack(side="left", fill="x", expand=True)

    # Variables
    fee_type_var = tk.StringVar(value="Select")
    due_date_var = tk.StringVar()
    min_amount_var = tk.DoubleVar()
    max_amount_var = tk.DoubleVar()
    sort_var = tk.StringVar(value="Sort by")

    # Filters
    tk.Label(filter_frame, text="Fee Type:").grid(row=0, column=0, padx=5)
    fee_types = get_fee_types(cur)
    tk.OptionMenu(filter_frame, fee_type_var, "Select", *fee_types).grid(row=0, column=1, padx=5)

    tk.Label(filter_frame, text="Due Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5)
    tk.Entry(filter_frame, textvariable=due_date_var, width=12).grid(row=0, column=3, padx=5)

    tk.Label(filter_frame, text="Min Amount:").grid(row=0, column=4, padx=5)
    tk.Entry(filter_frame, textvariable=min_amount_var, width=8).grid(row=0, column=5, padx=5)

    tk.Label(filter_frame, text="Max Amount:").grid(row=0, column=6, padx=5)
    tk.Entry(filter_frame, textvariable=max_amount_var, width=8).grid(row=0, column=7, padx=5)

    # Apply Filters
    def apply_fee_filters():
        filters = {}
        if fee_type_var.get() != "Select":
            filters["fee_type"] = fee_type_var.get()
        if due_date_var.get():
            filters["due_date"] = due_date_var.get()
        if min_amount_var.get():
            filters["min_amount"] = min_amount_var.get()
        if max_amount_var.get():
            filters["max_amount"] = max_amount_var.get()
        refresh_fee_table(root, cur, filters, sort_var.get())

    tk.Button(filter_frame, text="Apply Filters", command=apply_fee_filters).grid(row=0, column=8, padx=10)

    # Right tools: Sort + Reset
    right_tools_frame = tk.Frame(top_frame)
    right_tools_frame.pack(side="right")

    tk.Label(right_tools_frame, text="Sort by:").pack(side="left", padx=5)

    # Full fee table columns
    columns = [
        "fee_id", "mem_id", "org_id", "academic_year_issued", "semester_issued",
        "due_date", "fee_type", "amount", "status", "date_paid"
    ]

    def on_sort_select(selected_col):
        if selected_col == "Sort by":
            return
        data = [(root.tree.set(child, selected_col), child) for child in root.tree.get_children()]
        try:
            data.sort(key=lambda x: float(x[0]) if x[0] != '' else 0)
        except ValueError:
            data.sort(key=lambda x: x[0])
        for index, (_, child) in enumerate(data):
            root.tree.move(child, '', index)

    tk.OptionMenu(right_tools_frame, sort_var, *columns, command=on_sort_select).pack(side="left")

    def reset_all():
        fee_type_var.set("Select")
        due_date_var.set("")
        min_amount_var.set(0.0)
        max_amount_var.set(0.0)
        sort_var.set("Sort by")
        refresh_fee_table(root, cur, {},"")

    tk.Button(right_tools_frame, text="🔄", font=("Arial", 12), command=reset_all).pack(side="left", padx=10)

    # Treeview
    tree_frame = tk.Frame(root)
    tree_frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    root.tree = tree  # Save reference

    # Buttons frame
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Add Delete Button
    def delete_selected():
        selected = root.tree.selection()
        if not selected:
            return  # No item selected
        confirm = tk.messagebox.askyesno("Delete", "Are you sure you want to delete the selected member?")
        if not confirm:
            return

        for item in selected:
            values = root.tree.item(item, "values")
            fee_id = values[0]  # Assuming Member id is the first column

            # Execute delete query
            cur.execute("DELETE FROM fee WHERE fee_id = %s", (fee_id,))

        # Commit the change to database
        cur.connection.commit()

        # Refresh table after deletion
        refresh_fee_table(root, cur, {}, "")

    def edit_selected():
        selected = root.tree.selection()
        if not selected:
            return
        item = selected[0]
        values = root.tree.item(item, "values")
        fee_id = values[0]  # Assuming fee_id is the first column

        # Fetch the selected fee's details
        cur.execute("SELECT * FROM fee WHERE fee_id = %s", (fee_id,))
        fee = cur.fetchone()

        def save_changes():
            # Collect updated values from the entry fields
            mem_id = mem_id_var.get()
            org_id = org_id_var.get()
            academic_year_issued = academic_year_issued_var.get()
            semester_issued = semester_issued_var.get()
            due_date = due_date_var.get()
            fee_type = fee_type_var.get()
            amount = amount_var.get()
            status = status_var.get()
            date_paid = date_paid_var.get()

            try:
                cur.execute("""
                    UPDATE fee SET
                        mem_id = %s,
                        org_id = %s,
                        academic_year_issued = %s,
                        semester_issued = %s,
                        due_date = %s,
                        fee_type = %s,
                        amount = %s,
                        status = %s,
                        date_paid = %s
                    WHERE fee_id = %s
                """, (mem_id, org_id, academic_year_issued, semester_issued, due_date, fee_type, amount, status, date_paid, fee_id))
                cur.connection.commit()

                # Refresh the fee table after the update
                refresh_fee_table(root, cur, {}, "")
                edit_window.destroy()
            except Exception as e:
                tk.messagebox.showerror("Error", str(e))

        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Fee")

        # Create Tkinter StringVars to store the fee data
        mem_id_var = tk.StringVar(value=fee[1])
        org_id_var = tk.StringVar(value=fee[2])
        academic_year_issued_var = tk.StringVar(value=fee[3])
        semester_issued_var = tk.StringVar(value=fee[4])
        due_date_var = tk.StringVar(value=fee[5])
        fee_type_var = tk.StringVar(value=fee[6])
        amount_var = tk.DoubleVar(value=fee[7])
        status_var = tk.StringVar(value=fee[8])
        date_paid_var = tk.StringVar(value=fee[9])

        # Entry fields for fee data
        entries = [
            ("Member ID", mem_id_var),
            ("Organization ID", org_id_var),
            ("Academic Year Issued", academic_year_issued_var),
            ("Semester Issued", semester_issued_var),
            ("Due Date (YYYY-MM-DD)", due_date_var),
            ("Fee Type", fee_type_var),
            ("Amount", amount_var),
            ("Status", status_var),
            ("Date Paid (YYYY-MM-DD)", date_paid_var)
        ]

        for idx, (label, var) in enumerate(entries):
            tk.Label(edit_window, text=label).grid(row=idx, column=0)
            tk.Entry(edit_window, textvariable=var).grid(row=idx, column=1)

        tk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=len(entries), column=0, columnspan=2, pady=10)
    # Final buttons
    tk.Button(button_frame, text="Edit Selected ✏️", command=edit_selected).pack(side="left", padx=10)
    tk.Button(button_frame, text="Delete Selected 🔴", command=delete_selected, fg="red").pack(side="left", padx=10)


    refresh_fee_table(root, cur, {},"")  # Initial load


def refresh_fee_table(root, cur, filters, sort_by):
    query = "SELECT * FROM fee WHERE 1=1"
    
    if filters.get("fee_type"):
        query += f" AND fee_type = '{filters['fee_type']}'"
    if filters.get("due_date"):
        query += f" AND due_date = '{filters['due_date']}'"
    if filters.get("min_amount"):
        query += f" AND amount >= {filters['min_amount']}"
    if filters.get("max_amount"):
        query += f" AND amount <= {filters['max_amount']}"

    if sort_by and sort_by != "Sort by":
        query += f" ORDER BY {sort_by}"

    cur.execute(query)
    fees = cur.fetchall()

    for row in root.tree.get_children():
        root.tree.delete(row)

    for fee in fees:
        root.tree.insert("", "end", values=fee)


def get_fee_types(cur):
    cur.execute("SELECT DISTINCT fee_type FROM fee")
    return [row[0] for row in cur.fetchall()]
