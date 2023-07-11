#testy
import tkinter as tk
import unittest

import admin


class ProductsMenuTest(unittest.TestCase):

    def setUp(self):
        root = tk.Tk()
        self.application = admin.ProductsMenu(root)
        self.application.initialize_menu()

    def test_clear_product_entries(self):
        self.application.product_name_entry.insert(tk.END, "Leżaki")
        self.application.product_price_entry.insert(tk.END, "1100")
        self.application.in_stock_entry.insert(tk.END, "20")
        self.application.description_entry.insert(tk.END, "Lezaki plazowe, regulowane")

        self.application.clear_product_entries()

        self.assertFalse(self.application.product_name_entry.get())
        self.assertFalse(self.application.product_price_entry.get())
        self.assertFalse(self.application.in_stock_entry.get())
        self.assertFalse(self.application.description_entry.get())

    def test_search_product(self):
        self.application.clear_product_entries()
        self.application.product_name_entry.insert(tk.END, "Leżaki")
        self.application.search_product()  

        child = self.application.product_tree.get_children()  
        self.assertTrue(self.application.product_tree.item(child)['values'][1] == "Leżaki")


class CustomersMenuTest(unittest.TestCase):

    def setUp(self):
        root = tk.Tk()
        self.application = admin.CustomersMenu(root)
        self.application.initialize_menu()

    def test_clear_customer_entries(self):
        self.application.name_entry.insert(tk.END, "Ala Makota")
        self.application.login_entry.insert(tk.END, "gosc")
        self.application.email_entry.insert(tk.END, "ala@email.com")
        self.application.phone_entry.insert(tk.END, "123123123")
        self.application.perm_entry.insert(tk.END, "2")

        self.application.clear_customer_entries()

        self.assertFalse(self.application.name_entry.get())
        self.assertFalse(self.application.login_entry.get())
        self.assertFalse(self.application.email_entry.get())
        self.assertFalse(self.application.phone_entry.get())
        self.assertFalse(self.application.perm_entry.get())

    def test_search_customer(self):
        self.application.clear_customer_entries()
        self.application.login_entry.insert(tk.END, "admin")
        self.application.search_customer()  

        child = self.application.customers_tree.get_children()  
        self.assertTrue(self.application.customers_tree.item(child)['values'][1] == "admin")


class OrdersMenuTest(unittest.TestCase):

    def setUp(self):
        root = tk.Tk()
        self.application = admin.OrdersMenu(root)
        self.application.initialize_menu()

    def test_clear_entries(self):
        self.application.id_customer_entry.insert(tk.END, "1")
        self.application.id_product_entry.insert(tk.END, "1")
        self.application.quantity_entry.insert(tk.END, "5")
        self.application.payment_status_entry.insert(tk.END, "1")
        self.application.send_status_entry.insert(tk.END, "0")
        self.application.location_entry.insert(tk.END, "Jędrychowa chatka")

        self.application.initialize_menu()

        self.assertFalse(self.application.id_customer_entry.get())
        self.assertFalse(self.application.id_product_entry.get())
        self.assertFalse(self.application.quantity_entry.get())
        self.assertFalse(self.application.payment_status_entry.get())
        self.assertFalse(self.application.send_status_entry.get())
        self.assertFalse(self.application.location_entry.get())

    def test_search_order(self):
        self.application.send_status_entry.insert(tk.END, "1")
        self.application.search_order()  
        for child in self.application.order_tree.get_children():
            self.assertTrue(self.application.order_tree.item(child)['values'][3] == 1)


if __name__ == '__main__':
    unittest.main()
