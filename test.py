import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="add.gif")
        btn_open_dialog = tk.Button(toolbar, text='Добавить позицию', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='delete.gif')
        btn_delete = tk.Button(toolbar, text='Удалить позицию', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='search.gif')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='refresh.gif')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.combobox = ttk.Combobox(self, values=[u"agility_heroes", u"intelligence_heroes", u"power_heroes"])
        self.combobox.current(0)
        btn_combobox = ttk.Combobox(self, values=[u"agility_heroes", u"intelligence_heroes", u"power_heroes"])
        btn_combobox.pack(side=tk.LEFT)


        self.tree = ttk.Treeview(self, columns=('ID', 'name1', 'herous'),
                                 height=15, show='headings')
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column("name1", width=300, anchor=tk.CENTER)
        self.tree.column("herous", width=365, anchor=tk.CENTER)

        self.tree.heading("ID", text='ID')
        self.tree.heading("name1", text='Герой')
        self.tree.heading("herous", text='История')

        self.tree.pack()

    def records(self, name1, herous):
        self.db.insert_data(name1, herous)
        self.view_records()

    def update_record(self, name1, herous):
        self.db.c.execute('''UPDATE heroes SET name1=?, herous=? WHERE ID=?''',
                          (name1, herous, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM heroes''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM heroes WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, name1):
        name1 = ('%' + name1 + '%',)
        self.db.c.execute('''SELECT * FROM heroes WHERE name1 LIKE ?''', name1)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить ')
        self.geometry('400x220+400+300')
        self.resizable(False, False)


        label_herous = tk.Label(self, text='История героя:')
        label_herous.place(x=50, y=50)
        label_ame1 = tk.Label(self, text='Имя героя:')
        label_ame1.place(x=50, y=80)

        self.entry_herous = ttk.Entry(self)
        self.entry_herous.place(x=200, y=50)

        self.entry_name1 = ttk.Entry(self)
        self.entry_name1.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name1.get(),
                                                                       self.entry_herous.get())
                                                                       )

        self.grab_set()
        self.focus_set()

class Update(Child):
        def __init__(self):
            super().__init__()
            self.init_edit()
            self.view = app
            self.db = db
            self.default_data()

        def init_edit(self):
            self.title('Редактировать позицию')
            btn_edit = ttk.Button(self, text='Редактировать')
            btn_edit.place(x=205, y=170)
            btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name1.get(),
                                                                              self.entry_herous.get(),
                                                                              ))

            self.btn_ok.destroy()

        def default_data(self):
            self.db.c.execute('''SELECT * FROM heroes WHERE id=?''',
                              (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
            row = self.db.c.fetchone()
            self.entry_name1.insert(0, row[1])
            self.entry_herous.insert(0, row[2])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('heroes.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS heroes (id integer primary key, name1 text, herous text)''')
        self.conn.commit()

    def insert_data(self, name1, herous):
        self.c.execute('''INSERT INTO heroes(name1, herous) VALUES (?, ?)''',
                       (name1, herous))
        self.conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("GUI")
    root.geometry("850x450+300+200")
    root.resizable(False, False)
    root.mainloop()
