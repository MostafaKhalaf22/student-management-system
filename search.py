import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
# search student by name or id
class SearchWindow:
    def __init__(self, parent, refresh_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Search Student")
        self.window.geometry("600x400")
        self.refresh_callback = refresh_callback
        self.build_ui()

    def build_ui(self):
        tk.Label(self.window, text="Search Student",
                 font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(self.window)
        frame.pack(pady=5)

        tk.Label(frame, text="Search by Name or ID:",
                 font=("Arial", 11)).grid(row=0, column=0, padx=5)
        self.search_entry = tk.Entry(frame, font=("Arial", 11), width=25)
        self.search_entry.grid(row=0, column=1, padx=5)

        tk.Button(frame, text="Search", bg="blue", fg="white",
                  font=("Arial", 11),
                  command=self.search).grid(row=0, column=2, padx=5)

        columns = ("ID", "Name", "Student ID", "Major")
        self.tree = ttk.Treeview(self.window, columns=columns,
                                  show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        tk.Button(self.window, text="Edit Selected Student",
                  bg="green", fg="white", font=("Arial", 11),
                  command=self.edit_student).pack(pady=5)

    def search(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a name or ID!")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM students
            WHERE name LIKE ? OR student_id LIKE ?
        """, (f"%{query}%", f"%{query}%"))
        results = cursor.fetchall()
        conn.close()

        if results:
            for row in results:
                self.tree.insert("", tk.END, values=row)
        else:
            messagebox.showinfo("Info", "No students found!")

    def edit_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student first!")
            return
        student = self.tree.item(selected[0])["values"]
        from edit_student import EditStudentWindow
        EditStudentWindow(self.window, student, self.refresh_callback)