import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_table():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS students
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT,
                          age TEXT)''')
        conn.commit()
        conn.close()
        print("Database and table created successfully")  # Debug print
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")  # Debug print
        messagebox.showerror("Database Error", f"Failed to create database: {e}")

def insert_data():
    name = name_entry.get()
    age = age_entry.get()
    
    if name and age:
        try:
            print(f"Attempting to insert: Name={name}, Age={age}")  # Debug print
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO students (name, age) VALUES (?, ?)', (name, age))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data inserted successfully!")
            clear_entries()
            show_data()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")  # Debug print
            messagebox.showerror("Error", f"Failed to insert data: {e}")
    else:
        print(f"Empty fields: Name={name}, Age={age}")  # Debug print
        messagebox.showwarning("Error", "Please fill all fields")

def update_data():
    if not id_entry.get():
        messagebox.showwarning("Error", "Please select a record to update")
        return
        
    id = id_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    
    if name and age:
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE students SET name=?, age=? WHERE id=?', (name, age, id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data updated successfully!")
            clear_entries()
            show_data()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to update data: {e}")
    else:
        messagebox.showwarning("Error", "Please fill all fields")

def delete_data():
    if not id_entry.get():
        messagebox.showwarning("Error", "Please select a record to delete")
        return

    if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM students WHERE id=?', (id_entry.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data deleted successfully!")
            clear_entries()
            show_data()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to delete data: {e}")

def show_data(show_message=False):
    # Clear current display
    display_text.delete(1.0, tk.END)
    
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students')
        data = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to retrieve data: {e}")
        return
        
    if not data:
        if show_message:  # Only show dialog if explicitly requested
            messagebox.showinfo("No Records", "No records found in the database!")
        display_text.insert(tk.END, "No records found.\n")
        return
        
    # Show all records
    for record in data:
        display_text.insert(tk.END, f"ID: {record[0]}, Name: {record[1]}, Age: {record[2]}\n")

def select_record(event=None):
    # Get the line clicked
    line = display_text.get("current linestart", "current lineend")
    if line and "ID:" in line:
        try:
            # Extract ID from the line
            id = line.split(',')[0].split(':')[1].strip()
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students WHERE id=?', (id,))
            record = cursor.fetchone()
            conn.close()
            
            if record:
                # Fill the entry fields with the selected record
                id_entry.delete(0, tk.END)
                name_entry.delete(0, tk.END)
                age_entry.delete(0, tk.END)
                
                id_entry.insert(0, record[0])
                name_entry.insert(0, record[1])
                age_entry.insert(0, record[2])
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to select record: {e}")

def clear_entries():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)

# Create main window
root = tk.Tk()
root.title("Student Database - CRUD Operations")
root.geometry("400x600")

# Create database table
create_table()

# Create input fields
tk.Label(root, text="ID (Auto-filled):").pack(pady=5)
id_entry = tk.Entry(root)
id_entry.pack(pady=5)

tk.Label(root, text="Name:").pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

tk.Label(root, text="Age:").pack(pady=5)
age_entry = tk.Entry(root)
age_entry.pack(pady=5)

# Create buttons frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Create buttons
tk.Button(button_frame, text="Insert", command=insert_data).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Update", command=update_data).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Delete", command=delete_data).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Clear", command=clear_entries).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Show All", command=lambda: show_data(True)).pack(side=tk.LEFT, padx=5)

# Create display area
tk.Label(root, text="Click on a record to select it:").pack(pady=5)
display_text = tk.Text(root, height=15, width=40)
display_text.pack(pady=10)

# Bind click event to display_text
display_text.bind('<ButtonRelease-1>', select_record)

# Show initial data
show_data(False)  # Don't show message on startup

root.mainloop()
