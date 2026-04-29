import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

class GradesWindow:
    def __init__(self, parent, student_id):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Grades - Student {student_id}")
        self.window.geometry("500x450")
        self.student_id = student_id
        self.build_ui()
        self.load_grades()

    def build_ui(self):
        tk.Label(self.window, text="Student Grades",
                 font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(self.window)
        frame.pack(pady=5)

        tk.Label(frame, text="Subject:",
                 font=("Arial", 11)).grid(row=0, column=0, padx=5)
        self.subject_entry = tk.Entry(frame, font=("Arial", 11), width=15)
        self.subject_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Grade:",
                 font=("Arial", 11)).grid(row=0, column=2, padx=5)
        self.grade_entry = tk.Entry(frame, font=("Arial", 11), width=8)
        self.grade_entry.grid(row=0, column=3, padx=5)

        tk.Button(self.window, text="Add Grade", bg="green", fg="white",
                  font=("Arial", 11), command=self.add_grade).pack(pady=5)

        columns = ("Subject", "Grade")
        self.tree = ttk.Treeview(self.window, columns=columns,
                                  show="headings", height=10)
        self.tree.heading("Subject", text="Subject")
        self.tree.heading("Grade", text="Grade")
        self.tree.column("Subject", width=200)
        self.tree.column("Grade", width=100)
        self.tree.pack(pady=10)

        self.avg_label = tk.Label(self.window, text="Average: -",
                                   font=("Arial", 12, "bold"))
        self.avg_label.pack(pady=5)

        tk.Button(self.window, text="Delete Selected Grade",
                  bg="red", fg="white", font=("Arial", 10),
                  command=self.delete_grade).pack(pady=5)

    def load_grades(self):
        if not self.window.winfo_exists():
            return
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT subject, grade FROM grades WHERE student_id=?",
                       (self.student_id,))
        grades = cursor.fetchall()
        conn.close()

        total = 0
        for row in grades:
            self.tree.insert("", tk.END, values=row)
            total += row[1]

        if grades:
            avg = total / len(grades)
            self.avg_label.config(text=f"Average: {avg:.2f}")
        else:
            self.avg_label.config(text="Average: -")

    def add_grade(self):
        subject = self.subject_entry.get().strip()
        grade = self.grade_entry.get().strip()

        if not subject or not grade:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        try:
            grade = float(grade)
            if grade < 0 or grade > 100:
                messagebox.showwarning("Warning", "Grade must be between 0 and 100!")
                return
        except ValueError:
            messagebox.showerror("Error", "Grade must be a number!")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)",
                       (self.student_id, subject, grade))
        conn.commit()
        conn.close()

        self.subject_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)
        self.load_grades()

    def delete_grade(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a grade first!")
            return

        item = self.tree.item(selected[0])["values"]
        confirm = messagebox.askyesno("Confirm", f"Delete {item[0]} grade?")
        if confirm:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM grades WHERE student_id=? AND subject=?",
                           (self.student_id, item[0]))
            conn.commit()
            conn.close()
            if self.window.winfo_exists():
                self.load_grades()