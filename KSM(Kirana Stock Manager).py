import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
from plyer import notification

class KiranaStockManager:
    def __init__(self):
        self.stock = {}
        self.limits = {}
        self.data_file = "test.txt"
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    item, quantity, limit = line.strip().split(',')
                    self.stock[item] = int(quantity)
                    if limit != 'None':
                        self.limits[item] = int(limit)
        except FileNotFoundError:
            pass

    def view_available_stock(self):
        if not self.stock:
            self.show_info("No stock available.")
        else:
            stock_info = "\nAvailable Stock:\n"
            for item, quantity in self.stock.items():
                limit = self.limits.get(item, None)
                if limit is not None and quantity < limit:
                    stock_info += f"{item}: {quantity} units (Insufficient! Please order more stock.)\n"
                else:
                    stock_info += f"{item}: {quantity} units\n"
            self.show_info(stock_info)

    def check_stock_limits(self):
        for item, quantity in self.stock.items():
            limit = self.limits.get(item, None)
            if limit is not None and quantity < limit:
                notification_title = f"Stock Alert: {item}"
                notification_message = f"Stock of {item} is below the set limit! Current quantity: {quantity}"
                notification.notify(
                    title=notification_title,
                    message=notification_message,
                    app_icon=None, 
                    timeout=10,  
                )

    def record_sold_stock(self, item, quantity_sold):
        if item in self.stock:
            try:
                if quantity_sold > self.stock[item]:
                    self.show_error("Error: Insufficient stock available.")
                else:
                    self.stock[item] -= quantity_sold
                    self.show_info(f"{quantity_sold} units of {item} sold successfully.")
                    self.check_stock_limits()
            except ValueError:
                self.show_error("Error: Please enter a valid quantity.")
        else:
            self.show_error("Error: Item not found in stock.")

    def add_new_stock(self, item, quantity_added):
        try:
            if item in self.stock:
                self.stock[item] += quantity_added
            else:
                self.stock[item] = quantity_added
            self.show_info(f"{quantity_added} units of {item} added to stock.")
            self.check_stock_limits()
        except ValueError:
            self.show_error("Error: Please enter a valid quantity.")

    def set_quantity_limits(self, item, limit):
        try:
            self.limits[item] = limit
            self.show_info(f"Quantity limit set for {item}: {limit} units.")
        except ValueError:
            self.show_error("Error: Please enter a valid quantity.")

    def save_data(self):
        with open(self.data_file, 'w') as file:
            for item, quantity in self.stock.items():
                limit = self.limits.get(item, 'None')
                file.write(f"{item},{quantity},{limit}\n")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.view_available_stock()
            elif choice == '2':
                item = input("Enter the name of the sold item (or type 'done' to finish): ")
                if item.lower() != 'done':
                    try:
                        quantity_sold = int(input(f"Enter the quantity of {item} sold: "))
                        self.record_sold_stock(item, quantity_sold)
                    except ValueError:
                        self.show_error("Error: Please enter a valid quantity.")
            elif choice == '3':
                item = input("Enter the name of the new item (or type 'done' to finish): ")
                if item.lower() != 'done':
                    try:
                        quantity_added = int(input(f"Enter the quantity of {item} to be added: "))
                        self.add_new_stock(item, quantity_added)
                    except ValueError:
                        self.show_error("Error: Please enter a valid quantity.")
            elif choice == '4':
                item = input("Enter the name of the item to set a quantity limit (or type 'done' to finish): ")
                if item.lower() != 'done':
                    try:
                        limit = int(input(f"Enter the quantity limit for {item}: "))
                        self.set_quantity_limits(item, limit)
                    except ValueError:
                        self.show_error("Error: Please enter a valid quantity.")
            elif choice == '5':
                self.show_info("Exiting Kirana Stock Manager. Goodbye!")
                self.save_data()
                break
            else:
                self.show_error("Error: Invalid choice. Please enter a number between 1 and 5.")

    def display_menu(self):
        print("Welcome To Kirana Stock Manager")
        print("Enter the number to perform the respective task.")
        print("1: View Available Stock")
        print("2: Sold Stock")
        print("3: Add New Stock")
        print("4: Set Quantity Limit")
        print("5: Exit")

    def show_info(self, message):
        messagebox.showinfo("Information", message)

    def show_error(self, message):
        messagebox.showerror("Error", message)


class KiranaStockManagerGUI:
    def __init__(self, master, stock_manager):
        self.master = master
        self.master.title("Kirana Stock Manager")
        self.stock_manager = stock_manager

     
        self.master.configure(bg="#B2EBF2")  

     
        self.label = tk.Label(master, text="Welcome To Kirana Stock Manager", bg="#2FCBFD", fg="BLACK", font=("ARIAL", 18))
        self.label.pack()

        
        button_style = ttk.Style()
        button_style.configure("TButton", font=("Helvetica", 12), padding=10, background="#34F5C5", foreground="black")

        self.view_stock_button = ttk.Button(master, text="View Available Stock", command=self.view_stock)
        self.view_stock_button.pack(pady=5)

        self.sold_stock_button = ttk.Button(master, text="Sell Item", command=self.record_sold_stock)
        self.sold_stock_button.pack(pady=5)

        self.add_stock_button = ttk.Button(master, text="Add New Stock", command=self.add_new_stock)
        self.add_stock_button.pack(pady=5)

        self.set_limit_button = ttk.Button(master, text="Set Quantity Limit", command=self.set_quantity_limit)
        self.set_limit_button.pack(pady=5)

        self.exit_button = ttk.Button(master, text="Exit", command=self.exit)
        self.exit_button.pack(pady=5)

    def view_stock(self):
        self.stock_manager.view_available_stock()

    def record_sold_stock(self):
        item = self.get_user_input("Enter the name of the sold item (or type 'done' to finish):")
        if item.lower() != 'done':
            try:
                quantity_sold = int(self.get_user_input(f"Enter the quantity of {item} sold:"))
                self.stock_manager.record_sold_stock(item, quantity_sold)
            except ValueError:
                self.show_error("Error: Please enter a valid quantity.")

    def add_new_stock(self):
        item = self.get_user_input("Enter the name of the new item (or type 'done' to finish):")
        if item.lower() != 'done':
            try:
                quantity_added = int(self.get_user_input(f"Enter the quantity of {item} to be added:"))
                self.stock_manager.add_new_stock(item, quantity_added)
            except ValueError:
                self.show_error("Error: Please enter a valid quantity.")

    def set_quantity_limit(self):
        item = self.get_user_input("Enter the name of the item to set a quantity limit (or type 'done' to finish):")
        if item.lower() != 'done':
            try:
                limit = int(self.get_user_input(f"Enter the quantity limit for {item}:"))
                self.stock_manager.set_quantity_limits(item, limit)
            except ValueError:
                self.show_error("Error: Please enter a valid quantity.")

    def exit(self):
        self.master.destroy()

    def get_user_input(self, prompt):
        user_input = simpledialog.askstring("User Input", prompt)
        return user_input if user_input is not None and user_input.lower() != 'done' else ""

    def show_error(self, message):
        messagebox.showerror("Error", message)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")  
    kirana_manager = KiranaStockManager()
    gui = KiranaStockManagerGUI(root, kirana_manager)
    kirana_manager.run()
    root.mainloop()