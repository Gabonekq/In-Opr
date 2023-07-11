import tkinter as tk

import admin
import gosc
import db as db
import my_config


LOGIN_WINDOW_SIZE = "300x200"
FALSE_LOG_IN_VALUE = -1


class LoginWindow:
    

    def __init__(self, master):
        
        self.master = master
        self.master.title(my_config.APP_NAME)
        self.master.geometry(LOGIN_WINDOW_SIZE)
        self.master.configure(bg=my_config.BACKGROUND)
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND, bd=15)

        
        self.error_label = tk.Label()

      
        self.login_entry = None
        self.password_entry = None
        self.name_entry = None
        self.phone_entry = None
        self.email_entry = None

    def initialize_login_window(self):
        
        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND, bd=15)

        #label
        login_label = tk.Label(self.frame, bg=my_config.BACKGROUND, text='Login:')
        login_label.grid(row=0, column=0)
        password_label = tk.Label(self.frame, bg=my_config.BACKGROUND, text='Hasło:')
        password_label.grid(row=1, column=0)
        self.login_entry = tk.Entry(self.frame, bg=my_config.FOREGROUND, width=18)
        self.login_entry.grid(row=0, column=1)
        self.password_entry = tk.Entry(self.frame, show='*', bg=my_config.FOREGROUND, width=18)
        self.password_entry.grid(row=1, column=1)

        # przyciski
        login_button = tk.Button(self.frame, text='Zaloguj', bg=my_config.FOREGROUND,
                                 command=self.login, width=16)
        login_button.grid(row=3, column=1, pady=(10, 0))
        create_button = tk.Button(self.frame, text='Zarejestruj się',
                                  bg=my_config.FOREGROUND, command=self.create_account, width=16)
        create_button.grid(row=4, column=1)
        self.frame.pack()

    def login(self):
        
        if self.error_label:
            self.error_label.destroy()

        #sprawdzenie
        if not self.login_entry.get():
            self.error_label = tk.Label(self.frame, text="Błąd loginu",
                                        fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
            self.error_label.grid(row=2, column=1)
        elif not self.password_entry.get():
            self.error_label = tk.Label(self.frame, text="Błąd hasła",
                                        fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
            self.error_label.grid(row=2, column=1)

        else:
            my_config.MY_ID, perm = db.customer_perm(self.login_entry.get(), self.password_entry.get())
            if perm == FALSE_LOG_IN_VALUE or my_config.MY_ID == FALSE_LOG_IN_VALUE:
                self.error_label = tk.Label(self.frame, text="Sprawdź ponownie",
                                            fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
                self.error_label.grid(row=2, column=1)
            elif perm == my_config.ADMIN_PERM:
                self.admin_app()
            else:
                self.customer_app()

    def create_account(self):
        #nowe konto
        self.frame.destroy()
        self.frame = tk.Frame(self.master, bg=my_config.BACKGROUND)
        self.frame.pack()

        #label
        login_label = tk.Label(self.frame, text='Login:', bg=my_config.BACKGROUND)
        login_label.grid(row=0, column=0, pady=(10, 0), sticky=tk.E)
        password_label = tk.Label(self.frame, text='Hasło:', bg=my_config.BACKGROUND)
        password_label.grid(row=1, column=0, sticky=tk.E, )
        name_label = tk.Label(self.frame, text='Imię:', bg=my_config.BACKGROUND)
        name_label.grid(row=2, column=0, sticky=tk.E)
        phone_label = tk.Label(self.frame, text='Numer telefonu:', bg=my_config.BACKGROUND)
        phone_label.grid(row=3, column=0, sticky=tk.E)
        email_label = tk.Label(self.frame, text='Email:', bg=my_config.BACKGROUND)
        email_label.grid(row=4, column=0, sticky=tk.E)

        
        self.login_entry = tk.Entry(self.frame, width=18, bg=my_config.FOREGROUND)
        self.login_entry.grid(row=0, column=1, pady=(10, 0))
        self.password_entry = tk.Entry(self.frame, width=18, show='*', bg=my_config.FOREGROUND)
        self.password_entry.grid(row=1, column=1)
        self.name_entry = tk.Entry(self.frame, width=18, bg=my_config.FOREGROUND)
        self.name_entry.grid(row=2, column=1)
        self.phone_entry = tk.Entry(self.frame, width=18, bg=my_config.FOREGROUND)
        self.phone_entry.grid(row=3, column=1)
        self.email_entry = tk.Entry(self.frame, width=18, bg=my_config.FOREGROUND)
        self.email_entry.grid(row=4, column=1)

        
        login_button = tk.Button(self.frame, text='Utwórz', command=self.create_account_db,
                                 width=16, bg=my_config.FOREGROUND)
        login_button.grid(row=6, column=0, pady=(20, 0))
        create_button = tk.Button(self.frame, text='Cofnij', command=self.initialize_login_window,
                                  width=16, bg=my_config.FOREGROUND)
        create_button.grid(row=6, column=1, pady=(20, 0))

    def create_account_db(self):
        
        if self.error_label:
            self.error_label.destroy()

        #sprawdzenie
        if not self.login_entry.get():
            self.error_label = tk.Label(self.frame, text="Błąd loginu",
                                        fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
            self.error_label.grid(row=5, column=1)
        elif len(self.password_entry.get()) < 6:
            self.error_label = tk.Label(self.frame, text="Hasło musi mieć min. 6 znaków",
                                        fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
            self.error_label.grid(row=5, column=1)
        elif not self.name_entry.get():
            self.error_label = tk.Label(self.frame, text="Błąd imienia",
                                        fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
            self.error_label.grid(row=5, column=1)
        elif not self.email_entry.get():
            self.error_label = tk.Label(self.frame, text="Błąd email",
                                        fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
            self.error_label.grid(row=5, column=1)
        elif self.phone_entry.get() and not my_config.is_integer(self.phone_entry.get()):
            self.error_label = tk.Label(self.frame, text="Zły numer",
                                        fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
            self.error_label.grid(row=5, column=1)

        else:
            # szukanie w bazie
            exist = db.is_customer_exists(self.login_entry.get(), self.email_entry.get())
            if exist == my_config.CUSTOMER_EMAIL:
                self.error_label = tk.Label(self.frame, text="Email zajęty.".format(exist),
                                            fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
                self.error_label.grid(row=5, column=1)

            elif exist == my_config.CUSTOMER_LOGIN:
                self.error_label = tk.Label(self.frame, text="Login zajęty.".format(exist),
                                            fg=my_config.ERROR_FOREGROUND, bg=my_config.BACKGROUND)
                self.error_label.grid(row=5, column=1)
            else:
                db.add_customer(self.login_entry.get(), self.password_entry.get(),
                                self.name_entry.get(), self.phone_entry.get(),
                                self.email_entry.get())
                self.frame.destroy()
                application = LoginWindow(self.master)
                application.initialize_login_window()

    def admin_app(self):
        #admin
        self.frame.destroy()
        application = admin.CustomersMenu(self.master)
        application.initialize_menu()

    def customer_app(self):
        #gosc
        self.frame.destroy()
        application = gosc.CustomerApp(self.master)
        application.initialize_main_buttons()
