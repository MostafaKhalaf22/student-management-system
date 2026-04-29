import tkinter as tk
from tkinter import messagebox
import hashlib
from database import get_connection, init_db

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        init_db()
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Student Management System",
                 font=("Arial", 14, "bold")).pack(pady=20)
        tk.Label(self.root, text="Username:",
                 font=("Arial", 11)).pack()
        self.username_entry = tk.Entry(self.root, font=("Arial", 11))
        self.username_entry.pack(pady=5)
        tk.Label(self.root, text="Password:",
                 font=("Arial", 11)).pack()
        self.password_entry = tk.Entry(self.root, show="*",
                                       font=("Arial", 11))
        self.password_entry.pack(pady=5)
        tk.Button(self.root, text="Login", font=("Arial", 11),
                  bg="blue", fg="white",
                  command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed = hashlib.sha256(password.encode()).hexdigest()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                       (username, hashed))
        user = cursor.fetchone()
        conn.close()
        if user:
            self.root.destroy()
            from dashboard import open_dashboard
            open_dashboard()
        else:
            messagebox.showerror("Error", "Wrong username or password!")