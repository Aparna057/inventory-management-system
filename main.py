import tkinter as tk
from db import init_db
from auth import LoginScreen

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Inventory Management System")
    root.geometry("1200x700")
    init_db()
    LoginScreen(root)
    root.mainloop()
