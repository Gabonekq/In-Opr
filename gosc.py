from tkinter import messagebox
import tkinter as tk
from tkinter.ttk import Treeview

import db as db
import login_window
import my_config


CUSTOMER_WINDOW_SIZE = "650x600"

PRODUCT_COLUMNS = ('Id', 'Nazwa', 'Cena', 'Dostępne')
PRODUCT_COLUMNS_SIZE = (25, 150, 50, 70)

MY_ORDERS_COLUMNS = ('Id', 'Nazwa', 'Ilość', 'Cena')
MY_ORDERS_COLUMNS_SIZE = (25, 150, 60, 90)


class CustomerApp:
   

    def __init__(self, master):
        
        self.master = master
        self.master.geometry(CUSTOMER_WINDOW_SIZE)
        self.master.configure(bg=my_config.BACKGROUND)
        self.master.title(my_config.APP_NAME)

        
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.function_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.function_frame2 = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.function_frame3 = tk.Frame(self.master, bg=my_config.BACKGROUND)

        
        self.error_label = tk.Label()

        self.product_tree = None
        self.my_orders_tree = None
        self.location_entry = None
        self.quantity_entry = None
        self.id_product_entry = None

    def initialize_main_buttons(self):
        
        if self.frame:
            self.frame.destroy()
        if self.function_frame:
            self.function_frame.destroy()
        if self.function_frame2:
            self.function_frame2.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()

        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        search_button = tk.Button(self.frame, text='Lista rezerwacji',
                                  bg=my_config.FOREGROUND, command=self.list_products, width=16)
        search_button.grid(row=0, column=0, pady=(10, 3))
        edit_button = tk.Button(self.frame, text='Edytuj konto', bg=my_config.FOREGROUND,
                                command=self.account_edit, width=16)
        edit_button.grid(row=1, column=0, pady=(0, 3))
        orders_button = tk.Button(self.frame, text='Moje rezerwacje', bg=my_config.FOREGROUND,
                                  command=self.my_orders, width=16)
        orders_button.grid(row=2, column=0, pady=(0, 3))
        logoff_button = tk.Button(self.frame, text='Wyloguj', bg=my_config.FOREGROUND,
                                  command=self.log_off, width=16)
        logoff_button.grid(row=3, column=0, pady=(0, 3))
        self.frame.pack()

    def list_products(self):
        
        self.initialize_main_buttons()

       
        self.function_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.function_frame.pack()
        self.function_frame2 = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.function_frame2.pack()

        list_label = tk.Label(self.function_frame, text='Lista rezerwacji',
                              width=100, bg=my_config.BACKGROUND)
        list_label.grid(row=0, column=0, pady=(10, 0))

        
        self.product_tree = Treeview(self.function_frame, columns=PRODUCT_COLUMNS,
                                     show='headings', height=10)
        self.product_tree.grid(row=1, column=0, padx=8)

        for column_name, width in zip(PRODUCT_COLUMNS, PRODUCT_COLUMNS_SIZE):
            self.product_tree.column(column_name, width=width, anchor=tk.CENTER)
            self.product_tree.heading(column_name, text=column_name)

        scrollbar = tk.Scrollbar(self.function_frame, orient=tk.VERTICAL)
        scrollbar.configure(command=self.product_tree.set)
        self.product_tree.configure(yscrollcommand=scrollbar)
        self.product_tree.bind('<ButtonRelease-1>', self.product_selection)

        
        records = db.return_products()
        for record in records:
            self.product_tree.insert('', tk.END, values=[record[0], record[1], record[2], record[3]])

        #label
        id_product_label = tk.Label(self.function_frame2, text='Produkt ID:', bg=my_config.BACKGROUND)
        id_product_label.grid(row=0, column=0, sticky=tk.E)
        quantity_label = tk.Label(self.function_frame2, text='Ilość:', bg=my_config.BACKGROUND)
        quantity_label.grid(row=1, column=0, sticky=tk.E)
        location_label = tk.Label(self.function_frame2, text='Liczba gości:', bg=my_config.BACKGROUND)
        location_label.grid(row=2, column=0, sticky=tk.E)

        
        self.id_product_entry = tk.Entry(self.function_frame2, width=30, bg=my_config.FOREGROUND)
        self.id_product_entry.grid(row=0, column=1)
        self.quantity_entry = tk.Entry(self.function_frame2, width=30, bg=my_config.FOREGROUND)
        self.quantity_entry.grid(row=1, column=1)
        self.location_entry = tk.Entry(self.function_frame2, width=30, bg=my_config.FOREGROUND)
        self.location_entry.grid(row=2, column=1)

        #przyciski
        place_order_button = tk.Button(self.function_frame2, text='Zarezerwuj',
                                       bg=my_config.FOREGROUND, command=self.place_order, width=16)
        place_order_button.grid(row=4, column=0)
        details_button = tk.Button(self.function_frame2, text='Szczegóły',
                                   bg=my_config.FOREGROUND, command=self.product_details, width=16)
        details_button.grid(row=4, column=1, )

    def place_order(self):
        
        if self.error_label:
            self.error_label.destroy()

        
        if not self.id_product_entry.get():
            self.error_message("Błąd ID")
        elif not my_config.is_integer(self.quantity_entry.get()) or int(self.quantity_entry.get()) < 1:
            self.error_message("Dodaj ilość")
        elif not self.location_entry.get():
            self.error_message("Dodaj liczbę")

        
        elif not db.is_customer_id_exist(my_config.MY_ID) or not db.is_product_id_exists(
                self.id_product_entry.get()):
            self.error_message("ID nie istnieje")

        
        elif db.add_order(my_config.MY_ID, self.id_product_entry.get(), self.quantity_entry.get(),
                          self.location_entry.get()):
            messagebox.showinfo("Agrorelask", 'Zarezerwowano')
            self.list_products()
        else:
            self.error_message("Brak wystarczającej ilośći")

    def product_details(self):
        
        if self.error_label:
            self.error_label.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()

        if not self.id_product_entry.get():
            self.error_message("Wybierz")

        elif db.is_product_id_exists(self.id_product_entry.get()):

            self.function_frame3 = tk.Frame(self.master, bg=my_config.BACKGROUND)
            self.function_frame3.pack(side=tk.TOP)

           
            description = db.return_product(self.id_product_entry.get())[4]
            self.error_label = tk.Message(self.function_frame3, text="Opis: {}".format(description),
                                          bg=my_config.BACKGROUND, width=300)
            self.error_label.grid(row=5, column=0)
        else:
            self.error_message("Nie istnieje")

    def product_selection(self, event):
        
        try:
            if self.product_tree.selection():
                record = self.product_tree.set(self.product_tree.selection())
                self.id_product_entry.delete(0, tk.END)
                self.id_product_entry.insert(tk.END, record[PRODUCT_COLUMNS[0]])

        except KeyError:
            pass

    def order_selection(self, event):
        
        if self.my_orders_tree.selection():
            record = self.my_orders_tree.set(self.my_orders_tree.selection())
            record = db.return_order(record[PRODUCT_COLUMNS[0]])

            if self.function_frame2:
                self.function_frame2.destroy()

            self.function_frame2 = tk.Frame(self.master, bg=my_config.BACKGROUND)
            self.function_frame2.pack(side=tk.TOP)

            
            order_info = ("Ilość: \t{}\nCena: \t{}\n"
                          "Data: \t{}\nLiczba osób: \t{}\n"
                          ).format(record[3], record[4], record[5], record[6], record[7], record[8])

            self.error_label = tk.Message(self.function_frame2, text=order_info,
                                          bg=my_config.BACKGROUND, width=300)
            self.error_label.grid(row=0, column=0)

    def account_edit(self):
        
        if self.frame:
            self.frame.destroy()
        if self.function_frame:
            self.function_frame.destroy()
        if self.function_frame2:
            self.function_frame2.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()
        AccountEdit(self.master)

    def my_orders(self):
        
        self.initialize_main_buttons()

        self.function_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.function_frame.pack()

        
        list_label = tk.Label(self.function_frame, text='Moje rezerwacje:', width=100, bg=my_config.BACKGROUND)
        list_label.grid(row=0, column=0, pady=(10, 0))

        
        self.my_orders_tree = Treeview(self.function_frame, columns=MY_ORDERS_COLUMNS,
                                       show='headings', height=10)
        self.my_orders_tree.grid(row=1, column=0)

        for column_name, width in zip(MY_ORDERS_COLUMNS, MY_ORDERS_COLUMNS_SIZE):
            self.my_orders_tree.column(column_name, width=width, anchor=tk.CENTER)
            self.my_orders_tree.heading(column_name, text=column_name)

        scrollbar = tk.Scrollbar(self.function_frame, orient=tk.VERTICAL)
        scrollbar.configure(command=self.my_orders_tree.set)
        self.my_orders_tree.configure(yscrollcommand=scrollbar)
        self.my_orders_tree.bind('<ButtonRelease-1>', self.order_selection)

        
        records = db.orders_product_info(my_config.MY_ID)
        for record in records:
            self.my_orders_tree.insert('', tk.END, values=[record[0], record[1], record[2], record[3]])

    def error_message(self, name):
       
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.function_frame2, text=name, bg=my_config.BACKGROUND,
                                    fg=my_config.ERROR_FOREGROUND)
        self.error_label.grid(row=3, column=1)

    def log_off(self):
        
        if self.frame:
            self.frame.destroy()
        if self.function_frame:
            self.function_frame.destroy()
        if self.function_frame2:
            self.function_frame2.destroy()
        if self.function_frame3:
            self.function_frame3.destroy()
        application = login_window.LoginWindow(self.master)
        application.initialize_login_window()


class AccountEdit:
    

    def __init__(self, master):
        
        self.master = master
        self.master.configure(bg=my_config.BACKGROUND)
        self.master.title(my_config.APP_NAME)
        self.master.geometry(CUSTOMER_WINDOW_SIZE)

        
        self.error_label = tk.Label()

        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.frame.pack()

        
        new_password_label = tk.Label(self.frame, text='Nowe hasło:', bg=my_config.BACKGROUND)
        new_password_label.grid(row=1, column=0, pady=(10, 0), sticky=tk.E)
        password_label = tk.Label(self.frame, text='Hasło:', bg=my_config.BACKGROUND)
        password_label.grid(row=2, column=0, sticky=tk.E)
        name_label = tk.Label(self.frame, text='Imię:', bg=my_config.BACKGROUND)
        name_label.grid(row=3, column=0, pady=(4, 0), sticky=tk.E)
        phone_label = tk.Label(self.frame, text='Numer:', bg=my_config.BACKGROUND)
        phone_label.grid(row=4, column=0, pady=(4, 0), sticky=tk.E)
        email_label = tk.Label(self.frame, text='Email:', bg=my_config.BACKGROUND)
        email_label.grid(row=5, column=0, pady=(4, 0), sticky=tk.E)

        
        self.new_password_entry = tk.Entry(self.frame, width=22, show='*', bg=my_config.FOREGROUND)
        self.new_password_entry.grid(row=1, column=1, pady=(10, 0))
        self.password_entry = tk.Entry(self.frame, width=22, show='*', bg=my_config.FOREGROUND)
        self.password_entry.grid(row=2, column=1)
        self.name_entry = tk.Entry(self.frame, width=22, bg=my_config.FOREGROUND)
        self.name_entry.grid(row=3, column=1)
        self.phone_entry = tk.Entry(self.frame, width=22, bg=my_config.FOREGROUND)
        self.phone_entry.grid(row=4, column=1)
        self.email_entry = tk.Entry(self.frame, width=22, bg=my_config.FOREGROUND)
        self.email_entry.grid(row=5, column=1)

       
        self.change_button = tk.Button(self.frame, text='Zmień', bg=my_config.FOREGROUND,
                                       command=self.set_change, width=16)
        self.change_button.grid(row=1, column=2, padx=(10, 0), pady=(10, 0))
        self.cancel_button = tk.Button(self.frame, text='Wróć', bg=my_config.FOREGROUND,
                                       command=self.exit, width=16)
        self.cancel_button.grid(row=2, column=2, padx=(10, 0))

        
        customer_info = db.return_customer(my_config.MY_ID)
        if customer_info:
            self.name_entry.insert(tk.END, customer_info[3])
            self.phone_entry.insert(tk.END, customer_info[4])
            self.email_entry.insert(tk.END, customer_info[5])
        else:
            messagebox.showinfo("Agrorelaks", 'ERROR: ZŁE ID!!!')
            self.exit()

    def set_change(self):
        
        if self.error_label:
            self.error_label.destroy()

        
        if 0 < len(self.new_password_entry.get()) < 6:
            self.error_message('Hasło musi mieć min. 6 znaków')

       
        elif self.password_entry.get() != db.return_customer(my_config.MY_ID)[2]:
            self.error_message('Błędne hasło')
        elif not self.name_entry.get():
            self.error_message('Imię nie może być puste')
        elif self.phone_entry.get() and not my_config.is_integer(self.phone_entry.get()):
            self.error_message("Zły numer telefonu")
        elif not self.email_entry.get():
            self.error_message('Email nie może być pusty')

        else:
           

            if self.new_password_entry:
                #nowe haslo
                db.edit_customer(my_config.MY_ID, self.new_password_entry.get(), self.name_entry.get(),
                                 self.email_entry.get(),
                                 self.phone_entry.get())
            else:
                
                db.edit_customer(my_config.MY_ID,
                                 db.return_customer(my_config.MY_ID)[2], self.name_entry.get(),
                                 self.email_entry.get(), self.phone_entry.get())

            self.error_message("Konto zaktualizowane")

    def error_message(self, name):
       
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.frame, fg=my_config.ERROR_FOREGROUND,
                                    text=name, bg=my_config.BACKGROUND)
        self.error_label.grid(row=6, column=1)

    def exit(self):
        
        self.frame.destroy()
        application = CustomerApp(self.master)
        application.initialize_main_buttons()
