import tkinter as tk
import sqlite3 as sql
import pandas as pd
from tkinter import messagebox, ttk
from datetime import datetime

conn = sql.connect("Expenses.db")

cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    MONTH TEXT NOT NULL,
    EXPENSE REAL NOT NULL,
    CATEGORY TEXT NOT NULL,
    REMARKS TEXT,
    DATE TEXT NOT NULL)''')


def add_expense():
    try:
        expense_value = float(expense.get())
        
        if expense_value <= 0:
            messagebox.showinfo( title = "Alert", message = "Expense must be greater than 0!")
            return
        
    except ValueError:
        messagebox.showinfo(title = "Alert", message = "Expense must be in digits!")
        return
    
    month_value = month.get()
    category_value = category.get()
    remarks_value = remarks.get()
    date = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute(
        "INSERT INTO expenses (MONTH, EXPENSE, CATEGORY, REMARKS, DATE) VALUES (?, ?, ?, ?, ?)", 
        (month_value, expense_value, category_value, remarks_value, date)
    )
    
    conn.commit()
    
    show_expenses()
    
    messagebox.showinfo(title = "Success", message = "Record inserted successfully")
    
    expense.delete(first = 0, last = 'end')
    remarks.delete(first = 0, last = 'end')
    month.current(0)
    category.current(0)
    
def clear_data():
    
    expense.delete(first = 0, last = 'end')
    remarks.delete(first = 0, last = 'end')
    month.current(0)
    category.current(0)
    
    messagebox.showinfo(title = "Success", message = "Record Cleared Successfully!")

def show_expenses():
    
    for row in tree.get_children():
        tree.delete(row)
        
    cursor.execute(
            "SELECT * FROM expenses ORDER BY DATE DESC"
        )
        
    rows = cursor.fetchall()
        
    total_expense = 0
        
    for row in rows:
        tree.insert("", "end", values = row)
        total_expense += row[2]
            
    total_lbl.config(text = f"Total Expenses (in RS.) : {total_expense}")


def delete_expense():
    selected_row = tree.selection()
    
    if not selected_row:
        messagebox.showinfo("Error", "Please select a record to delete!")
        return
    
    item = tree.item(selected_row[0])
    
    record_id = item['values'][0]
    
    cursor.execute(
        "DELETE FROM expenses WHERE ID = ?", (record_id,)
    )
    
    conn.commit()
    
    messagebox.showinfo("Success", "Record deleted successfully")
    
    show_expenses()
    
def export_to_csv():
    df = pd.read_sql_query("SELECT * FROM expenses ORDER BY DATE", conn)
    df.to_csv("../expense tracker/expenses.csv", index = False)
    
    messagebox.showinfo("Success", "Data Exported successfully!")


root = tk.Tk()
root.title("Expense Tracker")
root.geometry("500x350")

frame1 = tk.Frame(root)
frame1.pack(pady = 20)

lbl1 = tk.Label(frame1, text = "Select Month", font = ("Ariel", 16))
lbl1.grid(row = 0, column = 0, pady = 10)

all_months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
month = ttk.Combobox(frame1, values = all_months, state = 'readonly', font = ("Arial", 16), width = 20)
month.grid(row = 0, column = 1, pady = 10)
month.current(0)

lbl2 = tk.Label(frame1, text = "Enter Expense (in RS.)", font = ("Arial, 16"))
lbl2.grid(row = 1, column = 0, pady = 10)

expense = tk.Entry(frame1, width = 20, font = ("Arial", 16))
expense.grid(row = 1, column = 1, pady = 10)

lbl3 = tk.Label(frame1, text = "Select Category", font = ("Arial", 16))
lbl3.grid(row = 2, column = 0, pady = 10)

all_categories = ["Food", "Bills", "Travel", "Social", "Other"]
category = ttk.Combobox(frame1, value = all_categories, state = 'readonly', font = ("Arial", 16), width = 20)
category.grid(row = 2, column = 1, pady = 10)
category.current(0)

lbl4 = tk.Label(frame1, text = "Enter Remarks", font = ("Arail, 16"))
lbl4.grid(row = 3, column = 0, pady = 10)

remarks = tk.Entry(frame1, width = 20, font = ("Arial, 16"))
remarks.grid(row = 3, column = 1, pady = 10)

add_btn = tk.Button(frame1, text = "Save", width = 15, bg = "green", fg = "white", font = ("Arial", 16), command = add_expense)
add_btn.grid(row = 4, column = 0, pady = 10)

clear_btn = tk.Button(frame1, text = "Clear", width= 15, bg = "yellow", fg = "white", font = ("Arial", 16), command = clear_data)
clear_btn.grid(row = 4, column = 1, pady = 10)

delete_btn = tk.Button(frame1, text = "Delete", width = 15, bg = "red", fg = "white", font = ("Arial", 16), command = delete_expense)
delete_btn.grid(row = 5, column = 0, pady = 10)

export_btn = tk.Button(frame1, text = "Export", width = 15, bg = "blue", fg = "white", font = ("Arial", 16), command = export_to_csv)
export_btn.grid(row = 5, column = 1, pady = 10)

total_lbl = tk.Label(frame1, text = "Total Expenses (in Rs.) : 0", font = ("Arial", 16))
total_lbl.grid(row = 6, column = 0, columnspan = 2, pady = 10)

frame2 = tk.Frame(root)
frame2.pack(pady = 20)

tree = ttk.Treeview(frame2, columns = ("ID","Month", "Expense", "Category", "Remarks", "Date"), show = "headings")

tree.heading("ID", text = "ID", anchor = "center")
tree.heading("Month", text = "Month", anchor = "center")
tree.heading("Expense", text = "Expense", anchor = "center")
tree.heading("Category", text = "Category", anchor = "center")
tree.heading("Remarks", text = "Remarks", anchor = "center")
tree.heading("Date", text = "Date", anchor = "center")

tree.column("ID", width = 50)
tree.column("Month", width = 100)
tree.column("Expense", width = 100)
tree.column("Category", width = 100)
tree.column("Remarks", width = 200)
tree.column("Date", width = 120)

tree.pack()

show_expenses()

root.mainloop()

conn.close()