import tkinter as tk
from tkinter import ttk, messagebox
from authentication import hash_password

# Color scheme and fonts
primary_color = "#0078D4"
button_bg = "#00A4EF"
button_hover_bg = "#0063B1"
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


def show_member_table(root, cur, org_id):
    # Top filter and sort UI
    top_frame = tk.Frame(root, pady=10, bg=main_area_bg)
    top_frame.pack(fill="x")

    filter_frame = tk.Frame(top_frame, bg=main_area_bg)
    filter_frame.pack(side="left", fill="x", expand=True)

    gender_var = tk.StringVar(value="Select")
    batch_var = tk.StringVar()
    degree_var = tk.StringVar()
    year_var = tk.StringVar()
    sort_var = tk.StringVar(value="Sort by")
    role_var = tk.StringVar()
    status_var = tk.StringVar()

    tk.Label(filter_frame, text="Gender:", bg=main_area_bg).grid(row=0, column=0, padx=5)
    gender_menu = tk.OptionMenu(filter_frame, gender_var, "Select", "M", "F")
    gender_menu.config(relief="flat", font=modern_font, bg="white", highlightthickness=1, borderwidth=1)
    gender_menu.grid(row=0, column=1, padx=5)
    tk.Label(filter_frame, text="Batch:", bg=main_area_bg).grid(row=0, column=2, padx=5)
    tk.Entry(filter_frame, textvariable=batch_var, width=8, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="gray").grid(row=0, column=3, padx=5)
    tk.Label(filter_frame, text="Degree:", bg=main_area_bg).grid(row=0, column=4, padx=5)
    tk.Entry(filter_frame, textvariable=degree_var, width=10, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="gray").grid(row=0, column=5, padx=5)
    tk.Label(filter_frame, text="Role:", bg=main_area_bg).grid(row=0, column=8, padx=5)
    tk.Entry(filter_frame, textvariable=role_var, width=10, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="gray").grid(row=0, column=9, padx=5)
    tk.Label(filter_frame, text="Status:", bg=main_area_bg).grid(row=0, column=10, padx=5)
    tk.Entry(filter_frame, textvariable=status_var, width=10, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="gray").grid(row=0, column=11, padx=5)
    tk.Label(filter_frame, text="Year:", bg=main_area_bg).grid(row=0, column=6, padx=5)
    tk.Entry(filter_frame, textvariable=year_var, width=8, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="gray").grid(row=0, column=7, padx=5)

    tk.Label(filter_frame, text="Gender:", bg=main_area_bg).grid(row=0, column=0, padx=5)
    gender_menu = tk.OptionMenu(filter_frame, gender_var, "Select", "M", "F")
    gender_menu.config(relief="flat", font=modern_font, bg="white", highlightthickness=1, borderwidth=1)
    gender_menu.grid(row=0, column=1, padx=5)
    tk.Label(filter_frame, text="Batch:", bg=main_area_bg).grid(row=0, column=2, padx=5)
    tk.Entry(filter_frame, textvariable=batch_var, width=8, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="gray").grid(row=0, column=3, padx=5)
    tk.Label(filter_frame, text="Degree:", bg=main_area_bg).grid(row=0, column=4, padx=5)
    tk.Entry(filter_frame, textvariable=degree_var, width=10, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="gray").grid(row=0, column=5, padx=5)
    tk.Label(filter_frame, text="Year:", bg=main_area_bg).grid(row=0, column=6, padx=5)
    tk.Entry(filter_frame, textvariable=year_var, width=8, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="gray").grid(row=0, column=7, padx=5)
    tk.Label(filter_frame, text="Role:", bg=main_area_bg).grid(row=0, column=8, padx=5)
    tk.Entry(filter_frame, textvariable=role_var, width=10, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="gray").grid(row=0, column=9, padx=5)
    tk.Label(filter_frame, text="Status:", bg=main_area_bg).grid(row=0, column=10, padx=5)
    tk.Entry(filter_frame, textvariable=status_var, width=10, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="gray").grid(row=0, column=11, padx=5)
    
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
        if role_var.get():
            filters["role"] = role_var.get()
        if status_var.get():
            filters["status"] = status_var.get()
        refresh_member_table(root, cur, filters, sort_var.get(), org_id)
  
    # apply_btn = tk.Button(filter_frame, text="Apply Filters", command=apply_filters)
    # apply_btn.grid(row=0, column=8, padx=10)
    # style_button(apply_btn)

    # Place Apply Filters button after all filter fields
    apply_btn = tk.Button(filter_frame, text="Apply Filters", command=apply_filters)
    apply_btn.grid(row=0, column=12, padx=10)

    # Sort and reset
    right_tools_frame = tk.Frame(top_frame, bg=main_area_bg)
    right_tools_frame.pack(side="right")

    tk.Label(right_tools_frame, text="Sort by:", bg=main_area_bg).pack(side="left", padx=5)
    sort_options = [
        "mem_id", "first_name", "second_name", "surname",
        "batch", "committee"
    ]

    def on_sort_select(selected_col):
        if selected_col != "Sort by":
            filters = {}
            if gender_var.get() != "Select":
                filters["gender"] = gender_var.get()
            if batch_var.get():
                filters["batch"] = batch_var.get()
            if degree_var.get():
                filters["degree"] = degree_var.get()
            if year_var.get():
                filters["year"] = year_var.get()
            refresh_member_table(root, cur, filters, selected_col, org_id)


    sort_menu = tk.OptionMenu(right_tools_frame, sort_var, *sort_options, command=on_sort_select)
    sort_menu.config(relief="flat",
        font=modern_font,
        bg="white",
        highlightthickness=1,
        borderwidth=1)
    sort_menu.pack(side="left")

    def reset_all():
        gender_var.set("Select")
        batch_var.set("")
        degree_var.set("")
        year_var.set("")
        sort_var.set("Sort by")
        refresh_member_table(root, cur, {}, "", org_id)

    reset_btn = tk.Button(right_tools_frame, text="🔄", font=modern_font, command=reset_all)
    reset_btn.pack(side="left", padx=10)
    style_button(reset_btn)

    # Treeview
    tree_frame = tk.Frame(root)
    tree_frame.pack(fill="both", expand=True)

    columns = ("Member Id",
        "Name",
        "Role",
        "Status",
        "Gender",
        "Degree Program",
        "Batch",
        "Year of Membership",
        "Committee")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Modern.Treeview")
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    # Modern Treeview Style
    style = ttk.Style()
    style.configure("Modern.Treeview", font=modern_font, rowheight=25)
    style.configure("Modern.Treeview.Heading", font=("Arial", 9, "bold"))

    root.tree = tree

    # Buttons frame
    button_frame = tk.Frame(root, bg=main_area_bg)
    button_frame.pack(pady=10)

    def delete_selected():
        selected = root.tree.selection()
        if not selected:
            return
        confirm = messagebox.askyesno("Delete",
            "Are you sure you want to delete the selected member?")
        if not confirm:
            return

        for item in selected:
            values = root.tree.item(item, "values")
            member_id = values[0]
            cur.execute("DELETE FROM userdata WHERE mem_id = %s", (member_id,))
            cur.execute("DELETE FROM fee WHERE mem_id = %s", (member_id,))
            cur.execute("DELETE FROM serves WHERE mem_id = %s", (member_id,))
            cur.execute("DELETE FROM member WHERE mem_id = %s", (member_id,))
        cur.connection.commit()
        refresh_member_table(root, cur, {}, "", org_id)

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
                """, (first_name,
                      second_name, surname,
                      email, deg_prog,
                      year_mem, gender,
                      batch,
                      member_id))
                cur.connection.commit()
                refresh_member_table(root, cur, {}, "", org_id)
                edit_window.destroy()
            except ImportError as e:
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
                tk.Entry(edit_window, textvariable=var, font=modern_font, bd=1, relief="flat", highlightthickness=1, highlightbackground="black").grid(row=idx, column=1)

        save_btn = tk.Button(edit_window, text="Save Changes", command=save_changes)
        save_btn.grid(row=len(entries), column=0, columnspan=2, pady=10)
        style_button(save_btn)

    def add_member(root, cur, org_id):
        # Create a new window to add a member
        add_window = tk.Toplevel(root)
        add_window.title("Add Member")
        
        # Create the labels and entry fields
        tk.Label(add_window, text="First Name").grid(row=0, column=0)
        new_first_name = tk.Entry(add_window)
        new_first_name.grid(row=0, column=1)
        
        tk.Label(add_window, text="Second Name").grid(row=1, column=0)
        new_second_name = tk.Entry(add_window)
        new_second_name.grid(row=1, column=1)
        
        tk.Label(add_window, text="Surname").grid(row=2, column=0)
        new_surname = tk.Entry(add_window)
        new_surname.grid(row=2, column=1)
        
        tk.Label(add_window, text="Email").grid(row=3, column=0)
        new_email = tk.Entry(add_window)
        new_email.grid(row=3, column=1)
        
        tk.Label(add_window, text="Degree Program").grid(row=4, column=0)
        new_deg_prog = tk.Entry(add_window)
        new_deg_prog.grid(row=4, column=1)
        
        tk.Label(add_window, text="Year of Membership").grid(row=5, column=0)
        new_year_mem = tk.Entry(add_window)
        new_year_mem.grid(row=5, column=1)
        
        tk.Label(add_window, text="Gender (M/F)").grid(row=6, column=0)
        new_gender = tk.Entry(add_window)
        new_gender.grid(row=6, column=1)
        
        tk.Label(add_window, text="Batch").grid(row=7, column=0)
        new_batch = tk.Entry(add_window)
        new_batch.grid(row=7, column=1)
    
        tk.Label(add_window, text="Role").grid(row=8, column=0)
        new_role = tk.Entry(add_window)
        new_role.grid(row=8, column=1)
   
        tk.Label(add_window, text="Committee").grid(row=9, column=0)
        new_committee = tk.Entry(add_window)
        new_committee.grid(row=9, column=1)

        tk.Label(add_window, text="Semester").grid(row=10, column=0)
        new_semester = ttk.Combobox(add_window, values=["1st", "2nd", "Midyear"])
        new_semester.grid(row=10, column=1)

        tk.Label(add_window, text="Academic Year").grid(row=11, column=0)
        new_academic_year = tk.Entry(add_window)
        new_academic_year.grid(row=11, column=1)

        tk.Label(add_window, text="Password").grid(row=12, column=0)
        new_pass = tk.Entry(add_window)
        new_pass.grid(row=12, column=1)

        def save_new_member(root, cur, org_id):
            # Gather all input values
            first_name = new_first_name.get()
            second_name = new_second_name.get()
            surname = new_surname.get()
            email = new_email.get()
            deg_prog = new_deg_prog.get()
            year_mem = new_year_mem.get()
            gender = new_gender.get()
            batch = new_batch.get()
            role = new_role.get()
            committee = new_committee.get()
            semester = new_semester.get()
            academic_year = new_academic_year.get()
            password = new_pass.get()

            # Insert member into the MEMBER table (mem_id is auto-incremented)
            try:
                cur.execute("""
                    INSERT INTO member (first_name, second_name, surname, email, deg_prog, year_mem, gender, batch) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (first_name, second_name, surname, email, deg_prog, year_mem, gender, batch))

                # Get the last inserted mem_id
                cur.execute("SELECT LAST_INSERT_ID()")
                mem_id = cur.fetchone()[0]
                # Insert into SERVES table with the provided role, 
                # committee, semester, and academic year
                cur.execute("""
                    INSERT INTO serves (mem_id, org_id, role, status, committee, semester, academic_year) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (mem_id, org_id, role, "Active", committee, semester, academic_year))

                username = email.split('@')[0]
                hashed_password = hash_password(password)
                cur.execute("""
                    INSERT INTO userdata (username, password, , user_type, mem_id)
                    VALUES (%s, %s, %s, %s)
                """, (username, (hashed_password), 'user', mem_id))

                # Commit the changes and refresh the table
                cur.connection.commit()
                refresh_member_table(root, cur, {}, "", org_id)
                add_window.destroy()  # Close the window after saving
            except ImportError as e:
                messagebox.showerror("Error",
                    str(e))  # Show an error message if something goes wrong

        # Create a button to save the member data
        save_button = tk.Button(add_window,
            text="Save Member",
            command=lambda: save_new_member(root, cur, org_id))
        save_button.grid(row=13, column=0, columnspan=2)

    add_btn = tk.Button(button_frame,
        text="Add Member",
        command=lambda: add_member(root, cur, org_id))
    add_btn.pack(side="left", padx=10)
    style_button(add_btn)

    edit_btn = tk.Button(button_frame, text="Edit", command=edit_selected)
    edit_btn.pack(side="left", padx=10)
    style_button(edit_btn)

    del_btn = tk.Button(button_frame, text="Delete", command=delete_selected, fg="red")
    del_btn.pack(side="left", padx=10)
    style_button(del_btn)

    refresh_member_table(root, cur, {}, "", org_id)


def refresh_member_table(root, cur, filters, sort_by, org_id):
    """Refresh table"""
    base_query = """
    SELECT 
        mem_id, 
        concat(surname,', ',first_name,' ', second_name), 
        role, 
        status, 
        gender, 
        deg_prog, 
        batch,           -- from member
        year_mem,        -- from member
        committee 
    FROM member 
    NATURAL JOIN serves
    """
    conditions = []
    params = []

    if org_id != 0:
        conditions.append("org_id = %s")
        params.append(org_id)

    if filters.get("gender"):
        conditions.append("gender = %s")
        params.append(filters["gender"])
    if filters.get("batch"):
        conditions.append("batch = %s")
        params.append(filters["batch"])
    if filters.get("degree"):
        conditions.append("deg_prog LIKE %s")
        params.append(f"%{filters['degree']}%")
    if filters.get("year"):
        conditions.append("year_mem = %s")
        params.append(filters["year"])
    if filters.get("role"):
        conditions.append("role = %s")
        params.append(filters["role"])
    if filters.get("status"):
        conditions.append("status = %s")
        params.append(filters["status"])

    # Construct the WHERE clause only if there are conditions
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    # Add sorting if applicable
    if sort_by and sort_by != "Sort by":
        base_query += f" ORDER BY {sort_by}"

    cur.execute(base_query, tuple(params))
    members = cur.fetchall()

    # Clear and refill the tree
    for row in root.tree.get_children():
        root.tree.delete(row)
    for member in members:
        root.tree.insert("", "end", values=member)
