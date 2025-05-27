import tkinter as tk
from tkinter import ttk, messagebox

# COLOR SCHEME AND FONTS
primary_color = "#020325"
button_bg = "#020325"
button_hover_bg = "#1a1a40"
main_area_bg = "#FFFFFF"
title_font = ("Segoe UI", 11)
button_font = ("Segoe UI", 10)
modern_font = ("Arial", 10)

# Style helper
def style_button(btn):
    btn.configure(
        font=button_font,
        relief="flat",
        bg=button_bg,
        fg="white",
        activebackground=button_hover_bg,
        activeforeground="white",
        borderwidth=1,
        highlightthickness=1,
        highlightbackground="#cccccc",
        highlightcolor="#cccccc",
        padx=6,
        pady=3,
        cursor="hand2"
    )

    def on_enter(e):
        btn['background'] = button_hover_bg

    def on_leave(e):
        btn['background'] = button_bg

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


def show_fee_table(root, cur, org_id):
    top_frame = tk.Frame(root, pady=10, bg=main_area_bg)
    top_frame.pack(fill="x")

    filter_frame = tk.Frame(top_frame, bg=main_area_bg)
    filter_frame.pack(side="left", fill="x", expand=True)

    fee_type_var = tk.StringVar(value="Select")
    due_date_var = tk.StringVar()
    min_amount_var = tk.DoubleVar()
    max_amount_var = tk.DoubleVar()
    sort_var = tk.StringVar(value="Sort by")

    tk.Label(filter_frame, text="Fee Type:", bg=main_area_bg).grid(row=0, column=0, padx=5)
    fee_types = get_fee_types(cur)
    fee_type_menu = tk.OptionMenu(filter_frame, fee_type_var, "Select", *fee_types)
    fee_type_menu.config(relief="flat", font=modern_font, bg="white", highlightthickness=1, borderwidth=1)
    fee_type_menu.grid(row=0, column=1, padx=5)

    tk.Label(filter_frame, text="Due Date (YYYY-MM-DD):", bg=main_area_bg).grid(row=0, column=2, padx=5)
    tk.Entry(filter_frame, textvariable=due_date_var, width=12, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="gray").grid(row=0, column=3, padx=5)

    tk.Label(filter_frame, text="Min Amount:", bg=main_area_bg).grid(row=0, column=4, padx=5)
    tk.Entry(filter_frame, textvariable=min_amount_var, width=8, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="gray").grid(row=0, column=5, padx=5)

    tk.Label(filter_frame, text="Max Amount:", bg=main_area_bg).grid(row=0, column=6, padx=5)
    tk.Entry(filter_frame, textvariable=max_amount_var, width=8, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="gray").grid(row=0, column=7, padx=5)

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
        refresh_fee_table(root, cur, filters, sort_var.get(), org_id)

    apply_btn = tk.Button(filter_frame, text="Apply Filters", command=apply_fee_filters)
    apply_btn.grid(row=0, column=8, padx=10)
    style_button(apply_btn)

    # Sort and reset
    right_tools_frame = tk.Frame(top_frame, bg=main_area_bg)
    right_tools_frame.pack(side="right")

    tk.Label(right_tools_frame, text="Sort by:", bg=main_area_bg).pack(side="left", padx=5)

    sort_options = [
        "fee_id", "mem_id", "academic_year_issued", "semester_issued",
        "due_date", "fee_type", "amount", "status", "date_paid"
    ]


    def on_sort_select(selected_col):
        if selected_col != "Sort by":
            filters = {}
            if fee_type_var.get() != "Select":
                filters["fee_type"] = fee_type_var.get()
            if due_date_var.get():
                filters["due_date"] = due_date_var.get()
            if min_amount_var.get():
                filters["min_amount"] = min_amount_var.get()
            if max_amount_var.get():
                filters["max_amount"] = max_amount_var.get()
            refresh_fee_table(root, cur, filters, selected_col, org_id)

    sort_menu = tk.OptionMenu(right_tools_frame, sort_var, *sort_options, command=on_sort_select)
    sort_menu.config(relief="flat", font=modern_font, bg="white", highlightthickness=1, borderwidth=1)
    sort_menu.pack(side="left")

    def reset_all():
        fee_type_var.set("Select")
        due_date_var.set("")
        min_amount_var.set(0.0)
        max_amount_var.set(0.0)
        sort_var.set("Sort by")
        refresh_fee_table(root, cur, {}, "", org_id)

    reset_btn = tk.Button(right_tools_frame, text="🔄", font=modern_font, command=reset_all)
    reset_btn.pack(side="left", padx=10)
    style_button(reset_btn)

    # Treeview
    tree_frame = tk.Frame(root)
    tree_frame.pack(fill="both", expand=True)

    columns = (
        "Fee Id", "Member Id", "Full Name", "Academic Year Issued", "Semester Issued",
        "Due Date", "Fee Type", "Amount (Php)", "Status", "Date Paid"
    )
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Modern.Treeview")
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    # Modern Treeview Style
    style = ttk.Style()
    style.configure("Modern.Treeview", font=modern_font, rowheight=25)
    style.configure("Modern.Treeview.Heading", font=("Arial", 9, "bold"))

    root.tree = tree

    button_frame = tk.Frame(root, bg=main_area_bg)
    button_frame.pack(pady=10)

    def delete_selected():
        selected = root.tree.selection()
        if not selected:
            return
        confirm = messagebox.askyesno("Delete", "Are you sure you want to delete the selected fee?")
        if not confirm:
            return

        for item in selected:
            values = root.tree.item(item, "values")
            fee_id = values[0]
            cur.execute("DELETE FROM fee WHERE fee_id = %s", (fee_id,))

        cur.connection.commit()
        refresh_fee_table(root, cur, {}, "", org_id)

    def edit_selected():
        selected = root.tree.selection()
        if not selected:
            return
        item = selected[0]
        values = root.tree.item(item, "values")
        fee_id = values[0]

        cur.execute("SELECT * FROM fee WHERE fee_id = %s", (fee_id,))
        fee = cur.fetchone()

        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Fee")

        mem_id_var = tk.StringVar(value=fee[1])
        org_id_var = tk.StringVar(value=fee[2])
        academic_year_issued_var = tk.StringVar(value=fee[3])
        semester_issued_var = tk.StringVar(value=fee[4])
        due_date_var = tk.StringVar(value=fee[5])
        fee_type_var = tk.StringVar(value=fee[6])
        amount_var = tk.DoubleVar(value=fee[7])
        status_var = tk.StringVar(value=fee[8])
        date_paid_var = tk.StringVar(value=fee[9])

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
            tk.Entry(edit_window, textvariable=var, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="black").grid(row=idx, column=1)

        def save_changes():
            try:
                cur.execute("""UPDATE fee SET
                        mem_id = %s,
                        org_id = %s,
                        academic_year_issued = %s,
                        semester_issued = %s,
                        due_date = %s,
                        fee_type = %s,
                        amount = %s,
                        status = %s,
                        date_paid = %s
                    WHERE fee_id = %s""", (mem_id_var.get(), org_id_var.get(), academic_year_issued_var.get(),
                    semester_issued_var.get(), due_date_var.get(), fee_type_var.get(),
                    amount_var.get(), status_var.get(), date_paid_var.get(), fee_id))
                cur.connection.commit()
                refresh_fee_table(root, cur, {}, "", org_id)
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        save_btn = tk.Button(edit_window, text="Save Changes", command=save_changes)
        save_btn.grid(row=len(entries), column=0, columnspan=2, pady=10)
        style_button(save_btn)

    def add_fee():
        add_window = tk.Toplevel(root)
        add_window.title("Add Fee")

        mem_id_var = tk.StringVar()
        org_id_var = tk.StringVar()
        academic_year_issued_var = tk.StringVar()
        semester_issued_var = tk.StringVar()
        due_date_var = tk.StringVar()
        fee_type_var = tk.StringVar()
        amount_var = tk.DoubleVar()
        status_var = tk.StringVar()
        date_paid_var = tk.StringVar()

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
            tk.Label(add_window, text=label).grid(row=idx, column=0)
            tk.Entry(add_window, textvariable=var, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="black").grid(row=idx, column=1)

        def save_changes():
            try:
                # If status is 'Unpaid', set date_paid to None (NULL in DB)
                status = status_var.get().strip()
                date_paid = date_paid_var.get().strip()
                if status.lower() == "unpaid" or not date_paid:
                    date_paid = None

                cur.execute("""
                    INSERT INTO FEE(mem_id, org_id, academic_year_issued, semester_issued,
                    due_date, fee_type, amount, status, date_paid)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    mem_id_var.get(), org_id_var.get(), academic_year_issued_var.get(),
                    semester_issued_var.get(), due_date_var.get(), fee_type_var.get(),
                    amount_var.get(), status, date_paid
                ))
                cur.connection.commit()
                refresh_fee_table(root, cur, {}, "", org_id)
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        save_btn = tk.Button(add_window, text="Save Changes", command=save_changes)
        save_btn.grid(row=len(entries), column=0, columnspan=2, pady=10)
        style_button(save_btn)

    add_btn = tk.Button(button_frame, text="Add", command=add_fee)
    add_btn.pack(side="left", padx=10)
    style_button(add_btn)

    edit_btn = tk.Button(button_frame, text="Edit", command=edit_selected)
    edit_btn.pack(side="left", padx=10)
    style_button(edit_btn)

    del_btn = tk.Button(button_frame, text="Delete", command=delete_selected, fg="white")
    del_btn.pack(side="left", padx=10)
    style_button(del_btn)

    refresh_fee_table(root, cur, {}, "", org_id)


def refresh_fee_table(root, cur, filters, sort_by, org_id):
    query = """SELECT 
        fee_id, 
        mem_id, 
        CONCAT(first_name, ' ', surname) AS full_name, 
        academic_year_issued, 
        semester_issued, 
        due_date, 
        fee_type, 
        amount, 
        status, 
        date_paid 
        FROM 
            fee 
        NATURAL JOIN 
            member"""
    
    conditions = []
    params = []

    if org_id != 0:
        conditions.append("org_id = %s")
        params.append(org_id)

    if filters.get("fee_type"):
        conditions.append("fee_type = %s")
        params.append(filters["fee_type"])
    if filters.get("due_date"):
        conditions.append("due_date = %s")
        params.append(filters["due_date"])
    if filters.get("min_amount"):
        conditions.append("amount >= %s")
        params.append(filters["min_amount"])
    if filters.get("max_amount"):
        conditions.append("amount <= %s")
        params.append(filters["max_amount"])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if sort_by and sort_by != "Sort by":
        query += f" ORDER BY {sort_by}"

    cur.execute(query, tuple(params))
    fees = cur.fetchall()

    for row in root.tree.get_children():
        root.tree.delete(row)

    for fee in fees:
        root.tree.insert("", "end", values=fee)


def get_fee_types(cur):
    cur.execute("SELECT DISTINCT fee_type FROM fee")
    return [row[0] for row in cur.fetchall()]