"""Imports"""
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import customtkinter as ctk

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

    # COLOR SCHEME AND FONTS
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
        tree = ttk.Treeview(parent, columns=columns, show="headings")

        # Create a font object to measure text
        font = tkFont.Font()

        for col in columns:
            tree.heading(col, text=col)

            max_width = font.measure(col)
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
            values = ctk_prompt(main_area, "Filter Member Dues", fields)

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
            values = ctk_prompt(main_area, "Filter Executive Committee", fields)
            
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
            query = """
                SELECT org_id,org_name, mem_id, concat(surname,', ',first_name,' ', second_name), academic_year, semester 
                FROM RolesPerYear 
                WHERE role = 'President' 
                ORDER BY academic_year DESC
            """
            if org_id != 0:
                query = query + "AND org_id = %s"
                cur.execute(query, (org_id,))
            else:
                cur.execute(query)
            rows = cur.fetchall()
            display_report(main_area, rows, ["org ID,","Organization","Mem ID", "Name", "Year", "Semester"])

        elif table_name == "late_payments":
            # 6. Late payments for org, semester, academic year
            fields = [
                {"label": "Semester", "type": "combo", "options": ["1st", "2nd"], "default": "1st"},
                {"label": "Academic Year", "type": "entry", "default": "2024-2025"}
            ]
            values = ctk_prompt(main_area, "Filter Late Payments", fields)
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
            # 7. Active vs inactive percentage for last n semesters
            fields = [
                {"label": "Number of Semesters", "type": "entry", "default": "2"}
            ]
            values = ctk_prompt(main_area, "Filter Active Percentage", fields)
            if not values or not isinstance(values, dict):
                show_summary_reports_panel(main_area, load_table)
                return

            n_semesters = int(values.get("Number of Semesters"))

            # Get last n (semester, year) combinations
            if org_id != 0:
                cur.execute("""
                    SELECT DISTINCT semester, academic_year, org_id
                    FROM percentage
                    WHERE org_id = %s
                    ORDER BY academic_year DESC, 
                            FIELD(semester, '2nd', 'Midyear', '1st')  -- custom semester order
                    LIMIT %s
                """, (org_id, n_semesters))
            else:
                cur.execute("""
                    SELECT DISTINCT semester, academic_year, org_id
                    FROM percentage
                    ORDER BY academic_year DESC, 
                            FIELD(semester, '2nd', 'Midyear', '1st')  -- custom semester order
                    LIMIT %s
                """, (n_semesters,))

            recent_terms = cur.fetchall()
            if not recent_terms:
                ctk.CTkLabel(main_area, text="No data found for that range.", text_color="red", font=("Arial", 14)).pack(pady=20)
                return

            # Fetch all data from those n semesters
            conditions = []
            params = []
            for sem, year in recent_terms:
                conditions.append("(semester = %s AND academic_year = %s)")
                params.extend([sem, year])

            query = "SELECT * FROM percentage WHERE " + " OR ".join(conditions)
            if org_id != 0:
                query += " AND org_id = %s"
                params.append(org_id)

            cur.execute(query, tuple(params))
            rows = cur.fetchall()

            display_report(main_area, rows, ["Organization", "Semester", "Number of Members", "Active Members", "Active %", "Inactive %"])

        elif table_name == "alumni":
            # 8. Alumni as of a given date
            fields = [
                {"label": "Date (YYYY-MM-DD)", "type": "entry", "default": ""}
            ]
            values = ctk_prompt(main_area, "Filter Alumni", fields)
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
            values = ctk_prompt(main_area, "Fee Summary as of Date", fields)
            if not values:
                show_summary_reports_panel(main_area, load_table)
                return

            as_of_date = values.get("As of Date (YYYY-MM-DD)")

            if org_id != 0:
                cur.execute("""
                    SELECT org_id, 
                        SUM(CASE WHEN status = 'Paid' THEN amount ELSE 0 END) AS total_paid,
                        SUM(CASE WHEN status = 'Unpaid' THEN amount ELSE 0 END) AS total_unpaid
                    FROM Fee
                    WHERE date_paid <= %s AND org_id = %s
                """, (as_of_date, org_id))
            else:
                cur.execute("""
                    SELECT
                        SUM(CASE WHEN status = 'Paid' THEN amount ELSE 0 END) AS total_paid,
                        SUM(CASE WHEN status = 'Unpaid' THEN amount ELSE 0 END) AS total_unpaid
                    FROM Fee
                    WHERE date_paid <= %s
                """, (as_of_date,))

            row = cur.fetchone()
            total_paid = row[0] if row and row[0] else 0
            total_unpaid = row[1] if row and row[1] else 0

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


# --- SMOOTH MODAL DIALOG FUNCTION ---
def ctk_prompt(parent, title, fields):
    result = {}

    popup = ctk.CTkToplevel(parent)
    popup.title(title)
    popup.geometry("380x200")
    popup.grab_set()
    popup.resizable(False, False)
    popup.configure(fg_color="white")

    # DIALOGS
    popup.update_idletasks()
    parent.update_idletasks()
    x = parent.winfo_rootx() + (parent.winfo_width() // 2) - 190
    y = parent.winfo_rooty() + (parent.winfo_height() // 2) - 100
    popup.geometry(f"+{x}+{y}")

    frame = ctk.CTkFrame(popup, fg_color="white", corner_radius=15)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    vars = []
    for i, field in enumerate(fields):
        ctk.CTkLabel(frame, text=field["label"] + ":", font=("Arial", 13), text_color="black").grid(row=i, column=0, sticky="w", pady=7, padx=5)
        if field["type"] == "combo":
            var = ctk.StringVar(value=field.get("default", "Select"))
            combo = ctk.CTkComboBox(frame, variable=var, values=field["options"], width=180)
            combo.grid(row=i, column=1, pady=7, padx=5)
            vars.append(var)
        else:
            var = ctk.StringVar(value=field.get("default", ""))
            entry = ctk.CTkEntry(frame, textvariable=var, width=180)
            entry.grid(row=i, column=1, pady=7, padx=5)
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
        popup.grab_release()
        popup.destroy()

    def on_cancel():
        popup.grab_release()
        popup.destroy()

    btn_frame = ctk.CTkFrame(frame, fg_color="white")
    btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=(15,0))
    ctk.CTkButton(btn_frame, text="OK", command=on_ok, fg_color="#0078D4", text_color="white", width=90).pack(side="left", padx=8)
    ctk.CTkButton(btn_frame, text="Cancel", command=on_cancel, fg_color="#c0392b", text_color="white", width=90).pack(side="left", padx=8)

    popup.wait_window()
    return result if result else None