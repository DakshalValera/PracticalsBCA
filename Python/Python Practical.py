import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

# Database connection
def connect_db():
    try:
        return mysql.connector.connect(host="localhost", user="root", password="", database="College")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to connect to database:\n{err}")
        return None

# Load data into table
def fetch_data():
    try:
        conn = connect_db()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Student")
        rows = cursor.fetchall()
        
        for row in tree.get_children():
            tree.delete(row)
            
        for row in rows:
            tree.insert("", tk.END, values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to fetch data:\n{err}")
    finally:
        if conn:
            conn.close()

# Add new student
def add_record():
    try:
        if not all([name_var.get(), course_var.get(), sem_var.get(), subject_var.get(), gender_var.get()]):
            messagebox.showwarning("Error", "All fields are required!")
            return
            
        try:
            sem = int(sem_var.get())
        except ValueError:
            messagebox.showwarning("Error", "Semester must be a number!")
            return
            
        gender = "M" if gender_var.get() == "Male" else "F"
            
        conn = connect_db()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Student (Name, Course, Sem, Subject, Gender) VALUES (%s, %s, %s, %s, %s)", 
            (name_var.get(), course_var.get(), sem, subject_var.get(), gender)
        )
        conn.commit()
        clear_fields()
        fetch_data()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to add record:\n{err}")
    finally:
        if conn:
            conn.close()

# Update selected student
def update_record():
    try:
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Error", "Select a record to update")
            return
            
        if not all([name_var.get(), course_var.get(), sem_var.get(), subject_var.get(), gender_var.get()]):
            messagebox.showwarning("Error", "All fields are required!")
            return
            
        try:
            sem = int(sem_var.get())
        except ValueError:
            messagebox.showwarning("Error", "Semester must be a number!")
            return
            
        gender = "M" if gender_var.get() == "Male" else "F"
            
        values = tree.item(selected, "values")
        conn = connect_db()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Student SET Name=%s, Course=%s, Sem=%s, Subject=%s, Gender=%s WHERE _id=%s", 
            (name_var.get(), course_var.get(), sem, subject_var.get(), gender, values[0])
        )
        conn.commit()
        clear_fields()
        fetch_data()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to update record:\n{err}")
    finally:
        if conn:
            conn.close()

# Delete selected student
def delete_record():
    conn = None
    try:
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Error", "Select a record to delete")
            return
            
        values = tree.item(selected, "values")
        if not messagebox.askyesno("Confirm", "Delete this record?"):
            return
            
        conn = connect_db()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Student WHERE _id=%s", (values[0],))
        conn.commit()
        clear_fields()
        fetch_data()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to delete record:\n{err}")
    finally:
        if conn:
            conn.close()

# Clear input fields
def clear_fields():
    name_var.set("")
    course_var.set("")
    sem_var.set("")
    subject_var.set("")
    gender_var.set("")

# Fill form with selected record
def on_tree_select(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, "values")
        name_var.set(values[1])
        course_var.set(values[2])
        sem_var.set(values[3])
        subject_var.set(values[4])
        gender_var.set("Male" if values[5] == "M" else "Female")

# Setup main window
root = tk.Tk()
root.title("Student Database")
root.geometry("700x500")

# Create variables
name_var = tk.StringVar()
course_var = tk.StringVar()
sem_var = tk.StringVar()
subject_var = tk.StringVar()
gender_var = tk.StringVar()

# Setup input form
input_frame = tk.Frame(root, pady=10)
input_frame.pack()

# Input fields
tk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=2)
tk.Entry(input_frame, textvariable=name_var, width=25).grid(row=0, column=1, padx=5, pady=2)

tk.Label(input_frame, text="Course:").grid(row=1, column=0, padx=5, pady=2)
tk.Entry(input_frame, textvariable=course_var, width=25).grid(row=1, column=1, padx=5, pady=2)

tk.Label(input_frame, text="Semester:").grid(row=2, column=0, padx=5, pady=2)
tk.Entry(input_frame, textvariable=sem_var, width=25).grid(row=2, column=1, padx=5, pady=2)

tk.Label(input_frame, text="Subject:").grid(row=3, column=0, padx=5, pady=2)
tk.Entry(input_frame, textvariable=subject_var, width=25).grid(row=3, column=1, padx=5, pady=2)

tk.Label(input_frame, text="Gender:").grid(row=4, column=0, padx=5, pady=2)
gender_combo = ttk.Combobox(input_frame, textvariable=gender_var, values=["Male", "Female"], width=22, state="readonly")
gender_combo.grid(row=4, column=1, padx=5, pady=2)

# Setup buttons
button_frame = tk.Frame(root, pady=10)
button_frame.pack()

# Action buttons
tk.Button(button_frame, text="Add", command=add_record, width=8).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Update", command=update_record, width=8).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Delete", command=delete_record, width=8).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Clear", command=clear_fields, width=8).pack(side=tk.LEFT, padx=5)

# Setup table
tree = ttk.Treeview(root, columns=("_id", "Name", "Course", "Sem", "Subject", "Gender"), show="headings", height=10)
tree.heading("_id", text="ID")
tree.heading("Name", text="Name")
tree.heading("Course", text="Course")
tree.heading("Sem", text="Semester")
tree.heading("Subject", text="Subject")
tree.heading("Gender", text="Gender")

tree.column("_id", width=50)
tree.column("Name", width=150)
tree.column("Course", width=150)
tree.column("Sem", width=80)
tree.column("Subject", width=150)
tree.column("Gender", width=80)

tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Add scrollbar
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar.set)

# Bind tree selection
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Load initial data
fetch_data()

# Start main loop
root.mainloop()