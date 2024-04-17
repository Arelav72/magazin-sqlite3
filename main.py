import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


import sqlite3

# создаем базу данных
def init_db():
    conn = sqlite3.connect("businees_orders.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        order_details TEXTNOT NULL,
        status TEXTNOT NULL
    )''')
    conn.commit()
    conn.close()
def add_order():
    conn = sqlite3.connect("businees_orders.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (customer_name, order_details, status) VALUES (?,?,'новый')",

                (customer_name_entry.get(), order_details_entry.get()))
    conn.commit()
    conn.close()
    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)
    view_orders()
    messagebox.showinfo("Успешно", "Заказ успешно добавлен")

def view_orders():
    for i in tree.get_children():
        tree.delete(i)

    conn = sqlite3.connect("businees_orders.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.commit()
    conn.close()

def complete_order():
    selected_item = tree.selection()
    if selected_item:
        order_id = tree.item(selected_item[0])["values"][0]
        conn = sqlite3.connect("businees_orders.db")
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status = 'завершен' WHERE id =?",
                    (order_id,))
        conn.commit()
        conn.close()
        view_orders()
        messagebox.showinfo("Успешно", "Заказ успешно завершен")
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для изменения статуса")




app = tk.Tk()
app.title("Система управления заказами")


# поле для ввода имени пользователя
tk.Label(app, text="Введите имя пользователя").pack()
customer_name_entry = tk.Entry(app)
customer_name_entry.pack()

# поле для ввода заказа
tk.Label(app, text="Детали заказа").pack()
order_details_entry = tk.Entry(app)
order_details_entry .pack()
# команда для добавления заказа
add_button = tk.Button(app, text="Добавить заказ", command=add_order)
add_button.pack()
complete_button = tk.Button(app, text="Завершить заказ", command=complete_order)
complete_button.pack()



columns = ("id", "customer_name", "order_details","status")
tree = ttk.Treeview(app, columns=columns, show="headings")
for column in columns:
    tree.heading(column, text=column)
tree.pack()


init_db() # выполняем команду для создания базы данных
view_orders() # выполняем команду для вывода данных из базы данных
app.mainloop()

