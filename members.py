import tkinter as tk
from tkinter import ttk, messagebox

def show_member_table(root, cur):
    # Top filter and sort UI
    top_frame = tk.Frame(root, pady=10)
    top_frame.pack(fill="x")

    filter_frame = tk.Frame(top_frame)
    filter_frame.pack(side="left", fill="x", expand=True)

    gender_var = tk.StringVar(value="Select")
    batch_var = tk.StringVar()
    degree_var = tk.StringVar()
    year_var = tk.StringVar()
    sort_var = tk.StringVar(value="Sort by")

    tk.Label(filter_frame, text="Gender:").grid(row=0, column=0, padx=5)
    tk.OptionMenu(filter_frame, gender_var, "Select", "M", "F").grid(row=0, column=1, padx=5)
    tk.Label(filter_frame, text="Batch:").grid(row=0, column=2, padx=5)
    tk.Entry(filter_frame, textvariable=batch_var, width=8).grid(row=0, column=3, padx=5)
    tk.Label(filter_frame, text="Degree:").grid(row=0, column=4, padx=5)
    tk.Entry(filter_frame, textvariable=degree_var, width=10).grid(row=0, column=5, padx=5)
    tk.Label(filter_frame, text="Year:").grid(row=0, column=6, padx=5)
    tk.Entry(filter_frame, textvariable=year_var, width=8).grid(row=0, column=7, padx=5)

    def apply_filters():
        filters = {}
        if gender_var.get() != "Select":
            filters["gender"] = gender_var.get()
        if batch_var.get():
            filters["batch"] = batch_var.get()
        if degree_var.get():
            filters["degree"] = degree_var.get()
        if year_var.get():
            filters["year"] = year_var.get()
        refresh_member_table(root, cur, filters, sort_var.get())

    tk.Button(filter_frame, text="Apply Filters", command=apply_filters).grid(row=0, column=8, padx=10)

    # Sort and reset
    right_tools_frame = tk.Frame(top_frame)
    right_tools_frame.pack(side="right")

    tk.Label(right_tools_frame, text="Sort by:").pack(side="left", padx=5)
    sort_options = [
        "mem_id", "first_name", "second_name", "surname", "email",
        "deg_prog", "year_mem", "gender", "batch"
    ]

    def on_sort_select(selected_col):
        if selected_col != "Sort by":
            refresh_member_table(root, cur, {}, selected_col)

    tk.OptionMenu(right_tools_frame, sort_var, *sort_options, command=on_sort_select).pack(side="left")

    def reset_all():
        gender_var.set("Select")
        batch_var.set("")
        degree_var.set("")
        year_var.set("")
        sort_var.set("Sort by")
        refresh_member_table(root, cur, {}, "")

    tk.Button(right_tools_frame, text="🔄", font=("Arial", 12), command=reset_all).pack(side="left", padx=10)

    # Treeview
    tree_frame = tk.Frame(root)
    tree_frame.pack(fill="both", expand=True)

    columns = ("mem_id", "first_name", "second_name", "surname", "email", "deg_prog", "year_mem", "gender", "batch")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    root.tree = tree

    # Buttons frame
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    def delete_selected():
        selected = root.tree.selection()
        if not selected:
            return
        confirm = messagebox.askyesno("Delete", "Are you sure you want to delete the selected member?")
        if not confirm:
            return

        for item in selected:
            values = root.tree.item(item, "values")
            member_id = values[0]
            cur.execute("DELETE FROM fee WHERE mem_id = %s", (member_id,))
            cur.execute("DELETE FROM serves WHERE mem_id = %s", (member_id,))
            cur.execute("DELETE FROM member WHERE mem_id = %s", (member_id,))
        cur.connection.commit()
        refresh_member_table(root, cur, {}, "")

    def edit_selected():
        selected = root.tree.selection()
        if not selected:
            return
        item = selected[0]
        values = root.tree.item(item, "values")
        member_id = values[0]

        cur.execute("SELECT * FROM member WHERE mem_id = %s", (member_id,))
        member = cur.fetchone()

        def save_changes():
            first_name = first_name_var.get()
            second_name = second_name_var.get()
            surname = surname_var.get()
            email = email_var.get()
            deg_prog = deg_prog_var.get()
            year_mem = year_mem_var.get()
            gender = gender_var.get()
            batch = batch_var.get()

            try:
                cur.execute("""
                    UPDATE member SET
                    first_name = %s, second_name = %s, surname = %s,
                    email = %s, deg_prog = %s, year_mem = %s,
                    gender = %s, batch = %s
                    WHERE mem_id = %s
                """, (first_name, second_name, surname, email, deg_prog, year_mem, gender, batch, member_id))
                cur.connection.commit()
                refresh_member_table(root, cur, {}, "")
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Member")
        first_name_var = tk.StringVar(value=member[1])
        second_name_var = tk.StringVar(value=member[2])
        surname_var = tk.StringVar(value=member[3])
        email_var = tk.StringVar(value=member[4])
        deg_prog_var = tk.StringVar(value=member[5])
        year_mem_var = tk.StringVar(value=member[6])
        gender_var = tk.StringVar(value=member[7])
        batch_var = tk.StringVar(value=member[8])

        entries = [
            ("First Name", first_name_var),
            ("Second Name", second_name_var),
            ("Surname", surname_var),
            ("Email", email_var),
            ("Degree Program", deg_prog_var),
            ("Year of Membership", year_mem_var),
            ("Gender", gender_var),
            ("Batch", batch_var)
        ]

        for idx, (label, var) in enumerate(entries):
            tk.Label(edit_window, text=label).grid(row=idx, column=0)
            if label == "Gender":
                tk.OptionMenu(edit_window, var, "M", "F").grid(row=idx, column=1)
            else:
                tk.Entry(edit_window, textvariable=var).grid(row=idx, column=1)

        tk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=len(entries), column=0, columnspan=2, pady=10)

    # Final buttons
    tk.Button(button_frame, text="Edit Selected ✏️", command=edit_selected).pack(side="left", padx=10)
    tk.Button(button_frame, text="Delete Selected 🔴", command=delete_selected, fg="red").pack(side="left", padx=10)

    refresh_member_table(root, cur, {}, "")

def refresh_member_table(root, cur, filters, sort_by):
    query = "SELECT * FROM member WHERE 1=1"
    if filters.get("gender"):
        query += f" AND gender = '{filters['gender']}'"
    if filters.get("batch"):
        query += f" AND batch = {filters['batch']}"
    if filters.get("degree"):
        query += f" AND deg_prog LIKE '%{filters['degree']}%'"
    if filters.get("year"):
        query += f" AND year_mem = {filters['year']}"
    if sort_by and sort_by != "Sort by":
        query += f" ORDER BY {sort_by}"
    cur.execute(query)
    members = cur.fetchall()
    for row in root.tree.get_children():
        root.tree.delete(row)
    for member in members:
        root.tree.insert("", "end", values=member)
