import tkinter as tk
from db_connection import get_connection
from fee import show_fee_table
from members import show_member_table

# Establish database connection
conn = get_connection()
cur = conn.cursor()

def open_president_panel(root, admin, org_name, org_id):
    # Clear root and setup layout
    for widget in root.winfo_children():
        widget.destroy()

    buttons = [
        ("Home", "home"),
        ("Manage Members", "member"),
        ("View Fees", "fee"),
    ]

    # Microsoft-inspired color scheme
    primary_color = "#0078D4"  # Soft blue for primary elements
    button_bg = "#00A4EF"  # Light blue for button background
    button_hover_bg = "#0063B1"  # Darker blue for hover effect
    button_selected_bg = "#005A8D"  # Even darker blue for selected button
    main_area_bg = "#FFFFFF"  # Clean white background for the main content
    title_font = ("Segoe UI", 16, "bold")  # Segoe UI font, commonly used by Microsoft
    button_font = ("Segoe UI", 12)

    top_nav = tk.Frame(root, bg=primary_color, height=40)
    top_nav.pack_propagate(False)  # Prevent shrinking
    top_nav.pack(side="top", fill="x")

    # Title label in the top nav
    top_nav_title = tk.Label(top_nav, text=org_name, fg="white", bg=primary_color, font=title_font)
    top_nav_title.pack(side="left", padx=10)

    def on_enter(e):
        if e.widget["bg"] != button_selected_bg:
            e.widget["bg"] = button_hover_bg  # Darker blue on hover

    def on_leave(e):
        if e.widget["bg"] != button_selected_bg:
            e.widget["bg"] = button_bg  # Default light blue color

    selected_button = None  # Variable to track the selected button

    def button_click(e, table_name):
        nonlocal selected_button
        if selected_button:
            selected_button.config(bg=button_bg)  # Reset previous button color
        e.widget.config(bg=button_selected_bg)  # Set the clicked button to selected color
        selected_button = e.widget  # Update the selected button
        load_table(table_name)  # Load the appropriate table

    # Create buttons
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

    # Main content area with clean white background
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


    # Function to handle switching views
    def load_table(table_name):
        # Clear main content area
        for widget in main_area.winfo_children():
            widget.destroy()
        top_nav_title.config(text=org_name)

        if table_name == "home":
            home_header = tk.Label(main_area, text=org_name,
                                font=("Segoe UI", 40, "bold"), fg="#2C3E50", bg=main_area_bg)
            home_header.pack(pady=10)

            subtext = tk.Label(main_area, text="Manage Members, Fees, and More!",
                            font=("Segoe UI", 14), fg=primary_color, bg=main_area_bg)
            subtext.pack(pady=5)

            # Frame to hold report buttons
            report_frame = tk.Frame(main_area, bg=main_area_bg)
            report_frame.pack(pady=20)

            report_buttons = [
                ("Unpaid Membership Fees", "unpaid"),
                ("Member Dues", "member_dues"),
                ("Executive Committee", "exec"),
                ("List of Presidents", "roles_per_year"),
                ("Late Payments", "late_payments"),
                ("Active %", "percentage"),
                ("Alumni", "alumni"),
                ("Fee Summary", "fee_summary"),
                ("Top Debtors", "highest_debt")
            ]

            def load_report(report_key):
                load_table(report_key)

            for i, (text, key) in enumerate(report_buttons):
                btn = tk.Button(report_frame, text=text, command=lambda k=key: load_report(k),
                                bg=button_bg, fg="white", font=button_font, relief="raised", bd=1, padx=10, pady=5)
                btn.grid(row=i // 2, column=i % 2, padx=10, pady=5, sticky="ew")

        elif table_name == "member":
            show_member_table(main_area, cur, org_id)
        elif table_name == "fee":
            show_fee_table(main_area, cur, org_id)

        # Report view logic
        elif table_name == "unpaid":
            cur.execute("SELECT mem_id, concat(surname,', ',first_name,' ', second_name), due_date FROM Unpaid WHERE org_name = %s", (org_name,))
            rows = cur.fetchall()
            display_report(main_area, rows, ["ID", "Name", "Due Date"])

        elif table_name == "member_dues":
            cur.execute("SELECT org_name, fee_type, amount, due_date FROM Unpaid WHERE surname = 'Mendoza' AND org_name = %s", (org_name,))
            rows = cur.fetchall()
            display_report(main_area, rows, ["Org", "Fee Type", "Amount", "Due Date"])

        elif table_name == "exec":
            cur.execute("SELECT mem_id, concat(surname,', ',first_name,' ', second_name), role, status FROM Exec WHERE org_name = %s", (org_name,))
            rows = cur.fetchall()
            display_report(main_area, rows, ["ID", "Role", "Status"])

        elif table_name == "roles_per_year":
            cur.execute("SELECT mem_id, concat(surname,', ',first_name,' ', second_name), academic_year, semester FROM RolesPerYear WHERE org_name = %s AND role = 'President'", (org_name,))
            rows = cur.fetchall()
            display_report(main_area, rows, ["Mem ID", "Name", "Year", "Semester"])

        elif table_name == "late_payments":
            cur.execute("SELECT mem_id, concat(surname,', ',first_name,' ', second_name), fee_type, amount, academic_year_issued, semester_issued, due_date, date_paid FROM LatePayments WHERE org_name = %s", (org_name,))
            rows = cur.fetchall()
            display_report(main_area, rows, ["ID", "Name", "Type", "Amount", "Year", "Semester", "Due Date", "Date Paid"])

        elif table_name == "percentage":
            cur.execute("SELECT semester, academic_year, num_members, active_members, active_percentage FROM Percentage WHERE org_id = %s ORDER BY academic_year DESC", (org_id,))
            rows = cur.fetchall()
            display_report(main_area, rows, ["Semester", "Year", "Total Members", "# Active", "% Active"])

        elif table_name == "alumni":
            cur.execute("SELECT mem_id, concat(surname,', ',first_name,' ', second_name), academic_year, semester FROM Alumni WHERE org_name = %s", (org_name,))
            rows = cur.fetchall()
            display_report(main_area, rows, ["Mem ID", "Name", "Year", "Semester"])

        elif table_name == "fee_summary":
            cur.execute("SELECT * FROM OrgFeesSummary WHERE org_name = %s", (org_name,))
            rows = cur.fetchall()
            display_report(main_area, rows, ["Org", "Total Paid", "Total Unpaid", "Date Paid"])

        elif table_name == "highest_debt":
            cur.execute("SELECT * FROM HighestDebt WHERE org_name = %s AND academic_year_issued = '2024-2025' AND semester_issued = '2nd'", (org_name,))
            rows = cur.fetchall()
            display_report(main_area, rows, ["Org", "ID", "Surname", "First", "Second", "Sem", "Year", "Total Unpaid"])

    # Load homepage by default
    load_table("home")



    # Back to Superadmin button (right side)
    if(admin):
                # Function to handle going back to superadmin panel
        def go_back():
            # Dynamically import superadmin panel to avoid circular import
            from superadmin_panel import open_superadmin_panel  # <-- Import HERE
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
