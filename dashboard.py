import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
from theme import apply_theme, themes

def Dashboard(root, current_theme="Light Green"):
    for widget in root.winfo_children():
        widget.destroy()

    theme = apply_theme(root, current_theme)

    def refresh_table():
        for item in tree.get_children():
            tree.delete(item)
        conn = sqlite3.connect("ims.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory")
        for row in cur.fetchall():
            inventory_value = row[2] * row[3]
            tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], inventory_value, row[5]))
            if row[2] < row[4]:
                messagebox.showwarning("Low Stock Alert", f"Low stock for {row[1]}")
        conn.close()

    def add_product():
        name = name_entry.get()
        qty = int(qty_entry.get())
        price = float(price_entry.get())
        reorder = int(reorder_entry.get())
        date = datetime.now().strftime("%Y-%m-%d")
        conn = sqlite3.connect("ims.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO inventory (name, quantity, price, reorder_quantity, date_added) VALUES (?, ?, ?, ?, ?)",
                    (name, qty, price, reorder, date))
        conn.commit()
        conn.close()
        refresh_table()

    def delete_product():
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            product_id = item["values"][0]
            conn = sqlite3.connect("ims.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM inventory WHERE id=?", (product_id,))
            conn.commit()
            conn.close()
            refresh_table()

    def export_data():
        file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if file_path:
            conn = sqlite3.connect("ims.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM inventory")
            data = cur.fetchall()
            with open(file_path, "w") as f:
                f.write("Inventory ID,Name,Quantity,Price,Reorder Quantity,Inventory Value,Date Added\n")
                for row in data:
                    value = row[2] * row[3]
                    f.write(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{value},{row[5]}\n")
            conn.close()
            messagebox.showinfo("Exported", "Data exported successfully!")

    def search_product(*args):
        keyword = search_var.get().lower()
        for item in tree.get_children():
            tree.delete(item)
        conn = sqlite3.connect("ims.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory WHERE LOWER(name) LIKE ?", ('%' + keyword + '%',))
        for row in cur.fetchall():
            value = row[2] * row[3]
            tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], value, row[5]))
        conn.close()

    def change_theme(new_theme):
        Dashboard(root, new_theme)

    # UI Layout
    tk.Label(root, text="Inventory Management System", font=("Arial", 26, "bold"), bg=theme["bg"], fg=theme["fg"]).pack(pady=10)

    control_frame = tk.Frame(root, bg=theme["bg"])
    control_frame.pack(pady=10)

    tk.Label(control_frame, text="Name", bg=theme["bg"]).grid(row=0, column=0)
    name_entry = tk.Entry(control_frame)
    name_entry.grid(row=0, column=1)

    tk.Label(control_frame, text="Qty", bg=theme["bg"]).grid(row=0, column=2)
    qty_entry = tk.Entry(control_frame)
    qty_entry.grid(row=0, column=3)

    tk.Label(control_frame, text="Price", bg=theme["bg"]).grid(row=0, column=4)
    price_entry = tk.Entry(control_frame)
    price_entry.grid(row=0, column=5)

    tk.Label(control_frame, text="Reorder Qty", bg=theme["bg"]).grid(row=0, column=6)
    reorder_entry = tk.Entry(control_frame)
    reorder_entry.grid(row=0, column=7)

    tk.Button(control_frame, text="Add Product", command=add_product, bg="green", fg="white").grid(row=0, column=8, padx=5)
    tk.Button(control_frame, text="Delete", command=delete_product, bg="red", fg="white").grid(row=0, column=9)
    tk.Button(control_frame, text="Export", command=export_data).grid(row=0, column=10)

    search_var = tk.StringVar()
    search_var.trace("w", search_product)
    tk.Entry(root, textvariable=search_var, width=40).pack(pady=5)
    
    theme_option = ttk.Combobox(root, values=list(themes.keys()))
    theme_option.set(current_theme)
    theme_option.pack(pady=5)
    theme_option.bind("<<ComboboxSelected>>", lambda e: change_theme(theme_option.get()))

    columns = ("Inventory ID", "Name", "Quantity in Stock", "Unit Price", "Reorder Quantity", "Inventory Value", "Date Added")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=140)
    tree.pack(expand=True, fill="both", padx=20, pady=10)

    refresh_table()
