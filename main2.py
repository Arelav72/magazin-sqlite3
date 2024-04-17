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
        order_details TEXT NOT NULL)''')
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
    for i in orders_tree.get_children():
        orders_tree.delete(i)
    conn = sqlite3.connect("businees_orders.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    for row in rows:
        orders_tree.insert("", tk.END, values=row)
    conn.commit()
    conn.close()


def complete_order():
    selected_item = orders_tree.selection()
    if selected_item:
        order_id = orders_tree.item(selected_item[0])["values"][0]
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

def delete_order():
    selected_item = orders_tree.selection()[0]  # Получаем выбранный элемент
    order_id = orders_tree.item(selected_item, 'values')[0]  # Получаем ID заказа из первой колонки
    confirm = messagebox.askyesno("Подтверждение", "Вы действительно хотите удалить выбранный заказ?")

    if confirm:
        try:
            with sqlite3.connect("businees_orders.db") as conn:  # Убедитесь, что имя базы данных верное
                cur = conn.cursor()
                cur.execute("DELETE FROM orders WHERE id=?", (order_id,))

                # Удаляем из интерфейса пользователя
                orders_tree.delete(selected_item)

                messagebox.showinfo("Успех", "Заказ успешно удален")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при удалении: {e}")
window = tk.Tk()
window.title("Управление Заказами")

# Фрейм для ввода данных
input_frame = tk.Frame(window, padx=10, pady=10)
input_frame.pack(padx=10, pady=5, fill="x", expand=True)

# Элементы ввода
tk.Label(input_frame, text="Имя клиента:").pack(side="left")
customer_name_entry = tk.Entry(input_frame)
customer_name_entry.pack(side="left", expand=True, padx=5)

tk.Label(input_frame, text="Детали заказа:").pack(side="left")
order_details_entry = tk.Entry(input_frame)
order_details_entry.pack(side="left", expand=True, padx=5)

# Фрейм для кнопок
button_frame = tk.Frame(window, padx=10, pady=10)
button_frame.pack(padx=10, pady=5, fill="x")

# Кнопки
add_button = tk.Button(button_frame, text="Добавить заказ", command=add_order)
add_button.pack(side="left", padx=5)

update_button = tk.Button(button_frame, text="Обновить выбранный", command=complete_order)
update_button.pack(side="left", padx=5)

delete_button = tk.Button(button_frame, text="Удалить выбранный", command=delete_order)
delete_button.pack(side="left", padx=5)

# Фрейм для списка заказов
orders_frame = tk.Frame(window, padx=10, pady=10)
orders_frame.pack(padx=10, pady=5, fill="both", expand=True)

# Список заказов
orders_tree = ttk.Treeview(orders_frame, columns=("ID", "Customer", "Order", "Status"), show="headings")
orders_tree.heading("ID", text="ID")
orders_tree.heading("Customer", text="Имя клиента")
orders_tree.heading("Order", text="Детали заказа")
orders_tree.heading("Status", text="Статус  заказа")
orders_tree.pack(fill="both", expand=True)


init_db()
view_orders()
window.mainloop()