import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class TableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Пример таблицы")
        
        # Подключение к базе данных SQLite
        self.conn = sqlite3.connect('preparat.db')
        self.c = self.conn.cursor()
        
        # Создание таблицы, если она не существует
        self.c.execute('''CREATE TABLE IF NOT EXISTS product
                        (id INTEGER PRIMARY KEY, name TEXT UNIQUE, instruction TEXT, 
                       doz TEXT, price INTEGER)''')
        self.conn.commit()
        
        # Создание таблицы
        self.tree = ttk.Treeview(self.root, columns=("Name", "Instruction","Doz","Price"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Name", text="Имя")
        self.tree.heading("Instruction", text="Инструкция")
        self.tree.heading("Doz", text="Дозировка")
        self.tree.heading("Price", text="Цена")
        self.tree.pack()
        
        # Интерфейс добавления данных
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()
        self.instruction_entry = tk.Entry(root)
        self.instruction_entry.pack()
        self.doz_entry = tk.Entry(root)
        self.doz_entry.pack()
        self.price_entry = tk.Entry(root)
        self.price_entry.pack()
        self.add_button = tk.Button(root, text="Добавить", command=self.add_data)
        self.add_button.pack()

        # Интерфейс удаления данных
        self.delete_button = tk.Button(root, text="Удалить", command=self.delete_data)
        self.delete_button.pack()

        # Интерфейс редактирования данных
        self.edit_button = tk.Button(root, text="Редактировать", command=self.edit_data)
        self.edit_button.pack()
        
        # Загрузка данных из базы данных и отображение их в таблице
        self.load_data()
    
    def load_data(self):
        # Очистка таблицы перед загрузкой новых данных
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Загрузка данных из базы данных и отображение их в таблице
        self.c.execute("SELECT * FROM product")
        rows = self.c.fetchall()
        for row in rows:
            self.tree.insert("", "end", text=row[0], values=(row[1], row[2],row[3],row[4]))
    
    def add_data(self):
        # Получение данных из полей ввода
        name = self.name_entry.get()
        instruction = self.instruction_entry.get()
        doz = self.doz_entry.get()
        price = int(self.price_entry.get()) if self.price_entry.get() else 0
        
        try:
            # Попытка добавить данные в базу данных
            self.c.execute("INSERT INTO product (name, instruction, doz, price) VALUES (?,?,?,?)", (name, instruction, doz, price))
            self.conn.commit()
            # Обновление отображения таблицы
            self.load_data()
        except sqlite3.IntegrityError:
            # Если название не уникально, выводим сообщение об ошибке с помощью messagebox
            messagebox.showerror("Ошибка", "Препарат уже существует, пожалуйста, выберите другое название")
    
    def delete_data(self):
        # Получение ID выделенной строки
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите строку для удаления")
            return
        
        # Получение ID выделенной строки и удаление данных из базы данных
        item_id = self.tree.item(selected_item)['text']
        self.c.execute("DELETE FROM product WHERE id=?", (item_id,))
        self.conn.commit()
        
        # Обновление отображения таблицы
        self.load_data()
    
    def edit_data(self):
        # Получение ID выделенной строки
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите строку для редактирования")
            return
        
        # Получение данных выделенной строки
        item_id = self.tree.item(selected_item)['text']
        name = self.name_entry.get()
        instruction = self.instruction_entry.get()
        doz = self.doz_entry.get()
        price = int(self.price_entry.get()) if self.price_entry.get() else 0
        
        # Обновление данных в базе данных
        self.c.execute("UPDATE product SET name=?, instruction=?, doz=?, price=? WHERE id=?", (name, instruction, doz, price, item_id))
        self.conn.commit()
        
        # Обновление отображения таблицы
        self.load_data()

def main():
    root = tk.Tk()
    app = TableApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()