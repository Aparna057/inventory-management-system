import tkinter as tk
from tkinter import messagebox
import sqlite3
from dashboard import Dashboard
from theme import apply_theme

def LoginScreen(root):
    for widget in root.winfo_children():
        widget.destroy()
    
    theme = apply_theme(root, "Light Green")

    tk.Label(root, text="Inventory Management System", font=("Arial", 28, "bold"),
             bg=theme["bg"], fg=theme["fg"]).pack(pady=20)

    frame = tk.Frame(root, bg=theme["bg"])
    frame.pack()

    tk.Label(frame, text="Username", bg=theme["bg"], fg=theme["fg"]).grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(frame)
    username_entry.grid(row=0, column=1)

    tk.Label(frame, text="Password", bg=theme["bg"], fg=theme["fg"]).grid(row=1, column=0, padx=10)
    password_entry = tk.Entry(frame, show="*")
    password_entry.grid(row=1, column=1)

    def login():
        user = username_entry.get()
        pwd = password_entry.get()
        conn = sqlite3.connect("ims.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE username=? AND password=?", (user, pwd))
        if cur.fetchone():
            Dashboard(root, "Light Green")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
        conn.close()

    def open_change_password_popup():
        popup = tk.Toplevel(root)
        popup.title("Change Password")
        popup.geometry("300x250")
        popup.grab_set()

        tk.Label(popup, text="Username").pack(pady=5)
        user_entry = tk.Entry(popup)
        user_entry.pack()

        tk.Label(popup, text="Old Password").pack(pady=5)
        old_pass_entry = tk.Entry(popup, show="*")
        old_pass_entry.pack()

        tk.Label(popup, text="New Password").pack(pady=5)
        new_pass_entry = tk.Entry(popup, show="*")
        new_pass_entry.pack()

        tk.Label(popup, text="Confirm Password").pack(pady=5)
        confirm_pass_entry = tk.Entry(popup, show="*")
        confirm_pass_entry.pack()

        def update_password():
            username = user_entry.get()
            old_pass = old_pass_entry.get()
            new_pass = new_pass_entry.get()
            confirm_pass = confirm_pass_entry.get()

            if new_pass != confirm_pass:
                messagebox.showerror("Error", "New passwords do not match!")
                return

            conn = sqlite3.connect("ims.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, old_pass))
            if cur.fetchone():
                cur.execute("UPDATE admin SET password=? WHERE username=?", (new_pass, username))
                conn.commit()
                messagebox.showinfo("Success", "Password changed successfully.")
                popup.destroy()
            else:
                messagebox.showerror("Error", "Invalid old password or username.")
            conn.close()

        tk.Button(popup, text="Update Password", command=update_password, bg="green", fg="white").pack(pady=10)

    tk.Button(frame, text="Login", command=login, bg="green", fg="white", width=20).grid(row=2, columnspan=2, pady=10)
    tk.Button(frame, text="Change Password", command=open_change_password_popup, bg="blue", fg="white", width=20).grid(row=3, columnspan=2, pady=5)
