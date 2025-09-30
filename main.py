import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import date, timedelta
from db_config import get_db_connection
from auth import login_user, register_user

def get_cursor():
    conn = get_db_connection()
    return conn, conn.cursor()

def add_book():
    name = simpledialog.askstring("Book Name", "Enter book name:")
    if not name:
        return
    author = simpledialog.askstring("Author", "Enter author name:")
    if not author:
        return
    qty = simpledialog.askinteger("Total", "Enter total quantity:")
    if not qty:
        return
    conn, cur = get_cursor()
    cur.execute("INSERT INTO books (name, author, total, available) VALUES (%s,%s,%s,%s)",
                (name, author, qty, qty))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book added successfully")

def add_student():
    sname = simpledialog.askstring("Student Name", "Enter student name:")
    if not sname:
        return
    email = simpledialog.askstring("Email", "Enter email (optional):")
    phone = simpledialog.askstring("Phone", "Enter phone number:")
    conn, cur = get_cursor()
    cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (sname, email, phone))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student added successfully")

def issue_book():
    student = simpledialog.askinteger("Student ID", "Enter student ID:")
    if not student:
        return
    book = simpledialog.askinteger("Book ID", "Enter book ID:")
    if not book:
        return
    conn, cur = get_cursor()
    cur.execute("SELECT available FROM books WHERE book_id=%s", (book,))
    row = cur.fetchone()
    if not row or row[0] < 1:
        messagebox.showwarning("Unavailable", "Book not available")
        conn.close()
        return
    today = date.today()
    due = today + timedelta(days=14)
    cur.execute("INSERT INTO issue_history (student_id, book_id, issue_date, return_date) VALUES (%s,%s,%s,%s)",
                (student, book, today, due))
    cur.execute("UPDATE books SET available = available-1 WHERE book_id=%s", (book,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"Book issued. Return by: {due}")

def return_book():
    issue_id = simpledialog.askinteger("Issue ID", "Enter Issue ID:")
    if not issue_id:
        return
    today = date.today()
    conn, cur = get_cursor()
    cur.execute("SELECT book_id, return_date FROM issue_history WHERE issue_id=%s AND status='issued'", (issue_id,))
    row = cur.fetchone()
    if not row:
        messagebox.showwarning("Error", "Invalid issue ID or book already returned")
        conn.close()
        return
    book_id, due = row
    fine = 0
    if today > due:
        fine = (today - due).days * 5
    cur.execute("UPDATE issue_history SET fine=%s, actual_return_date=%s, status='returned' WHERE issue_id=%s", 
                (fine, today, issue_id))
    cur.execute("UPDATE books SET available = available + 1 WHERE book_id=%s", (book_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"Book returned. Fine: Rs.{fine}")

def show_books():
    conn, cur = get_cursor()
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    conn.close()
    display = "ID | Name | Author | Total | Available\n" + "-"*50 + "\n"
    for row in rows:
        display += f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}\n"
    messagebox.showinfo("All Books", display)

def show_students():
    conn, cur = get_cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    display = "ID | Name | Email | Phone\n" + "-"*40 + "\n"
    for row in rows:
        display += f"{row[0]} | {row[1]} | {row[2]} | {row[3]}\n"
    messagebox.showinfo("All Students", display)

def show_history():
    conn, cur = get_cursor()
    cur.execute("""SELECT ih.issue_id, s.name, b.name, ih.issue_date, ih.return_date, ih.fine, ih.status 
                   FROM issue_history ih
                   JOIN students s ON ih.student_id = s.student_id
                   JOIN books b ON ih.book_id = b.book_id
                   ORDER BY ih.issue_id DESC LIMIT 10""")
    rows = cur.fetchall()
    conn.close()
    display = "IssueID | Student | Book | Issue | Return | Fine | Status\n" + "-"*65 + "\n"
    for r in rows:
        display += f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]}\n"
    messagebox.showinfo("Recent History", display)

def login_screen():
    login_win = tk.Tk()
    login_win.title('Library Login')
    login_win.geometry('300x200')
    
    tk.Label(login_win, text='Username', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10)
    tk.Label(login_win, text='Password', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10)
    
    uname = tk.Entry(login_win, font=('Arial', 12))
    upass = tk.Entry(login_win, show='*', font=('Arial', 12))
    uname.grid(row=0, column=1, padx=10, pady=10)
    upass.grid(row=1, column=1, padx=10, pady=10)
    
    def attempt_login():
        user = uname.get()
        pwd = upass.get()
        role = login_user(user, pwd)
        if role:
            login_win.destroy()
            launch_main(role)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def register_screen():
        reg_win = tk.Toplevel(login_win)
        reg_win.title('Register New User')
        reg_win.geometry('300x150')
        
        tk.Label(reg_win, text='Username').grid(row=0, column=0, padx=10, pady=5)
        tk.Label(reg_win, text='Password').grid(row=1, column=0, padx=10, pady=5)
        
        reg_uname = tk.Entry(reg_win)
        reg_upass = tk.Entry(reg_win, show='*')
        reg_uname.grid(row=0, column=1, padx=10, pady=5)
        reg_upass.grid(row=1, column=1, padx=10, pady=5)
        
        def do_register():
            user = reg_uname.get()
            pwd = reg_upass.get()
            if user and pwd:
                try:
                    register_user(user, pwd)
                    messagebox.showinfo("Success", "User registered successfully")
                    reg_win.destroy()
                except:
                    messagebox.showerror("Error", "Username already exists")
            else:
                messagebox.showerror("Error", "Please fill all fields")
        
        tk.Button(reg_win, text='Register', command=do_register).grid(row=2, column=1, pady=10)
    
    tk.Button(login_win, text='Login', command=attempt_login, font=('Arial', 12)).grid(row=2, column=1, pady=10)
    tk.Button(login_win, text='Register', command=register_screen, font=('Arial', 12)).grid(row=2, column=0, pady=10)
    
    login_win.mainloop()

def launch_main(role):
    app = tk.Tk()
    app.title(f"Library Management - {role.upper()}")
    app.geometry('400x500')
    
    tk.Label(app, text=f"Welcome {role.upper()}", font=('Arial', 16, 'bold')).pack(pady=10)
    
    if role == 'admin':
        tk.Button(app, text="Add New Book", command=add_book, width=25, height=2).pack(pady=5)
        tk.Button(app, text="Add New Student", command=add_student, width=25, height=2).pack(pady=5)
    
    tk.Button(app, text="Issue Book", command=issue_book, width=25, height=2).pack(pady=5)
    tk.Button(app, text="Return Book", command=return_book, width=25, height=2).pack(pady=5)
    tk.Button(app, text="View All Books", command=show_books, width=25, height=2).pack(pady=5)
    tk.Button(app, text="View All Students", command=show_students, width=25, height=2).pack(pady=5)
    tk.Button(app, text="View Issue History", command=show_history, width=25, height=2).pack(pady=5)
    
    tk.Button(app, text="Exit", command=app.quit, width=25, height=2, bg='red', fg='white').pack(pady=20)
    
    app.mainloop()

if __name__ == "__main__":
    login_screen()
