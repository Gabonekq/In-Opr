from tkinter import messagebox
import tkinter as tk
from tkinter.ttk import Treeview

import db as db
import login_window
import my_config


ADMIN_WINDOW_SIZE = "1000x640"

CUSTOMER_COLUMNS = ('Id', 'Imię', 'Email')
CUSTOMER_COLUMNS_SIZE = (25, 150, 200)

CUSTOMER_COLUMN_FULL = ('Id', 'Login', 'Imię', 'Numer', 'Email', 'perm')
CUSTOMER_COLUMN_FULL_SIZE = (25, 120, 150, 90, 200, 35)

PRODUCT_COLUMNS = ('Id', 'Produkt', 'Cena', 'Dostępne', 'Opis')
PRODUCT_COLUMNS_SIZE = (25, 120, 50, 50, 130)

ORDER_COLUMNS = ('Id', 'ilość', 'Płatność', 'Zatwierdź', 'Liczba osób', 'Data')
ORDER_COLUMNS_SIZE = (25, 60, 60, 40, 200, 120)


class CustomersMenu:
    

    def __init__(self, master):
        
        self.master = master
        self.master.geometry(ADMIN_WINDOW_SIZE)
        self.master.configure(bg=my_config.BACKGROUND)
        self.master.title(my_config.APP_NAME)

        
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.frame.pack()
       
        self.entry_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.entry_frame.pack()
        
        self.listbox_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.listbox_frame.pack()

        self.error_label = tk.Label()

        self.customers_tree = None
        self.login_entry = None
        self.email_entry = None
        self.phone_entry = None
        self.name_entry = None
        self.perm_entry = None

    def initialize_menu(self):
        
        self.frame.destroy()
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.frame.pack()

        self.entry_frame.destroy()
        self.entry_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.entry_frame.pack()

        self.listbox_frame.destroy()
        self.listbox_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.listbox_frame.pack()

        if self.error_label:
            self.error_label.destroy()

        
        customer_button = tk.Button(self.frame, text='Gość', command=self.initialize_menu,
                                    width=30, bg=my_config.FOREGROUND)
        customer_button.grid(row=0, column=0, pady=10)
        order_button = tk.Button(self.frame, text='Rezerwacja', command=self.go_to_order_window,
                                 width=30, bg=my_config.FOREGROUND)
        order_button.grid(row=0, column=1, )
        product_button = tk.Button(self.frame, text='Produkt', command=self.go_to_product_window,
                                   width=30, bg=my_config.FOREGROUND)
        product_button.grid(row=0, column=2)

        #label
        login_label = tk.Label(self.entry_frame, text='Login:', bg=my_config.BACKGROUND)
        login_label.grid(row=1, column=0, sticky=tk.E)
        name_label = tk.Label(self.entry_frame, text='Imię gościa:', bg=my_config.BACKGROUND)
        name_label.grid(row=2, column=0, sticky=tk.E)
        phone_label = tk.Label(self.entry_frame, text='Numer gościa:', bg=my_config.BACKGROUND)
        phone_label.grid(row=3, column=0, sticky=tk.E)
        email_label = tk.Label(self.entry_frame, text='Email gościa:', bg=my_config.BACKGROUND)
        email_label.grid(row=4, column=0, sticky=tk.E)
        perm_label = tk.Label(self.entry_frame, text='Perm:', bg=my_config.BACKGROUND)
        perm_label.grid(row=5, column=0, sticky=tk.E)

        
        self.login_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.login_entry.grid(row=1, column=1)
        self.name_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.name_entry.grid(row=2, column=1)
        self.phone_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.phone_entry.grid(row=3, column=1)
        self.email_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.email_entry.grid(row=4, column=1)
        self.perm_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.perm_entry.grid(row=5, column=1)

        # przyciski
        search_button = tk.Button(self.entry_frame, text='Szukaj', command=self.search_customer,
                                  width=20, bg=my_config.FOREGROUND)
        search_button.grid(row=1, column=2, padx=20)
        update_button = tk.Button(self.entry_frame, text='Aktualizuj', command=self.update_customer,
                                  width=20, bg=my_config.FOREGROUND)
        update_button.grid(row=2, column=2)
        clear_button = tk.Button(self.entry_frame, text='Wyczyść', command=self.clear_customer_entries,
                                 width=20, bg=my_config.FOREGROUND)
        clear_button.grid(row=3, column=2)
        delete_button = tk.Button(self.entry_frame, text='Usuń', command=self.delete_customer,
                                  width=20, bg=my_config.FOREGROUND)
        delete_button.grid(row=4, column=2)

        exit_button = tk.Button(self.entry_frame, text='Wyloguj', command=self.exit_admin_window,
                                width=20, bg=my_config.FOREGROUND)
        exit_button.grid(row=5, column=2)

        
        self.listbox_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.listbox_frame.pack()

        list_label = tk.Label(self.listbox_frame, text='Lista gości',
                              width=100, bg=my_config.BACKGROUND)
        list_label.grid(row=0, column=0)

        
        self.customers_tree = Treeview(self.listbox_frame, columns=CUSTOMER_COLUMN_FULL,
                                       show='headings', height=10)
        self.customers_tree.grid(row=1, column=0)

        for column_name, width in zip(CUSTOMER_COLUMN_FULL, CUSTOMER_COLUMN_FULL_SIZE):
            self.customers_tree.column(column_name, width=width, anchor=tk.CENTER)
            self.customers_tree.heading(column_name, text=column_name)

        scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        scrollbar.configure(command=self.customers_tree.set)
        self.customers_tree.configure(yscrollcommand=scrollbar)
        self.customers_tree.bind('<ButtonRelease-1>', self.get_selected_customer)

        
        records = db.return_customers()
        for record in records:
            
            self.customers_tree.insert('', tk.END, values=record)

    def clear_customer_entries(self):
        
        if self.error_label:
            self.error_label.destroy()

        self.login_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.perm_entry.delete(0, tk.END)

    def search_customer(self):
       
        try:
            if self.error_label:
                self.error_label.destroy()

            records = db.search_customer(self.login_entry.get(), self.name_entry.get(),
                                         self.phone_entry.get(), self.email_entry.get(),
                                         self.perm_entry.get())

            for child in self.customers_tree.get_children():
                self.customers_tree.delete(child)
            for record in records:
                self.customers_tree.insert('', tk.END, values=record)

        except KeyError:
            pass

    def delete_customer(self):
        
        if self.error_label:
            self.error_label.destroy()

        
        if not self.customers_tree.selection():
            self.error_message("Wybierz z listy")
            return

       
        selected_record = self.customers_tree.set(self.customers_tree.selection())
        record = db.return_customer(selected_record[CUSTOMER_COLUMN_FULL[0]])

        
        if record:
            customer_info = "{}\n{}\n{}".format(record[0], record[1], record[2])

            
            answer = messagebox.askquestion('Agroturystyka', "Usuń:\n{}".format(customer_info))
            if answer == 'Tak':
                db.delete_customer(selected_record[CUSTOMER_COLUMN_FULL[0]])
                
                self.initialize_menu()

        
        else:
            self.error_message("Nie istnieje w bazie")

    def update_customer(self):
        
        if self.error_label:
            self.error_label.destroy()

       
        if not self.customers_tree.selection():
            self.error_message("Wybierz z listy")
            return

        
        if not self.login_entry.get():
            self.error_message("Login nie może być pusty")
        elif not self.name_entry.get():
            self.error_message("Imię nie może być puste")
        elif not self.email_entry.get():
            self.error_message("Email nie może być pusty")
        elif self.perm_entry.get() not in ['0', '1']:
            self.error_message("perm must be int 0 or 1")

        
        elif self.phone_entry.get() and not my_config.is_integer(self.phone_entry.get()):
            self.error_message("Zły numer telefonu")

        
        else:
            current_record = self.customers_tree.set(self.customers_tree.selection())
            db.update_customer(current_record[CUSTOMER_COLUMN_FULL[0]], self.login_entry.get(),
                               self.name_entry.get(), self.email_entry.get(),
                               self.phone_entry.get(), self.perm_entry.get())

            
            self.initialize_menu()

    def get_selected_customer(self, event):
        
        self.clear_customer_entries()
        if self.error_label:
            self.error_label.destroy()

        if self.customers_tree.selection():
            record = self.customers_tree.set(self.customers_tree.selection())

            self.login_entry.insert(tk.END, record[CUSTOMER_COLUMN_FULL[1]])
            self.name_entry.insert(tk.END, record[CUSTOMER_COLUMN_FULL[2]])
            self.phone_entry.insert(tk.END, record[CUSTOMER_COLUMN_FULL[3]])
            self.email_entry.insert(tk.END, record[CUSTOMER_COLUMN_FULL[4]])
            self.perm_entry.insert(tk.END, record[CUSTOMER_COLUMN_FULL[5]])

    def error_message(self, name):
        
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.entry_frame, text=name,
                                    bg=my_config.BACKGROUND, fg=my_config.ERROR_FOREGROUND)
        self.error_label.grid(row=6, column=1)

    def go_to_order_window(self):
        
        self.frame.destroy()
        self.entry_frame.destroy()
        self.listbox_frame.destroy()
        application = OrdersMenu(self.master)
        application.initialize_menu()

    def go_to_product_window(self):
        
        self.frame.destroy()
        self.entry_frame.destroy()
        self.listbox_frame.destroy()
        application = ProductsMenu(self.master)
        application.initialize_menu()

    def exit_admin_window(self):
       
        self.frame.destroy()
        self.entry_frame.destroy()
        self.listbox_frame.destroy()
        application = login_window.LoginWindow(self.master)
        application.initialize_login_window()


class ProductsMenu:
    

    def __init__(self, master):
        
        self.master = master
        self.master.geometry(ADMIN_WINDOW_SIZE)
        self.master.configure(bg=my_config.BACKGROUND)
        self.master.title(my_config.APP_NAME)

        
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.frame.pack()
        
        self.entry_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.entry_frame.pack()
        
        self.listbox_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.listbox_frame.pack()

        
        self.error_label = tk.Label()

        self.product_tree = None
        self.description_entry = None
        self.in_stock_entry = None
        self.product_name_entry = None
        self.product_price_entry = None

    def initialize_menu(self):
        
        self.frame.destroy()
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.frame.pack()

        self.entry_frame.destroy()
        self.entry_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.entry_frame.pack()

        self.listbox_frame.destroy()
        self.listbox_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.listbox_frame.pack()

        if self.error_label:
            self.error_label.destroy()

        
        customer_button = tk.Button(self.frame, text='Gość', command=self.go_to_customer_window,
                                    width=30, bg=my_config.FOREGROUND)
        customer_button.grid(row=0, column=0, pady=10)
        order_button = tk.Button(self.frame, text='Rezerwacja', command=self.go_to_order_window,
                                 width=30, bg=my_config.FOREGROUND)
        order_button.grid(row=0, column=1, )
        product_button = tk.Button(self.frame, text='Produkt', command=self.initialize_menu,
                                   width=30, bg=my_config.FOREGROUND)
        product_button.grid(row=0, column=2)

        
        product_name_label = tk.Label(self.entry_frame, text='Nazwa:', bg=my_config.BACKGROUND)
        product_name_label.grid(row=0, column=0, sticky=tk.E)
        product_price_label = tk.Label(self.entry_frame, text='Cena:', bg=my_config.BACKGROUND)
        product_price_label.grid(row=1, column=0, sticky=tk.E)
        in_stock_label = tk.Label(self.entry_frame, text='Dostępne:', bg=my_config.BACKGROUND)
        in_stock_label.grid(row=2, column=0, sticky=tk.E)
        description_label = tk.Label(self.entry_frame, text='Opis:',
                                     bg=my_config.BACKGROUND)
        description_label.grid(row=3, column=0, sticky=tk.E)

        
        self.product_name_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.product_name_entry.grid(row=0, column=1)
        self.product_price_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.product_price_entry.grid(row=1, column=1)
        self.in_stock_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.in_stock_entry.grid(row=2, column=1)
        self.description_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.description_entry.grid(row=3, column=1)

        # przyciski
        add_button = tk.Button(self.entry_frame, text='Dodaj', command=self.add_product,
                               width=20, bg=my_config.FOREGROUND)
        add_button.grid(row=0, column=2, padx=20)
        search_button = tk.Button(self.entry_frame, text='Szukaj', command=self.search_product,
                                  width=20, bg=my_config.FOREGROUND)
        search_button.grid(row=1, column=2)
        update_button = tk.Button(self.entry_frame, text='Aktualizuj', command=self.update_product,
                                  width=20, bg=my_config.FOREGROUND)
        update_button.grid(row=2, column=2)
        clear_button = tk.Button(self.entry_frame, text='Wyczyść', command=self.clear_product_entries,
                                 width=20, bg=my_config.FOREGROUND)
        clear_button.grid(row=3, column=2)
        delete_button = tk.Button(self.entry_frame, text='Usuń', command=self.delete_product,
                                  width=20, bg=my_config.FOREGROUND)
        delete_button.grid(row=4, column=2)

        exit_button = tk.Button(self.entry_frame, text='Wyloguj', command=self.exit_admin_window,
                                width=20, bg=my_config.FOREGROUND)
        exit_button.grid(row=5, column=2)

        list_label = tk.Label(self.listbox_frame, text='Lista produktów',
                              width=100, bg=my_config.BACKGROUND)
        list_label.grid(row=0, column=0)

        
        self.product_tree = Treeview(self.listbox_frame, columns=PRODUCT_COLUMNS,
                                     show='headings', height=10)
        self.product_tree.grid(row=1, column=0)

        for column_name, width in zip(PRODUCT_COLUMNS, PRODUCT_COLUMNS_SIZE):
            self.product_tree.column(column_name, width=width, anchor=tk.CENTER)
            self.product_tree.heading(column_name, text=column_name)

        scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        scrollbar.configure(command=self.product_tree.set)
        self.product_tree.configure(yscrollcommand=scrollbar)
        self.product_tree.bind('<ButtonRelease-1>', self.get_selected_product)

        
        records = db.return_products()
        for record in records:
            
            self.product_tree.insert('', tk.END, values=record)

    def clear_product_entries(self):
        
        if self.error_label:
            self.error_label.destroy()

        self.product_name_entry.delete(0, tk.END)
        self.product_price_entry.delete(0, tk.END)
        self.in_stock_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def add_product(self):
        #nowy 
        if self.error_label:
            self.error_label.destroy()

        if not self.product_name_entry.get():
            self.error_message("Błąd nazwy")
        elif not my_config.is_float(self.product_price_entry.get()) or float(
                self.product_price_entry.get()) < 1.0:
            self.error_message("Dodaj cenę")
        elif not my_config.is_integer(self.in_stock_entry.get()) or int(
                self.in_stock_entry.get()) < 0:
            self.error_message("Dodaj ilość")

        
        else:
           
            if db.is_product_exists(self.product_name_entry.get()):
                self.error_message("'{}' Istnieje".format(self.product_name_entry.get()))

            else:
                db.add_product(self.product_name_entry.get(), self.product_price_entry.get(),
                               self.in_stock_entry.get(), self.description_entry.get())

                
                self.initialize_menu()

    def search_product(self):
        
        if self.error_label:
            self.error_label.destroy()

        try:
            for child in self.product_tree.get_children():
                self.product_tree.delete(child)

            records = db.search_products(self.product_name_entry.get(), self.product_price_entry.get(),
                                         self.in_stock_entry.get(), self.description_entry.get())
            for record in records:
                
                self.product_tree.insert('', tk.END, values=record)

        except KeyError:
            pass

    def delete_product(self):
       #usun 
        if self.error_label:
            self.error_label.destroy()

       
        if not self.product_tree.selection():
            self.error_message("Wybierz z listy")
            return

        selected_record = self.product_tree.set(self.product_tree.selection())
        record = db.return_product(selected_record[PRODUCT_COLUMNS[0]])

        if record:
            product_info = "{}\n{}\n{}".format(record[1], record[2], record[3])

            
            answer = messagebox.askquestion('Agroturystyka', "Usuń:\n{}".format(product_info))
            if answer == 'tak':
                db.delete_product(selected_record[PRODUCT_COLUMNS[0]])
                
                self.initialize_menu()

        
        else:
            self.error_message("Nie istnieje")

    def update_product(self):
        
        try:
            if self.error_label:
                self.error_label.destroy()

            
            if not self.product_tree.selection():
                self.error_message("Wybierz z listy")
                return

            
            if not self.product_name_entry.get():
                self.error_message("Dodaj nazwę")
            elif not my_config.is_float(self.product_price_entry.get()) or float(
                    self.product_price_entry.get()) < 1.0:
                self.error_message("Dodaj cenę")
            elif not my_config.is_integer(self.in_stock_entry.get()) or int(
                    self.in_stock_entry.get()) < 0:
                self.error_message("Dodaj ilość")

            else:
                
                record = self.product_tree.set(self.product_tree.selection())
                db.update_product(record[PRODUCT_COLUMNS[0]], self.product_name_entry.get(),
                                  self.product_price_entry.get(),
                                  self.in_stock_entry.get(), self.description_entry.get())

               
                self.initialize_menu()
        except KeyError:
            pass

    def get_selected_product(self, event):
        
        self.clear_product_entries()
        if self.error_label:
            self.error_label.destroy()
        try:
            if self.product_tree.selection():
                record = self.product_tree.set(self.product_tree.selection())
                self.product_name_entry.insert(tk.END, record[PRODUCT_COLUMNS[1]])
                self.product_price_entry.insert(tk.END, record[PRODUCT_COLUMNS[2]])
                self.in_stock_entry.insert(tk.END, record[PRODUCT_COLUMNS[3]])
                self.description_entry.insert(tk.END, record[PRODUCT_COLUMNS[4]])

        except KeyError:
            pass

    def error_message(self, name):
       
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.entry_frame, text=name,
                                    bg=my_config.BACKGROUND, fg=my_config.ERROR_FOREGROUND)
        self.error_label.grid(row=4, column=1)

    def go_to_order_window(self):
       
        self.frame.destroy()
        self.entry_frame.destroy()
        self.listbox_frame.destroy()
        application = OrdersMenu(self.master)
        application.initialize_menu()

    def go_to_customer_window(self):
        
        self.frame.destroy()
        self.entry_frame.destroy()
        self.listbox_frame.destroy()
        application = CustomersMenu(self.master)
        application.initialize_menu()

    def exit_admin_window(self):
        
        self.frame.destroy()
        self.entry_frame.destroy()
        self.listbox_frame.destroy()
        application = login_window.LoginWindow(self.master)
        application.initialize_login_window()


class OrdersMenu:
    
    def __init__(self, master):
       
        self.master = master
        self.master.geometry(ADMIN_WINDOW_SIZE)
        self.master.configure(bg=my_config.BACKGROUND)
        self.master.title(my_config.APP_NAME)

        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.frame.pack()
        
        self.entry_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.entry_frame.pack()
        
        self.orders_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.orders_frame.pack()
        self.products_customers_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.products_customers_frame.pack()

        
        self.error_label = tk.Label()

        self.order_tree = None
        self.product_tree = None
        self.customers_tree = None
        self.id_product_entry = None
        self.id_customer_entry = None
        self.quantity_entry = None
        self.location_entry = None
        self.payment_status_entry = None
        self.send_status_entry = None

    def initialize_menu(self):
        
        self.frame.destroy()
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.frame.pack()

        self.entry_frame.destroy()
        self.entry_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.entry_frame.pack()

        self.orders_frame.destroy()
        self.orders_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.orders_frame.pack()

        self.products_customers_frame.destroy()
        self.products_customers_frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.products_customers_frame.pack()

        if self.error_label:
            self.error_label.destroy()

        
        customer_button = tk.Button(self.frame, text='Gość', command=self.go_to_customer_window,
                                    width=30, bg=my_config.FOREGROUND)
        customer_button.grid(row=0, column=0, pady=10)
        order_button = tk.Button(self.frame, text='Rezrwacja', command=self.initialize_menu,
                                 width=30, bg=my_config.FOREGROUND)
        order_button.grid(row=0, column=1, )
        product_button = tk.Button(self.frame, text='Produkt', command=self.go_to_product_window,
                                   width=30, bg=my_config.FOREGROUND)
        product_button.grid(row=0, column=2)

       #label
        id_customer_label = tk.Label(self.entry_frame, text='Gość ID:', bg=my_config.BACKGROUND)
        id_customer_label.grid(row=0, column=0, sticky=tk.E)
        id_product_label = tk.Label(self.entry_frame, text='Produkt ID:', bg=my_config.BACKGROUND)
        id_product_label.grid(row=1, column=0, sticky=tk.E)
        quantity_label = tk.Label(self.entry_frame, text='Ilość:', bg=my_config.BACKGROUND)
        quantity_label.grid(row=2, column=0, sticky=tk.E)
        payment_status_label = tk.Label(self.entry_frame, text='Status płatności:', bg=my_config.BACKGROUND)
        payment_status_label.grid(row=3, column=0, sticky=tk.E)
        send_status_label = tk.Label(self.entry_frame, text='Wyślij status:', bg=my_config.BACKGROUND)
        send_status_label.grid(row=4, column=0, sticky=tk.E)
        location_label = tk.Label(self.entry_frame, text='Liczba osób:', bg=my_config.BACKGROUND)
        location_label.grid(row=5, column=0, sticky=tk.E)

        
        self.id_customer_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.id_customer_entry.grid(row=0, column=1)
        self.id_product_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.id_product_entry.grid(row=1, column=1)
        self.quantity_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.quantity_entry.grid(row=2, column=1)
        self.payment_status_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.payment_status_entry.grid(row=3, column=1)
        self.send_status_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.send_status_entry.grid(row=4, column=1)
        self.location_entry = tk.Entry(self.entry_frame, width=30, bg=my_config.FOREGROUND)
        self.location_entry.grid(row=5, column=1)

        # przyciski
        search_button = tk.Button(self.entry_frame, text='Szukaj', command=self.search_order, width=20,
                                  bg=my_config.FOREGROUND)
        search_button.grid(row=0, column=2, padx=20)
        add_button = tk.Button(self.entry_frame, text='Dodaj', command=self.add_order,
                               width=20, bg=my_config.FOREGROUND)
        add_button.grid(row=1, column=2, padx=20)
        clear_button = tk.Button(self.entry_frame, text='Wyczyść', command=self.initialize_menu,
                                 width=20, bg=my_config.FOREGROUND)
        clear_button.grid(row=2, column=2)
        delete_button = tk.Button(self.entry_frame, text='Usuń', command=self.delete_order,
                                  width=20, bg=my_config.FOREGROUND)
        delete_button.grid(row=3, column=2)
        exit_button = tk.Button(self.entry_frame, text='Wyloguj', command=self.exit_admin_window,
                                width=20, bg=my_config.FOREGROUND)
        exit_button.grid(row=4, column=2)

        
        list_label = tk.Label(self.orders_frame, text='Rezerwacje', bg=my_config.BACKGROUND)
        list_label.grid(row=0, column=0)

        self.order_tree = Treeview(self.orders_frame, columns=ORDER_COLUMNS, show='headings', height=8)
        self.order_tree.grid(row=1, column=0, padx=100)

        scrollbar_y = tk.Scrollbar(self.orders_frame, orient=tk.VERTICAL)
        scrollbar_y.configure(command=self.order_tree.set)
        scrollbar_x = tk.Scrollbar(self.orders_frame, orient=tk.HORIZONTAL)
        scrollbar_x.configure(command=self.order_tree.xview())
        self.order_tree.configure(yscrollcommand=scrollbar_y)
        self.order_tree.configure(xscrollcommand=scrollbar_x)
        self.order_tree.bind('<ButtonRelease-1>', self.order_list_manager)

        for column_name, width in zip(ORDER_COLUMNS, ORDER_COLUMNS_SIZE):
            self.order_tree.column(column_name, width=width, anchor=tk.CENTER)
            self.order_tree.heading(column_name, text=column_name)

       
        list_label1 = tk.Label(self.products_customers_frame, text='Produkty',
                               width=25, bg=my_config.BACKGROUND)
        list_label1.grid(row=0, column=0)

        self.product_tree = Treeview(self.products_customers_frame,
                                     columns=PRODUCT_COLUMNS, show='headings', height=8)
        self.product_tree.grid(row=1, column=0, padx=10)
        scrollbar_y = tk.Scrollbar(self.products_customers_frame, orient=tk.VERTICAL)
        scrollbar_y.configure(command=self.product_tree.set)
        scrollbar_x = tk.Scrollbar(self.products_customers_frame, orient=tk.HORIZONTAL)
        scrollbar_x.configure(command=self.order_tree.xview())
        self.product_tree.configure(yscrollcommand=scrollbar_y)
        self.product_tree.configure(xscrollcommand=scrollbar_x)
        self.product_tree.bind('<ButtonRelease-1>', self.product_list_manager)

        for column_name, width in zip(PRODUCT_COLUMNS, PRODUCT_COLUMNS_SIZE):
            self.product_tree.column(column_name, width=width, anchor=tk.CENTER)
            self.product_tree.heading(column_name, text=column_name)

       
        list_label2 = tk.Label(self.products_customers_frame, text='Goście',
                               width=25, bg=my_config.BACKGROUND)
        list_label2.grid(row=0, column=1)
        self.customers_tree = Treeview(self.products_customers_frame,
                                       columns=CUSTOMER_COLUMNS, show='headings', height=8)
        self.customers_tree.grid(row=1, column=1)

        scrollbar_y = tk.Scrollbar(self.products_customers_frame, orient=tk.VERTICAL)
        scrollbar_y.configure(command=self.customers_tree.set)
        scrollbar_x = tk.Scrollbar(self.products_customers_frame, orient=tk.HORIZONTAL)
        scrollbar_x.configure(command=self.order_tree.xview())
        self.customers_tree.configure(yscrollcommand=scrollbar_y)
        self.customers_tree.configure(xscrollcommand=scrollbar_x)
        self.customers_tree.bind('<ButtonRelease-1>', self.customer_list_manager)

        for column_name, width in zip(CUSTOMER_COLUMNS, CUSTOMER_COLUMNS_SIZE):
            self.customers_tree.column(column_name, width=width, anchor=tk.CENTER)
            self.customers_tree.heading(column_name, text=column_name)

        
        records = db.return_orders()
        for record in records:
            self.order_tree.insert('', tk.END, values=[
                record[0], record[3], record[5], record[6], record[8], record[7]])

        
        records = db.return_products()
        for record in records:
            self.product_tree.insert('', tk.END, values=record)

        
        records = db.return_customers()
        for record in records:
            self.customers_tree.insert('', tk.END, values=[record[0], record[2], record[4]])

    def add_order(self):
      
        if self.error_label:
            self.error_label.destroy()

       
        if not self.id_customer_entry.get():
            self.error_message("Brak ID gościa")
        elif not self.id_product_entry.get():
            self.error_message("Brak ID produktu")
        elif not my_config.is_integer(self.quantity_entry.get()) or int(self.quantity_entry.get()) < 1:
            self.error_message("Dodaj ilość")

        elif self.payment_status_entry.get() not in ['0', '1']:
            self.error_message("Status musi wynosić 0 lub 1")
        elif self.send_status_entry.get() not in ['0', '1']:
            self.error_message("Status musi wynosić 0 lub 1")
        elif not self.location_entry.get():
            self.error_message("Brak lokalizacji")

        
        elif not db.is_customer_id_exist(self.id_customer_entry.get()) or not db.is_product_id_exists(
                self.id_product_entry.get()):
            self.error_message("ID nie istnieje")

       
        elif db.add_order(self.id_customer_entry.get(), self.id_product_entry.get(),
                          self.quantity_entry.get(), self.location_entry.get(),
                          self.payment_status_entry.get(), self.send_status_entry.get()):

            self.initialize_menu()
        else:
            self.error_message("Brak wystarczającej ilości")

    def delete_order(self):
        #usun 
        if self.error_label:
            self.error_label.destroy()

       
        if not self.order_tree.selection():
            self.error_message("Wybierz z listy")
            return

       
        answer = messagebox.askquestion('Agroturystyka', 'Usuń:\n')
        if answer == 'tak':
            selected_record = self.order_tree.set(self.order_tree.selection())
            db.delete_order(selected_record[ORDER_COLUMNS[0]])

            self.initialize_menu()

    def search_order(self):
        
        if self.error_label:
            self.error_label.destroy()

        records = db.search_orders(self.id_product_entry.get(), self.id_customer_entry.get(),
                                   self.quantity_entry.get(), self.payment_status_entry.get(),
                                   self.send_status_entry.get(), self.location_entry.get())

        for child in self.order_tree.get_children():
            self.order_tree.delete(child)
        for record in records:
            self.order_tree.insert('', tk.END, values=[
                record[0], record[3], record[5], record[6], record[8], record[7]])

    def order_list_manager(self, event):
        
        if self.error_label:
            self.error_label.destroy()

        
        if self.order_tree.selection():
            current_record = self.order_tree.set(self.order_tree.selection())

            self.id_customer_entry.delete(0, tk.END)
            self.id_product_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.payment_status_entry.delete(0, tk.END)
            self.send_status_entry.delete(0, tk.END)
            self.location_entry.delete(0, tk.END)

            order_data = db.return_order(current_record[ORDER_COLUMNS[0]])
            self.id_customer_entry.insert(tk.END, order_data[1])
            self.id_product_entry.insert(tk.END, order_data[2])

            self.quantity_entry.insert(tk.END, current_record[ORDER_COLUMNS[1]])
            self.payment_status_entry.insert(tk.END, current_record[ORDER_COLUMNS[2]])
            self.send_status_entry.insert(tk.END, current_record[ORDER_COLUMNS[3]])
            self.location_entry.insert(tk.END, current_record[ORDER_COLUMNS[4]])

           
            record = db.return_customer(order_data[1])
            for child in self.customers_tree.get_children():
                self.customers_tree.delete(child)
            self.customers_tree.insert('', tk.END, values=[record[0], record[3], record[5]])

           
            record = db.return_product(order_data[2])
            for child in self.product_tree.get_children():
                self.product_tree.delete(child)
            self.product_tree.insert('', tk.END, values=record)

    def product_list_manager(self, event):
        
        if self.error_label:
            self.error_label.destroy()

        
        if self.product_tree.selection():
            current_record = self.product_tree.set(self.product_tree.selection())

            self.id_product_entry.delete(0, tk.END)
            self.id_product_entry.insert(tk.END, current_record[PRODUCT_COLUMNS[0]])

            
            records = db.return_product_orders(current_record[PRODUCT_COLUMNS[0]])
            for child in self.order_tree.get_children():
                self.order_tree.delete(child)

            for record in records:
                self.order_tree.insert('', tk.END, values=[
                    record[0], record[3], record[5], record[6], record[8], record[7]])

    def customer_list_manager(self, event):
        
        if self.error_label:
            self.error_label.destroy()

        
        if self.customers_tree.selection():
            current_record = self.customers_tree.set(self.customers_tree.selection())

            self.id_customer_entry.delete(0, tk.END)
            self.id_customer_entry.insert(tk.END, current_record[CUSTOMER_COLUMNS[0]])

            
            records = db.return_customer_orders(current_record[CUSTOMER_COLUMNS[0]])
            for child in self.order_tree.get_children():
                self.order_tree.delete(child)

            for record in records:
                self.order_tree.insert('', tk.END, values=[
                    record[0], record[3], record[5], record[6], record[8], record[7]])

    def error_message(self, name):
        
        if self.error_label:
            self.error_label.destroy()

        self.error_label = tk.Label(self.frame, text=name, bg=my_config.BACKGROUND,
                                    fg=my_config.ERROR_FOREGROUND)
        self.error_label.grid(row=11, column=1)

    def go_to_customer_window(self):
        
        self.frame.destroy()
        self.entry_frame.destroy()
        self.orders_frame.destroy()
        self.products_customers_frame.destroy()
        application = CustomersMenu(self.master)
        application.initialize_menu()

    def go_to_product_window(self):
       
        self.frame.destroy()
        self.entry_frame.destroy()
        self.orders_frame.destroy()
        self.products_customers_frame.destroy()
        application = ProductsMenu(self.master)
        application.initialize_menu()

    def exit_admin_window(self):
        
        self.frame.destroy()
        self.entry_frame.destroy()
        self.orders_frame.destroy()
        self.products_customers_frame.destroy()
        application = login_window.LoginWindow(self.master)
        application.initialize_login_window()
