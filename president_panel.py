"""Imports"""
import tkinter as tk
import customtkinter as ctk

from tkinter import simpledialog
from db_connection import get_connection
from fee import show_fee_table
from members import show_member_table

# DATABASE CONNECTION
conn = get_connection()
cur = conn.cursor()

# MAIN FUNCTION TO SET UP THE GUI FOR PRESIDENT PANEL
def open_president_panel(root, admin, org_name, org_id):
    
    for widget in root.winfo_children():
        widget.destroy()

    buttons = [
        ("Home", "home"),
        ("Manage Members", "member"),
        ("View Fees", "fee"),
    ]

    # COLOR SCHEME
    primary_color = "#0078D4"
    button_bg = "#00A4EF"
    button_hover_bg = "#0063B1" 
    button_selected_bg = "#005A8D"  
    main_area_bg = "#FFFFFF"
    
    title_font = ("Segoe UI", 16, "bold")
    button_font = ("Segoe UI", 12)

    # TOP NAVIGATION BAR
    top_nav = tk.Frame(root, bg=primary_color, height=40)
    top_nav.pack_propagate(False)  # Prevent shrinking
    top_nav.pack(side="top", fill="x")
    top_nav_title = tk.Label(top_nav, text=org_name, fg="white", bg=primary_color, font=title_font)
    top_nav_title.pack(side="left", padx=10)

    # HOVER EFFECTS AND BUTTON SELECTION
    def on_enter(e):
        if e.widget["bg"] != button_selected_bg:
            e.widget["bg"] = button_hover_bg

    def on_leave(e):
        if e.widget["bg"] != button_selected_bg:
            e.widget["bg"] = button_bg

    selected_button = None  # Variable to track the selected button

    def button_click(e, table_name):
        nonlocal selected_button
        if selected_button:
            selected_button.config(bg=button_bg)  # Reset previous button color
        e.widget.config(bg=button_selected_bg)  # Set the clicked button to selected color
        selected_button = e.widget  # Update the selected button
        load_table(table_name)  # Load the appropriate table

    # TO CREATE BUTTONS IN THE TOP NAVIGATION BAR
    for i, (text, table) in enumerate(buttons):
        btn = tk.Button(top_nav, text=text, command=lambda t=table: load_table(t), 
                        fg="white", bg=button_bg, font=button_font, relief="flat", bd=0)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", lambda e, t=table: button_click(e, t))  # Track button click

        if i == 0:
            btn.pack(side="left", ipady=10, ipadx=10, padx=(3, 1), pady=2)  # More left margin
        else:
            btn.pack(side="left", ipady=10, ipadx=10, padx=2, pady=2)

        # Default selected button is the "Home" button
        if text == "Home":
            selected_button = btn
            btn.config(bg=button_selected_bg)  # Set default button to selected color

    # MAIN AREA
    main_area = tk.Frame(root, bg=main_area_bg)
    main_area.pack(expand=True, fill="both")

    def display_report(parent, rows, columns):
        import tkinter.ttk as ttk
        import tkinter.font as tkFont

        tree = ttk.Treeview(parent, columns=columns, show="headings")

        # Create a font object to measure text
        font = tkFont.Font()

        for col in columns:
            tree.heading(col, text=col)

            # Calculate maximum width based on column title
            max_width = font.measure(col)

            # Also check content width for each column
            col_index = columns.index(col)
            for row in rows:
                cell_value = str(row[col_index])
                cell_width = font.measure(cell_value)
                max_width = max(max_width, cell_width)

            # Set column width with padding
            tree.column(col, width=max_width + 20, anchor="center")

        for row in rows:
            tree.insert("", "end", values=row)

        tree.pack(expand=True, fill="both", padx=20, pady=10)

    def load_table(table_name):
        for widget in main_area.winfo_children():
            widget.destroy()
        top_nav_title.config(text=org_name)

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
            values = ctk_prompt(main_area, "Filter Unpaid Membership Fees", fields)
            if not values:
                show_summary_reports_panel(main_area, load_table)
                return
            semester = values["Semester"]
            academic_year = values["Academic Year"]
            cur.execute("""
                SELECT mem_id, concat(surname,', ',first_name,' ', second_name), due_date
                FROM Unpaid 
                WHERE org_name = %s AND semester_issued = %s AND academic_year_issued = %s
            """, (org_name, semester, academic_year))
            rows = cur.fetchall()
            display_report(main_area, rows, ["ID", "Name", "Due Date"])

        elif table_name == "member_dues":
            # 3. Member's unpaid fees for all orgs - needs member surname input
            fields = [
                {"label": "Semester", "type": "combo", "options": ["1st", "2nd"], "default": "1st"},
                {"label": "Academic Year", "type": "entry", "default": "2024-2025"}
            ]
            values = ctk_prompt(main_area, "Filter Member Dues", fields)
            if not values:
                show_summary_reports_panel(main_area, load_table)
                return
            semester = values["Semester"]
            academic_year = values["Academic Year"]
            cur.execute("""
                SELECT * FROM MemberDues 
                WHERE org_name = %s AND academic_year_issued = %s AND semester_issued = %s
            """, (org_name, academic_year, semester))
            rows = cur.fetchall()
            display_report(main_area, rows, ["Org", "ID", "Surname", "First", "Second", "Sem", "Year", "Total Due"])

        elif table_name == "exec":
            # 4. Executives for org and academic year
            fields = [
                {"label": "Academic Year", "type": "entry", "default": "2024-2025"}
            ]
            values = ctk_prompt(main_area, "Filter Executive Committee", fields)
            if not values:
                show_summary_reports_panel(main_area, load_table)
                return
            academic_year = values["Academic Year"]
            cur.execute("""
                SELECT * FROM ExecCommittee 
                WHERE org_name = %s AND academic_year = %s
            """, (org_name, academic_year))
            rows = cur.fetchall()
            if not rows:
                ctk.CTkLabel(main_area, text="No executive committee found for that year.", text_color="red", font=("Arial", 14)).pack(pady=20)
            else:
                display_report(main_area, rows, ["Org", "ID", "Surname", "First", "Second", "Role", "Year"])

        elif table_name == "roles_per_year":
            # 5. Presidents for org, all years reverse order
            cur.execute("""
                SELECT mem_id, concat(surname,', ',first_name,' ', second_name), academic_year, semester 
                FROM RolesPerYear 
                WHERE org_name = %s AND role = 'President' 
                ORDER BY academic_year DESC
            """, (org_name,))
            rows = cur.fetchall()
            display_report(main_area, rows, ["Mem ID", "Name", "Year", "Semester"])

        elif table_name == "late_payments":
            # 6. Late payments for org, semester, academic year
            fields = [
                {"label": "Semester", "type": "combo", "options": ["1st", "2nd"], "default": "1st"},
                {"label": "Academic Year", "type": "entry", "default": "2024-2025"}
            ]
            values = ctk_prompt(main_area, "Filter Late Payments", fields)
            if not values:
                show_summary_reports_panel(main_area, load_table)
                return
            semester = values["Semester"]
            academic_year = values["Academic Year"]
            cur.execute("""
                SELECT mem_id, concat(surname,', ',first_name,' ', second_name), fee_type, amount, academic_year_issued, semester_issued, due_date, date_paid 
                FROM LatePayments 
                WHERE org_name = %s AND semester_issued = %s AND academic_year_issued = %s
            """, (org_name, semester, academic_year))
            rows = cur.fetchall()
            display_report(main_area, rows, ["ID", "Name", "Type", "Amount", "Year", "Semester", "Due Date", "Date Paid"])
        
        elif table_name == "percentage":
            # 7. Active vs inactive percentage for last n semesters
            fields = [
                {"label": "Number of Semesters", "type": "entry", "default": "2"}
            ]
            values = ctk_prompt(main_area, "Filter Active Percentage", fields)
            if not values:
                show_summary_reports_panel(main_area, load_table)
                return
            n_semesters = int(values["Number of Semesters"])

            # Get the last n (semester, academic_year) pairs for this org
            cur.execute("""
                SELECT DISTINCT semester, academic_year
                FROM serves
                WHERE org_id = %s
                ORDER BY academic_year DESC,
                         FIELD(semester, '2nd', '1st', 'Midyear') DESC
                LIMIT %s
            """, (org_id, n_semesters))
            sem_years = cur.fetchall()
            if not sem_years:
                display_report(main_area, [], ["Org", "Semesters", "Active %", "Inactive %"])
                return

            where_clauses = []
            params = []
            for sem, year in sem_years:
                where_clauses.append("(semester = %s AND academic_year = %s)")
                params.extend([sem, year])

            where_sql = " OR ".join(where_clauses)

            # COUNT ACTIVE/INACTIVE PERCENTAGES
            query = f"""
                SELECT
                    (SELECT org_name FROM organization WHERE org_id = %s) AS Org,
                    %s AS Semesters,
                    ROUND(100.0 * SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) / COUNT(*), 2) AS `Active %`,
                    ROUND(100.0 * SUM(CASE WHEN status = 'Inactive' THEN 1 ELSE 0 END) / COUNT(*), 2) AS `Inactive %`
                FROM serves
                WHERE org_id = %s AND ({where_sql})
            """
            params = [org_id, n_semesters, org_id] + params
            cur.execute(query, tuple(params))
            rows = cur.fetchall()
            display_report(main_area, rows, ["Org", "Semesters", "Active %", "Inactive %"])

        elif table_name == "alumni":
            # 8. Alumni as of a given date
            fields = [
                {"label": "Date (YYYY-MM-DD)", "type": "entry", "default": ""}
            ]
            values = ctk_prompt(main_area, "Filter Alumni", fields)
            if not values:
                show_summary_reports_panel(main_area, load_table)
                return
            date_as_of = values["Date (YYYY-MM-DD)"]
            cur.execute("""
                SELECT mem_id, concat(surname,', ',first_name,' ', second_name), academic_year, semester 
                FROM Alumni 
                WHERE org_name = %s AND academic_year <= %s
            """, (org_name, date_as_of)) 
            rows = cur.fetchall()
            display_report(main_area, rows, ["Mem ID", "Name", "Year", "Semester"])
        
        elif table_name == "fee_summary":
            # 9. Total fees paid/unpaid as of a given date
            fields = [
                {"label": "As of Date (YYYY-MM-DD)", "type": "entry", "default": ""}
            ]
            values = ctk_prompt(main_area, "Fee Summary as of Date", fields)
            if not values:
                show_summary_reports_panel(main_area, load_table)
                return
            as_of_date = values["As of Date (YYYY-MM-DD)"]

            # Query: Sum of paid and unpaid fees as of the given date
            cur.execute("""
                SELECT
                    SUM(CASE WHEN status = 'Paid' AND date_paid <= %s THEN amount ELSE 0 END) AS total_paid,
                    SUM(CASE WHEN status = 'Unpaid' AND due_date <= %s THEN amount ELSE 0 END) AS total_unpaid
                FROM fee
                WHERE org_id = %s
            """, (as_of_date, as_of_date, org_id))
            row = cur.fetchone()
            total_paid = row[0] if row[0] else 0
            total_unpaid = row[1] if row[1] else 0

            # Display result
            display_report(
                main_area,
                [(total_paid, total_unpaid)],
                ["Total Paid as of " + as_of_date, "Total Unpaid as of " + as_of_date]
            )

        elif table_name == "highest_debt":
            # Highest debtors for org by semester and academic year
            fields = [
                {"label": "Semester", "type": "combo", "options": ["1st", "2nd"], "default": "1st"},
                {"label": "Academic Year", "type": "entry", "default": "2024-2025"}
            ]
            values = ctk_prompt(main_area, "Filter Highest Debtors", fields)
            if not values:
                show_summary_reports_panel(main_area, load_table)
                return
            semester = values["Semester"]
            academic_year = values["Academic Year"]
            cur.execute("""
                SELECT org_name, mem_id, surname, first_name, second_name, semester_issued, academic_year_issued, total_unpaid
                FROM HighestDebt
                WHERE org_name = %s AND semester_issued = %s AND academic_year_issued = %s
                ORDER BY total_unpaid DESC
            """, (org_name, semester, academic_year))
            rows = cur.fetchall()
            if not rows:
                ctk.CTkLabel(main_area, text="No highest debtors found for that period.", text_color="red", font=("Arial", 14)).pack(pady=20)
            else:
                display_report(main_area, rows, ["Org", "ID", "Surname", "First", "Second", "Semester", "Year", "Total Unpaid"])
    
    load_table("home")

    # SUPERADMIN BACK BUTTON
    if(admin):
        def go_back():
            from superadmin_panel import open_superadmin_panel 
            # Clear current panel
            for widget in root.winfo_children():
                widget.destroy()
            # Reopen superadmin panel
            open_superadmin_panel(root)
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
        back_btn.pack(side="right", padx=5, pady=2, ipady=5, ipadx=2)
        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)

# SUMMARY REPORTS PANEL GUI
def show_summary_reports_panel(root, on_report_click):
    
    for widget in root.winfo_children():
        widget.destroy()

    # HEADER FRAME
    header_frame = ctk.CTkFrame(root, fg_color="#020325")
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
        ("List of Presidents", "roles_per_year"),
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

def ctk_prompt(parent, title, fields):
    result = {}

    popup = ctk.CTkToplevel(parent)
    popup.title(title)
    popup.geometry("350x180")
    popup.grab_set()
    popup.resizable(False, False)

    frame = ctk.CTkFrame(popup, fg_color="white")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    vars = []
    for i, field in enumerate(fields):
        ctk.CTkLabel(frame, text=field["label"] + ":", font=("Arial", 12), text_color="black").grid(row=i, column=0, sticky="w", pady=5)
        if field["type"] == "combo":
            var = ctk.StringVar(value=field.get("default", "Select"))
            combo = ctk.CTkComboBox(frame, variable=var, values=field["options"], width=180)
            combo.grid(row=i, column=1, pady=5)
            vars.append(var)
        else:
            var = ctk.StringVar(value=field.get("default", ""))
            entry = ctk.CTkEntry(frame, textvariable=var, width=180)
            entry.grid(row=i, column=1, pady=5)
            vars.append(var)

    def on_ok():
        for idx, field in enumerate(fields):
            val = vars[idx].get().strip()
            if not val or val == "Select":
                ctk.CTkLabel(frame, text="All fields required.", text_color="red").grid(row=len(fields)+1, column=0, columnspan=2)
                return
            result[field["label"]] = val
        popup.grab_release()
        popup.destroy()

    def on_cancel():
        popup.grab_release()
        popup.destroy()

    btn_frame = ctk.CTkFrame(frame, fg_color="white")
    btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=(10,0))
    ctk.CTkButton(btn_frame, text="OK", command=on_ok, fg_color="#0078D4", text_color="white", width=80).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Cancel", command=on_cancel, fg_color="#c0392b", text_color="white", width=80).pack(side="left", padx=5)

    popup.wait_window()
    return result if result else None
