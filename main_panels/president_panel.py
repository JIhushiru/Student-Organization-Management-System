"""Imports"""
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from tkinter import messagebox
import customtkinter as ctk

from setup.db_connection import get_connection
from tables.fee import show_fee_table
from tables.members import show_member_table


# DATABASE CONNECTION
conn = get_connection()
cur = conn.cursor()

# MAIN FUNCTION TO SET UP THE GUI FOR PRESIDENT PANEL
def open_president_panel(root, admin, org_name, org_id, name,show_login_callback):
    
    for widget in root.winfo_children():
        widget.destroy()

    buttons = [
        ("Home", "home"),
        ("Manage Members", "member"),
        ("View Fees", "fee"),
    ]

    # COLOR SCHEME AND FONTS
    primary_color = "#1a1a40"
    button_bg = "#00A4EF"
    button_hover_bg = "#0063B1"
    button_selected_bg = "#005A8D"
    main_area_bg = "#FFFFFF"
    title_font = ("Segoe UI", 16, "bold")
    button_font = ("Segoe UI", 12)

    # TOP NAVIGATION BAR
    top_nav = tk.Frame(root, bg=primary_color, height=50)
    top_nav.pack_propagate(False)  # Prevent shrinking
    top_nav.pack(side="top", fill="x")
    top_nav_title = tk.Label(top_nav, text=org_name, fg="white", bg=primary_color, font=title_font)
    top_nav_title.pack(side="left", padx=(13,5))

    # HOVER EFFECTS AND BUTTON SELECTION
    def on_enter(e):
        if e.widget["bg"] != button_selected_bg:
            e.widget["bg"] = button_hover_bg

    def on_leave(e):
        if e.widget["bg"] != button_selected_bg:
            e.widget["bg"] = button_bg

    selected_button = None  # Variable to track the selected button

    def button_click(button, table_name):
        nonlocal selected_button
        if selected_button:
            selected_button.config(bg=button_bg)
        button.config(bg=button_selected_bg)
        selected_button = button
        load_table(table_name)

    # TO CREATE BUTTONS IN THE TOP NAVIGATION BAR
    nav_buttons = []
    for i, (text, table) in enumerate(buttons):
        btn = tk.Button(top_nav, text=text, 
                        command=lambda t=table, b=None: button_click(b or nav_buttons[buttons.index((text, t))], t), 
                        fg="white", bg=button_bg, font=button_font, relief="flat", bd=0)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        nav_buttons.append(btn) 
        btn.config(command=lambda t=table, b=btn: button_click(b, t))

        if i == 0:
            btn.pack(side="left", ipady=5, ipadx=5, padx=(3, 7), pady=7)
        else:
            btn.pack(side="left", ipady=5, ipadx=5, padx=7, pady=7)

        if text == "Home":
            selected_button = btn
            btn.config(bg=button_selected_bg)  # Set default button to selected color

    # MAIN AREA
    main_area = tk.Frame(root, bg=main_area_bg)
    main_area.pack(expand=True, fill="both")

    def display_report(parent, rows, columns):
        tree = ttk.Treeview(parent, columns=columns, show="headings")

        font = tkFont.Font()

        for col in columns:
            tree.heading(col, text=col)

            max_width = font.measure(col)
            col_index = columns.index(col)
        
            for row in rows:
                cell_value = str(row[col_index])
                cell_width = font.measure(cell_value)
                max_width = max(max_width, cell_width)

            tree.column(col, width=max_width + 20, anchor="center")

        for row in rows:
            tree.insert("", "end", values=row)

        tree.pack(expand=True, fill="both", padx=20, pady=10)

    def load_table(table_name):
        for widget in main_area.winfo_children():
            widget.destroy()
        top_nav_title.config(text=org_name)
        main_area.update_idletasks()

        if table_name == "home":
            show_summary_reports_panel(main_area, on_report_click=load_table)

        elif table_name == "member":
            show_member_table(main_area, cur, org_id)
        elif table_name == "fee":
            show_fee_table(main_area, cur, org_id)

        # REPORTS
        elif table_name == "unpaid":
            # 2. Unpaid fees for org by semester and academic year
            fields = [
                {"label": "Semester", "type": "combo", "options": ["1st", "2nd"], "default": "1st"},
                {"label": "Academic Year", "type": "entry", "default": "2024-2025"}
            ]
            values = ctk_prompt(root, "Filter Unpaid Membership Fees", fields)
            if not values or not isinstance(values, dict):
                show_summary_reports_panel(main_area, load_table)
                return
            semester = values.get("Semester")
            academic_year = values.get("Academic Year")
            query ="""
                SELECT org_id, org_name, mem_id,
                    concat(surname,', ',first_name,' ', second_name), 
                    fee_type,
                    amount,
                    academic_year_issued,
                    semester_issued,
                    due_date 
                FROM Unpaid 
                where semester_issued = %s AND academic_year_issued = %s
            """
            if org_id != 0:
                query = query + "AND org_id = %s "
                cur.execute(query, (semester, academic_year, org_id))
            else:
                cur.execute(query, (semester, academic_year))

            rows = cur.fetchall()
            display_report(main_area, rows, ["Org ID", "Organization","ID", "Name", "Type", "Amount", "Year", "Sem", "Due Date"])

        elif table_name == "member_dues":
            # 3. Member's unpaid fees for all orgs - needs member surname and mem_id input
            fields = [
                {"label": "Surname", "type": "text"},
                {"label": "Member ID", "type": "text"},
            ]
            values = ctk_prompt(root, "Filter Member Dues", fields)

            if not values or not isinstance(values, dict):
                show_summary_reports_panel(main_area, load_table)
                return

            mem_id = values.get("Member ID")
            surname = values.get("Surname")

            query = """
                SELECT org_id, org_name, mem_id,
                    concat(surname,', ',first_name,' ', second_name), 
                    fee_type,
                    amount,
                    academic_year_issued,
                    semester_issued,
                    due_date 
                    FROM unpaid
                    WHERE mem_id = %s AND surname = %s
            """

            if org_id != 0:
                query += " AND org_id = %s"
                cur.execute(query, (mem_id, surname, org_id))
            else:
                cur.execute(query, (mem_id, surname))

            rows = cur.fetchall()

            display_report(main_area, rows, ["Org ID","Organization","ID", "Name", "Type", "Amount", "Year", "Sem", "Due Date"])

        elif table_name == "exec":
            # 4. Executives for org and academic year
            fields = [
                {"label": "Academic Year", "type": "entry", "default": "2024-2025"}
            ]
            values = ctk_prompt(root, "Filter Executive Committee", fields)
            
            if not values or not isinstance(values, dict):
                show_summary_reports_panel(main_area, load_table)
                return

            academic_year = values.get("Academic Year")
            query = """
                SELECT org_id, org_name, mem_id, concat(surname,', ',first_name,' ', second_name),
                    role,
                    academic_year FROM Exec
                    WHERE academic_year = %s
            """
            
            if org_id != 0:
                query += " AND org_id = %s"
                cur.execute(query, (academic_year, org_id))
            else:
                cur.execute(query, (academic_year,)) 

            rows = cur.fetchall()

            if not rows:
                ctk.CTkLabel(main_area, text="No executive committee found for that year.", text_color="red", font=("Arial", 14)).pack(pady=20)
            else:
                display_report(main_area, rows, ["Org ID","Organization", "ID", "Name", "Role", "Year"])


        elif table_name == "roles_per_year":
            # 5. Presidents for org, all years reverse order
            fields = [
                {"label": "Role", "type": "entry", "default": "President"}
            ]
            values = ctk_prompt(root, "Search Roles", fields)
            if not values or not isinstance(values, dict):
                show_summary_reports_panel(main_area, load_table)
                return

            role = values.get("Role")
            query = """
                SELECT org_id,org_name, mem_id, concat(surname,', ',first_name,' ', second_name), academic_year, semester 
                FROM RolesPerYear 
                WHERE role = %s 
            """
            order = " ORDER BY academic_year DESC "
            if org_id != 0:
                query = query + "AND org_id = %s"
                cur.execute(query+order, (role,org_id))
            else:
                cur.execute(query+order, (role,))
            rows = cur.fetchall()
            display_report(main_area, rows, ["org ID,","Organization","Mem ID", "Name", "Year", "Semester"])

        elif table_name == "late_payments":
            # 6. Late payments for org, semester, academic year
            fields = [
                {"label": "Semester", "type": "combo", "options": ["1st", "2nd"], "default": "1st"},
                {"label": "Academic Year", "type": "entry", "default": "2024-2025"}
            ]
            values = ctk_prompt(root, "Filter Late Payments", fields)
            if not values or not isinstance(values, dict):
                show_summary_reports_panel(main_area, load_table)
                return
            semester = values.get("Semester")
            academic_year = values.get("Academic Year")
            query = """
                SELECT org_id,org_name, mem_id, concat(surname,', ',first_name,' ', second_name), fee_type, amount, academic_year_issued, semester_issued, due_date, date_paid 
                FROM LatePayments 
                WHERE semester_issued = %s AND academic_year_issued = %s
            """
            if org_id != 0:
                query += "AND org_id = %s "
                cur.execute(query, (semester, academic_year, org_id))
            else:
                cur.execute(query, (semester, academic_year))
            rows = cur.fetchall()
            display_report(main_area, rows, ["Org ID","Organization","ID", "Name", "Type", "Amount", "Year", "Semester", "Due Date", "Date Paid"])
        
        elif table_name == "percentage":
            # 7. Percentage of active vs inactive members of a given organization for the last n semesters.
            fields = [
                {"label": "Number of Semesters", "type": "entry", "default": "2"}
            ]
            values = ctk_prompt(root, "Filter Active Percentage", fields)
            if not values or not isinstance(values, dict):
                show_summary_reports_panel(main_area, load_table)
                return

            n_semesters = int(values.get("Number of Semesters"))

            if org_id != 0:
                cur.execute("""
                    SELECT p.org_id, p.org_name, p.semester, p.academic_year,p.num_members,p.active_members,p.active_percentage
                    FROM percentage p
                    JOIN (
                        SELECT DISTINCT academic_year, semester
                        FROM percentage
                        WHERE org_id = %s
                        ORDER BY academic_year DESC,
                                FIELD(semester, '2nd', 'Midyear', '1st')
                        LIMIT %s
                    ) recent ON p.academic_year = recent.academic_year AND p.semester = recent.semester
                    WHERE p.org_id = %s
                """, (org_id, n_semesters, org_id))
            else:
                cur.execute("""
                    SELECT p.org_id, p.org_name, p.semester, p.academic_year,p.num_members,p.active_members,p.active_percentage
                    FROM percentage p
                    JOIN (
                        SELECT DISTINCT academic_year, semester
                        FROM percentage
                        ORDER BY academic_year DESC,
                                FIELD(semester, '2nd', 'Midyear', '1st')
                        LIMIT %s
                    ) recent ON p.academic_year = recent.academic_year AND p.semester = recent.semester
                """, (n_semesters,))

            rows = cur.fetchall()

            display_report(main_area, rows, ["Org ID", "Organization", "Semester", "Academic Year", "Number of Members", "Active Members", "Active %"])

        elif table_name == "alumni":
            # 8. Alumni as of a given date
            fields = [
                {"label": "Date (YYYY-MM-DD)", "type": "entry", "default": ""}
            ]
            values = ctk_prompt(root, "Filter Alumni", fields)
            if not values:
                show_summary_reports_panel(main_area, load_table)
                return

            date_as_of = values.get("Date (YYYY-MM-DD)")
            query = """
                SELECT org_id, org_name, mem_id, CONCAT(surname, ', ', first_name, ' ', second_name), academic_year, semester
                    FROM Alumni
                    WHERE DATE_FORMAT(STR_TO_DATE(SUBSTRING_INDEX(academic_year, '-', -1), '%Y'), '%Y') <= %s
            """
            if org_id != 0:
                query += "AND org_id = %s "
                cur.execute(query, (date_as_of, org_id))
            else:
                cur.execute(query, (date_as_of, ))

            rows = cur.fetchall()
            display_report(main_area, rows, ["Org ID","Organization", "Mem ID", "Name", "Year", "Semester"])

        elif table_name == "fee_summary":
            # 9. Total fees paid/unpaid as of a given date
            fields = [
                {"label": "As of Date (YYYY-MM-DD)", "type": "entry", "default": ""}
            ]
            values = ctk_prompt(root, "Fee Summary as of Date", fields)
            if not values:
                show_summary_reports_panel(main_area, load_table)
                return

            as_of_date = values.get("As of Date (YYYY-MM-DD)")

            # CALCULATES PAID OR UNPAID FEES
            if org_id != 0:
                cur.execute("""
                    SELECT
                        f.org_id,
                        o.org_name,
                        SUM(f.amount) AS total_fees,
                        SUM(CASE
                            WHEN f.status = 'Paid' AND f.date_paid <= %s THEN f.amount
                            ELSE 0
                        END) AS total_paid,
                        SUM(CASE
                            WHEN (f.status != 'Paid' OR f.date_paid > %s OR f.date_paid IS NULL) THEN f.amount
                            ELSE 0
                        END) AS total_unpaid
                    FROM Fee f
                    JOIN Organization o ON f.org_id = o.org_id
                    WHERE f.org_id = %s AND f.due_date <= %s
                    GROUP BY f.org_id, o.org_name
                """, (as_of_date, as_of_date, org_id, as_of_date))
            else:
                cur.execute("""
                    SELECT
                        f.org_id,
                        o.org_name,
                        SUM(f.amount) AS total_fees,
                        SUM(CASE
                            WHEN f.status = 'Paid' AND f.date_paid <= %s THEN f.amount
                            ELSE 0
                        END) AS total_paid,
                        SUM(CASE
                            WHEN (f.status != 'Paid' OR f.date_paid > %s OR f.date_paid IS NULL) THEN f.amount
                            ELSE 0
                        END) AS total_unpaid
                    FROM Fee f
                    JOIN Organization o ON f.org_id = o.org_id
                    WHERE f.due_date <= %s
                    GROUP BY f.org_id, o.org_name
                """, (as_of_date, as_of_date, as_of_date))

            rows = cur.fetchall()

            display_report(main_area, rows, ["Org ID", "Organization Name", "Total Fees", "Total Paid", "Total Unpaid"])

        elif table_name == "highest_debt":
            # 10. Highest debtors for org by semester and academic year
            fields = [
                {"label": "Semester", "type": "combo", "options": ["1st", "2nd"], "default": "1st"},
                {"label": "Academic Year", "type": "entry", "default": "2024-2025"}
            ]
            values = ctk_prompt(root, "Filter Highest Debtors", fields)
            if not values:
                show_summary_reports_panel(main_area, load_table)
                return

            semester = values.get("Semester")
            academic_year = values.get("Academic Year")

            if org_id != 0:
                cur.execute("""
                    SELECT org_id, org_name, mem_id, surname, first_name, second_name, semester_issued, academic_year_issued, total_unpaid
                    FROM HighestDebt
                    WHERE org_id = %s AND semester_issued = %s AND academic_year_issued = %s
                    ORDER BY total_unpaid DESC
                """, (org_id, semester, academic_year))
            else:
                cur.execute("""
                    SELECT org_id, org_name, mem_id, surname, first_name, second_name, semester_issued, academic_year_issued, total_unpaid
                    FROM HighestDebt
                    WHERE semester_issued = %s AND academic_year_issued = %s
                    ORDER BY total_unpaid DESC
                """, (semester, academic_year))

            rows = cur.fetchall()
            if not rows:
                ctk.CTkLabel(main_area, text="No highest debtors found for that period.", text_color="red", font=("Arial", 14)).pack(pady=20)
            else:
                display_report(main_area, rows, ["Org ID","Organization", "ID", "Surname", "First", "Second", "Semester", "Year", "Total Unpaid"])

    load_table("home")

    # SUPERADMIN BACK BUTTON
    if(admin):
        def go_back():
            from main_panels.superadmin_panel import open_superadmin_panel 
            # Clear current panel
            for widget in root.winfo_children():
                widget.destroy()
            # Reopen superadmin panel
            open_superadmin_panel(root, name, show_login_callback)
        back_btn = tk.Button(
            top_nav,
            text="Admin Page",
            command=go_back,
            fg="white",
            bg=button_bg,
            font=button_font,
            relief="flat",
            bd=0
        )
        back_btn.pack(side="right", ipady=5, ipadx=5, padx=7, pady=7)
        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)

    # LOG OUT BUTTON
    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            for widget in root.winfo_children():
                widget.destroy()
            show_login_callback()

    logout_btn = tk.Button(
        top_nav,
        text="Log Out",
        command=logout,
        fg="white",
        bg="#c0392b",
        font=button_font,
        relief="flat",
        bd=0
    )
    logout_btn.pack(side="right", ipady=5, ipadx=5, padx=7, pady=7)

    # MY FEES BUTTON
    def open_my_fees():
        cur.execute("""
            SELECT u.mem_id, u.username
            FROM userdata u
            JOIN serves s ON u.mem_id = s.mem_id
            WHERE s.org_id = %s AND u.username = %s
        """, (org_id, name))
        result = cur.fetchone()
        if result:
            mem_id, username = result
            from tables.member_fee_panel import show_member_fee_panel
            # TO OPEN MEMBER FEE PANEL
            for widget in root.winfo_children():
                widget.destroy()
            show_member_fee_panel(root, mem_id, username,show_login_callback, open_president_panel, admin, org_name, org_id)
        else:
            messagebox.showerror("Not Found", "No president record found for this organization.")

    if org_id != 0:
        my_fees_btn = tk.Button(
            top_nav,
            text="My Fees",
            command=open_my_fees,
            fg="white",
            bg="#0078D4",
            font=button_font,
            relief="flat",
            bd=0
        )
        my_fees_btn.pack(side="right", ipady=5, ipadx=5, padx=7, pady=7)

# SUMMARY REPORTS PANEL GUI
def show_summary_reports_panel(root, on_report_click):
    
    for widget in root.winfo_children():
        widget.destroy()

    # HEADER FRAME
    header_frame = ctk.CTkFrame(root, fg_color="#020325",corner_radius=0)
    header_frame.pack(fill="x", pady=(0, 10))

    header_label = ctk.CTkLabel(
        header_frame,
        text="SUMMARY REPORTS",
        font=("Palatino Linotype", 40, "bold"),
        text_color="white"
    )
    header_label.pack(pady=10)

    # SUBTEXT
    subtext = ctk.CTkLabel(
        root,
        text="Members, Fees, and More!",
        font=("Arial", 16, "italic"),
        text_color="#020325"
    )
    subtext.pack(pady=(0, 20))

    # CONTENT FRAME
    content_frame = ctk.CTkFrame(root, fg_color="white", corner_radius=20)
    content_frame.pack(fill="both", expand=True, padx=40, pady=10)

    # REPORTS
    reports = [
        ("Unpaid Membership Fees", "unpaid"),
        ("Member Dues", "member_dues"),
        ("Executive Committee", "exec"),
        ("Search Roles", "roles_per_year"),
        ("Late Payments", "late_payments"),
        ("Status Percentage", "percentage"),
        ("Alumni", "alumni"),
        ("Fee Summary", "fee_summary"),
        ("Top Debtors", "highest_debt")
    ]

    # GRID LAYOUT FOR REPORT BUTTONS
    cols = 3
    for idx, (label, key) in enumerate(reports):
        row, col = divmod(idx, cols)
        btn = ctk.CTkButton(
            content_frame,
            text=label,
            command=lambda k=key: on_report_click(k),
            fg_color="#020325",
            hover_color="#005A8D",
            text_color="white",
            font=("Arial", 14, "bold"),
            width=220,
            height=60,
            corner_radius=12
        )
        btn.grid(row=row, column=col, padx=30, pady=20, sticky="nsew")
        
    for c in range(cols):
        content_frame.grid_columnconfigure(c, weight=1)


# --- SMOOTH MODAL DIALOG FUNCTION ---
def ctk_prompt(root, title, fields):
    result = {}

    popup = ctk.CTkToplevel(root)
    popup.title(title)
    popup.geometry("400x240")
    popup.resizable(False, False)
    popup.configure(fg_color="white")

    # CENTERS THE DIALOG
    root.update_idletasks()
    popup.update_idletasks()
    x = root.winfo_rootx() + (root.winfo_width() // 2) - 200
    y = root.winfo_rooty() + (root.winfo_height() // 2) - 120
    y -= 100
    popup.geometry(f"+{x}+{y}")

    frame = ctk.CTkFrame(popup, fg_color="white", corner_radius=15)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    vars = []
    for i, field in enumerate(fields):
        label = ctk.CTkLabel(frame, text=field["label"] + ":", font=("Arial", 13), text_color="black")
        label.grid(row=i, column=0, sticky="e", pady=7, padx=5)
        
        if field["type"] == "combo":
            var = ctk.StringVar(value=field.get("default", "Select"))
            combo = ctk.CTkComboBox(frame, variable=var, values=field["options"], width=180)
            combo.grid(row=i, column=1, pady=7, padx=5, sticky="w")
            vars.append(var)
        else:
            var = ctk.StringVar(value=field.get("default", ""))
            entry = ctk.CTkEntry(frame, textvariable=var, width=180)
            entry.grid(row=i, column=1, pady=7, padx=5, sticky="w")
            vars.append(var)

    error_label = ctk.CTkLabel(frame, text="", text_color="red", font=("Arial", 11))
    error_label.grid(row=len(fields)+1, column=0, columnspan=2, pady=(5,0))

    def on_ok():
        for idx, field in enumerate(fields):
            val = vars[idx].get().strip()
            if not val or val == "Select":
                error_label.configure(text="All fields required.")
                return
            result[field["label"]] = val
        popup.destroy()

    def on_cancel():
        popup.destroy()

    btn_frame = ctk.CTkFrame(frame, fg_color="white")
    btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=(15,0))
    btn_frame.grid_columnconfigure((0, 1), weight=1)
    
    ctk.CTkButton(btn_frame, text="OK", command=on_ok, fg_color="#0078D4", text_color="white", width=90).grid(row=0, column=0, padx=8)
    ctk.CTkButton(btn_frame, text="Cancel", command=on_cancel, fg_color="#6c140a", text_color="white", width=90).grid(row=0, column=1, padx=8)

    popup.transient(root)  # Makes it stay on top of root, but not block it
    popup.lift()           # Bring to front without blocking input to root
    popup.focus_force()    # Focus on popup
    popup.wait_window()    # Optional: wait for popup to close before continuing

    return result if result else None

