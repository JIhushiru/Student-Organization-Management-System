import tkinter as tk
from tkinter import ttk

def show_serves_table(root, cur):
    # Frame for filters and tools
    top_frame = tk.Frame(root, pady=10)
    top_frame.pack(fill="x")

    filter_frame = tk.Frame(top_frame)
    filter_frame.pack(side="left", fill="x", expand=True)

    mem_id_var = tk.StringVar()
    org_id_var = tk.StringVar()
    role_var = tk.StringVar()
    status_var = tk.StringVar()
    committee_var = tk.StringVar()
    semester_var = tk.StringVar(value="Select")
    academic_year_var = tk.StringVar()
    sort_var = tk.StringVar(value="Sort by")

    # Row 0
    tk.Label(filter_frame, text="Member ID:").grid(row=0, column=0, padx=5)
    tk.Entry(filter_frame, textvariable=mem_id_var, width=10).grid(row=0, column=1, padx=5)

    tk.Label(filter_frame, text="Organization ID:").grid(row=0, column=2, padx=5)
    tk.Entry(filter_frame, textvariable=org_id_var, width=10).grid(row=0, column=3, padx=5)

    tk.Label(filter_frame, text="Role:").grid(row=0, column=4, padx=5)
    tk.Entry(filter_frame, textvariable=role_var, width=15).grid(row=0, column=5, padx=5)

    tk.Label(filter_frame, text="Status:").grid(row=0, column=6, padx=5)
    tk.Entry(filter_frame, textvariable=status_var, width=10).grid(row=0, column=7, padx=5)

    tk.Label(filter_frame, text="Committee:").grid(row=0, column=8, padx=5)
    tk.Entry(filter_frame, textvariable=committee_var, width=15).grid(row=0, column=9, padx=5)

    # Row 1
    tk.Label(filter_frame, text="Semester:").grid(row=1, column=0, padx=5)
    tk.OptionMenu(filter_frame, semester_var, "Select", "1st", "2nd", "Midyear").grid(row=1, column=1, padx=5)

    tk.Label(filter_frame, text="Academic Year:").grid(row=1, column=2, padx=5)
    tk.Entry(filter_frame, textvariable=academic_year_var, width=15).grid(row=1, column=3, padx=5)

    def apply_serves_filters():
        filters = {}
        if mem_id_var.get():
            filters["mem_id"] = mem_id_var.get()
        if org_id_var.get():
            filters["org_id"] = org_id_var.get()
        if role_var.get():
            filters["role"] = role_var.get()
        if status_var.get():
            filters["status"] = status_var.get()
        if committee_var.get():
            filters["committee"] = committee_var.get()
        if semester_var.get() != "Select":
            filters["semester"] = semester_var.get()
        if academic_year_var.get():
            filters["academic_year"] = academic_year_var.get()
        refresh_serves_table(root, cur, filters,"")

    tk.Button(filter_frame, text="Apply Filters", command=apply_serves_filters).grid(row=1, column=4, padx=10)

    # --- Sort and Reset tools ---
    tools_frame = tk.Frame(top_frame)
    tools_frame.pack(side="right")

    tk.Label(tools_frame, text="Sort by:").pack(side="left", padx=5)
    sort_options = ["mem_id", "org_id", "role", "status", "committee", "semester", "academic_year"]

    def on_sort_select(selected_col):
        if selected_col == "Sort by":
            return
        data = [(root.tree.set(child, selected_col), child) for child in root.tree.get_children()]
        try:
            data.sort(key=lambda x: float(x[0]))
        except ValueError:
            data.sort(key=lambda x: x[0].lower())
        for index, (val, child) in enumerate(data):
            root.tree.move(child, '', index)

    tk.OptionMenu(tools_frame, sort_var, *sort_options, command=on_sort_select).pack(side="left")

    def reset_serves_filters():
        mem_id_var.set("")
        org_id_var.set("")
        role_var.set("")
        status_var.set("")
        committee_var.set("")
        semester_var.set("Select")
        academic_year_var.set("")
        sort_var.set("Sort by")
        refresh_serves_table(root, cur, {},sort_var.get())

    tk.Button(tools_frame, text="🔄", font=("Arial", 12), command=reset_serves_filters).pack(side="left", padx=10)

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
            mem_id = values[0]
            org_id = values[1]
            academic_year = values[6]
            semester = values[5] 

            # Execute delete query
            cur.execute("""
                DELETE FROM serves 
                WHERE mem_id = %s AND org_id = %s AND academic_year = %s AND semester = %s
            """, (mem_id, org_id, academic_year, semester))

        # Commit the change to database
        cur.connection.commit()

        # Refresh table after deletion
        refresh_serves_table(root, cur, {}, "")

    # Add the button under the table
    delete_button = tk.Button(root, text="Delete Selected", command=delete_selected, fg="red")
    delete_button.pack(pady=10)

    # --- Treeview section ---
    tree_frame = tk.Frame(root)
    tree_frame.pack(fill="both", expand=True)

    columns = ("mem_id", "org_id", "role", "status", "committee", "semester", "academic_year")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    root.tree = tree
    refresh_serves_table(root, cur, {},"")

def refresh_serves_table(root, cur, filters, sort_by):
    query = """SELECT mem_id, org_id, role, status, committee, semester, academic_year FROM serves WHERE 1=1"""

    if filters.get("mem_id"):
        query += f" AND mem_id = {filters['mem_id']}"
    if filters.get("org_id"):
        query += f" AND org_id = {filters['org_id']}"
    if filters.get("role"):
        query += f" AND role LIKE '%{filters['role']}%'"
    if filters.get("status"):
        query += f" AND status LIKE '%{filters['status']}%'"
    if filters.get("committee"):
        query += f" AND committee LIKE '%{filters['committee']}%'"
    if filters.get("semester"):
        query += f" AND semester = '{filters['semester']}'"
    if filters.get("academic_year"):
        query += f" AND academic_year LIKE '%{filters['academic_year']}%'"

    if sort_by and sort_by != "Sort by":
        query += f" ORDER BY {sort_by}"

    cur.execute(query)
    serves = cur.fetchall()

    for row in root.tree.get_children():
        root.tree.delete(row)

    for serve in serves:
        root.tree.insert("", "end", values=serve)
