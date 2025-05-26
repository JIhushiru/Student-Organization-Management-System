import tkinter as tk
from tkinter import ttk, messagebox
from authentication import hash_password
from db_connection import get_connection
from president_panel import open_president_panel
import mariadb

BUTTON_COLOR = "#020325"
BUTTON_TEXT_COLOR = "white"
TITLE_FONT = ("Arial", 12, "bold")
ITEMS_PER_PAGE = 9  # 3 columns * 3 rows

def open_superadmin_panel(root):
    root.title("Admin View")
    root.geometry("1300x650")
    root.configure(bg="white")

    style = ttk.Style()
    style.theme_use('default')
    style.configure('TLabel', background='white', font=('Arial', 10))
    style.configure('Header.TLabel', background='white', font=('Palatino Linotype', 40, 'bold'), foreground=BUTTON_COLOR)

    header = ttk.Label(root, text="ORGANIZATIONS DASHBOARD", style='Header.TLabel')
    header.pack(pady=10)

    # Top Buttons
    top_button_frame = ttk.Frame(root)
    top_button_frame.pack(pady=10)

    def show_add_org_form():
        add_window = tk.Toplevel(root)
        add_window.title("Add New Organization")
        add_window.geometry("300x200")
        add_window.configure(bg="white")

        form_frame = ttk.Frame(add_window)
        form_frame.pack(padx=20, pady=20)

        ttk.Label(form_frame, text="Organization Name:").grid(row=0, column=0, sticky="w", pady=5)
        org_name_entry = ttk.Entry(form_frame, width=25)
        org_name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Organization Type:").grid(row=1, column=0, sticky="w", pady=5)
        org_type_entry = ttk.Entry(form_frame, width=25)
        org_type_entry.grid(row=1, column=1, pady=5)

        def submit_org():
            org_name = org_name_entry.get().strip()
            org_type = org_type_entry.get().strip()
            if not org_name or not org_type:
                messagebox.showwarning("Input Error", "All fields are required.")
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO ORGANIZATION (org_name, type) VALUES (?, ?)", (org_name, org_type))
                conn.commit()
                messagebox.showinfo("Success", f"'{org_name}' added successfully!")
                add_window.destroy()
                refresh_data()
            except mariadb.Error as e:
                messagebox.showerror("Database Error", f"Failed to add organization:\n{e}")
            finally:
                if cursor: cursor.close()
                if conn: conn.close()

        ttk.Button(form_frame, text="Add Organization", command=submit_org).grid(row=2, column=0, columnspan=2, pady=15)

    def show_delete_org_dialog():
        delete_window = tk.Toplevel(root)
        delete_window.title("Delete Organization")
        delete_window.geometry("350x150")
        delete_window.configure(bg="white")

        tk.Label(delete_window, text="Select an organization to delete:",
                 bg="white", font=("Arial", 10)).pack(pady=10)

        org_var = tk.StringVar()
        org_dropdown = ttk.Combobox(delete_window, textvariable=org_var, state="readonly", width=35)
        org_dropdown['values'] = [f"{name} (ID: {oid})" for oid, name in organizations]
        org_dropdown.pack(pady=5)

        def delete_selected():
            selected = org_var.get()
            if not selected:
                messagebox.showwarning("Selection Error", "Please select an organization to delete.")
                return
            org_id = int(selected.split("ID: ")[1].rstrip(")"))
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this organization?")
            if confirm:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM organization WHERE org_id = ?", (org_id,))
                    conn.commit()
                    messagebox.showinfo("Deleted", "Organization deleted successfully.")
                    delete_window.destroy()
                    refresh_data()
                except mariadb.Error as e:
                    messagebox.showerror("Database Error", f"Failed to delete organization:\n{e}")
                finally:
                    if cursor: cursor.close()
                    if conn: conn.close()

        ttk.Button(delete_window, text="Delete", command=delete_selected).pack(pady=10)

    # Place all three buttons in the top row
    tk.Button(top_button_frame, text="+ Add Organization", command=show_add_org_form,
              bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=("Arial", 10), padx=12, pady=6).pack(side="left", padx=10)

    tk.Button(top_button_frame, text="Manage All Organizations",
              command=lambda: open_president_panel(root, True, "All", 0),
              bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=("Arial", 10), padx=12, pady=6).pack(side="left", padx=10)

    tk.Button(top_button_frame, text="Delete Organization", command=show_delete_org_dialog,
              bg="#c0392b", fg="white", font=("Arial", 10), padx=12, pady=6).pack(side="left", padx=10)

    # Organization Frame
    org_frame = tk.Frame(root, bg="white")
    org_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Pagination Frame
    pagination_frame = tk.Frame(root, bg="white")
    pagination_frame.pack(pady=5)

    organizations = []
    current_page = [0]

    def fetch_organizations():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT org_id, org_name FROM organization ORDER BY org_name ASC")
        orgs = cur.fetchall()
        conn.close()
        return orgs

    def set_page(page_num):
        current_page[0] = page_num
        populate_organization_buttons()

    def refresh_data():
        nonlocal organizations
        organizations = fetch_organizations()
        set_page(0)

    def populate_organization_buttons():
        for widget in org_frame.winfo_children():
            widget.destroy()
        for widget in pagination_frame.winfo_children():
            widget.destroy()

        if not organizations:
            return

        total_orgs = len(organizations)
        total_pages = (total_orgs + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        page = current_page[0]

        start_index = page * ITEMS_PER_PAGE
        end_index = min(start_index + ITEMS_PER_PAGE, total_orgs)
        current_orgs = organizations[start_index:end_index]

        cols = 3
        for index, (org_id, org_name) in enumerate(current_orgs):
            row, col = divmod(index, cols)
            btn = tk.Button(org_frame, text=org_name,
                            command=lambda oid=org_id, oname=org_name: open_president_panel(root, True, oname, oid),
                            bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=TITLE_FONT,
                            width=25, height=4, relief="flat")
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        for c in range(cols):
            org_frame.grid_columnconfigure(c, weight=1)

        if total_pages > 1:
            if page > 0:
                tk.Button(pagination_frame, text="Previous", command=lambda: set_page(page - 1),
                          bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=("Arial", 10)).pack(side="left", padx=5)
            tk.Label(pagination_frame, text=f"Page {page + 1} of {total_pages}",
                     font=("Arial", 10), bg="white").pack(side="left", padx=10)
            if page < total_pages - 1:
                tk.Button(pagination_frame, text="Next", command=lambda: set_page(page + 1),
                          bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=("Arial", 10)).pack(side="left", padx=5)

    # Initial load
    refresh_data()

    def on_close():
        root.grab_release()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.wait_window()
