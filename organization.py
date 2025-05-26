import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Show the Organization Table UI
def show_organization_table(root, cur):
    # Frame for filter + tools
    top_frame = tk.Frame(root, pady=10)
    top_frame.pack(fill="x")

    # --- Filter section (left) ---
    filter_frame = tk.Frame(top_frame)
    filter_frame.pack(side="left", fill="x", expand=True)

    org_name_var = tk.StringVar()
    org_type_var = tk.StringVar(value="Select")
    sort_var = tk.StringVar(value="Sort by")

    tk.Label(filter_frame, text="Organization Name:").grid(row=0, column=0, padx=5)
    tk.Entry(filter_frame, textvariable=org_name_var, width=20).grid(row=0, column=1, padx=5)

    tk.Label(filter_frame, text="Organization Type:").grid(row=0, column=2, padx=5)
    org_types = get_org_types(cur)
    tk.OptionMenu(filter_frame, org_type_var, "Select", *org_types).grid(row=0, column=3, padx=5)

    def apply_org_filters():
        filters = {}
        if org_name_var.get():
            filters["org_name"] = org_name_var.get()
        if org_type_var.get() != "Select":
            filters["org_type"] = org_type_var.get()
        refresh_org_table(root, cur, filters, sort_var.get())

    tk.Button(filter_frame, text="Apply Filters", command=apply_org_filters).grid(row=0, column=4, padx=10)

    # --- Right tools section (Sort + Reset) ---
    right_tools_frame = tk.Frame(top_frame)
    right_tools_frame.pack(side="right")

    tk.Label(right_tools_frame, text="Sort by:").pack(side="left", padx=5)
    sort_options = ["org_id", "org_name", "type"]

    def on_sort_select(selected_col):
        if selected_col != "Sort by":
            refresh_org_table(root, cur, {}, selected_col)

    tk.OptionMenu(right_tools_frame, sort_var, *sort_options, command=on_sort_select).pack(side="left")

    def reset_org_filters():
        org_name_var.set("")
        org_type_var.set("Select")
        sort_var.set("Sort by")
        refresh_org_table(root, cur, {}, "")

    tk.Button(right_tools_frame, text="🔄", font=("Arial", 12), command=reset_org_filters).pack(side="left", padx=10)

    # --- Treeview Table Section ---
    tree_frame = tk.Frame(root)
    tree_frame.pack(fill="both", expand=True)

    columns = ("org_id", "org_name", "type")  # Defined columns for the organization table
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    # Set column headings and column width
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    root.tree = tree

    # Buttons frame
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Add Delete Button
    def delete_selected():
        selected = root.tree.selection()
        if not selected:
            return  # No item selected
        confirm = messagebox.askyesno("Delete", "Are you sure you want to delete the selected organization?")
        if not confirm:
            return

        for item in selected:
            values = root.tree.item(item, "values")
            org_id = values[0]  # Assuming Org id is the first column

            # Execute delete query
            cur.execute("DELETE FROM fee WHERE org_id = %s", (org_id,))
            cur.execute("DELETE FROM serves WHERE org_id = %s", (org_id,))
            cur.execute("DELETE FROM organization WHERE org_id = %s", (org_id,))

        # Commit the change to database
        cur.connection.commit()

        # Refresh table after deletion
        refresh_org_table(root, cur, {}, "")

    # Edit Button
    def edit_selected():
        selected = root.tree.selection()
        if not selected:
            return  # No item selected
        item = selected[0]
        values = root.tree.item(item, "values")
        org_id = values[0]  # Assuming org_id is the first column

        # Fetch the selected organization's details
        cur.execute("SELECT * FROM organization WHERE org_id = %s", (org_id,))
        org = cur.fetchone()

        def save_changes():
            # Collect updated values from the entry fields
            org_name = org_name_var.get()
            org_type = org_type_var.get()

            try:
                cur.execute("""
                    UPDATE organization SET
                        org_name = %s,
                        type = %s
                    WHERE org_id = %s
                """, (org_name, org_type, org_id))
                cur.connection.commit()

                # Refresh the organization table after the update
                refresh_org_table(root, cur, {}, "")
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Create a new window to edit organization details
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Organization")

        # Create Tkinter StringVars to store the organization data
        org_name_var = tk.StringVar(value=org[1])  # org_name is the second column
        org_type_var = tk.StringVar(value=org[2])  # org_type is the third column

        # Entry fields for organization data
        entries = [
            ("Organization Name", org_name_var),
            ("Organization Type", org_type_var),
        ]

        for idx, (label, var) in enumerate(entries):
            tk.Label(edit_window, text=label).grid(row=idx, column=0, padx=5)
            tk.Entry(edit_window, textvariable=var).grid(row=idx, column=1, padx=5)

        tk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=len(entries), column=0, columnspan=2, pady=10)

    # Final buttons
    tk.Button(button_frame, text="Edit Selected ✏️", command=edit_selected).pack(side="left", padx=10)
    tk.Button(button_frame, text="Delete Selected 🔴", command=delete_selected, fg="red").pack(side="left", padx=10)

    refresh_org_table(root, cur, {}, "")  # Load initial table

# Fetch distinct org types for dropdown
def get_org_types(cur):
    cur.execute("SELECT DISTINCT type FROM organization")
    return [row[0] for row in cur.fetchall()]

# Refresh data in the organization table
def refresh_org_table(root, cur, filters, sort_by):
    query = "SELECT org_id, org_name, type FROM organization WHERE 1=1"

    if filters.get("org_name"):
        query += f" AND org_name LIKE '%{filters['org_name']}%'"
    if filters.get("org_type"):
        query += f" AND type = '{filters['org_type']}'"

    if sort_by and sort_by != "Sort by":
        query += f" ORDER BY {sort_by}"

    cur.execute(query)
    organizations = cur.fetchall()

    # Clear current data
    for row in root.tree.get_children():
        root.tree.delete(row)

    # Insert new data
    for org in organizations:
        root.tree.insert("", "end", values=org)