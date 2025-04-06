import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# === DATABASE SETUP ===
def initialize_database():
    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birthday TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            address TEXT,
            preferred_contact_method TEXT CHECK(preferred_contact_method IN ('email', 'phone', 'mail')) NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# === SUBMIT FUNCTION ===
def submit_data():
    name = name_var.get().strip()
    birthday = birthday_var.get().strip()
    email = email_var.get().strip()
    phone = phone_var.get().strip()
    address = address_text.get("1.0", tk.END).strip()
    preferred_contact = contact_method_var.get().lower()

    # Basic validation
    if not all([name, birthday, email, preferred_contact]):
        messagebox.showwarning("Missing Info", "Please fill in all required fields.")
        return

    try:
        # Validate birthday format
        datetime.strptime(birthday, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Invalid Date", "Birthday must be in YYYY-MM-DD format.")
        return

    try:
        conn = sqlite3.connect("customers.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO customers (name, birthday, email, phone, address, preferred_contact_method)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, birthday, email, phone, address, preferred_contact))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Customer data submitted successfully!")
        clear_form()
    except sqlite3.IntegrityError as e:
        messagebox.showerror("Integrity Error", f"{e}")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

# === CLEAR FORM FUNCTION ===
def clear_form():
    name_var.set("")
    birthday_var.set("")
    email_var.set("")
    phone_var.set("")
    address_text.delete("1.0", tk.END)
    contact_method_var.set("Email")

# === GUI SETUP ===
initialize_database()
root = tk.Tk()
root.title("Customer Information Form")
root.geometry("400x500")
root.resizable(False, False)

# Variables
name_var = tk.StringVar()
birthday_var = tk.StringVar()
email_var = tk.StringVar()
phone_var = tk.StringVar()
contact_method_var = tk.StringVar(value="Email")

# Widgets
tk.Label(root, text="Customer Name *").pack(anchor='w', padx=10, pady=(10, 0))
tk.Entry(root, textvariable=name_var).pack(fill='x', padx=10)

tk.Label(root, text="Birthday (YYYY-MM-DD) *").pack(anchor='w', padx=10, pady=(10, 0))
tk.Entry(root, textvariable=birthday_var).pack(fill='x', padx=10)

tk.Label(root, text="Email *").pack(anchor='w', padx=10, pady=(10, 0))
tk.Entry(root, textvariable=email_var).pack(fill='x', padx=10)

tk.Label(root, text="Phone").pack(anchor='w', padx=10, pady=(10, 0))
tk.Entry(root, textvariable=phone_var).pack(fill='x', padx=10)

tk.Label(root, text="Address").pack(anchor='w', padx=10, pady=(10, 0))
address_text = tk.Text(root, height=4)
address_text.pack(fill='x', padx=10)

tk.Label(root, text="Preferred Contact Method *").pack(anchor='w', padx=10, pady=(10, 0))
ttk.Combobox(root, textvariable=contact_method_var, values=["Email", "Phone", "Mail"], state="readonly").pack(fill='x', padx=10)

tk.Button(root, text="Submit", command=submit_data, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20)

root.mainloop()
