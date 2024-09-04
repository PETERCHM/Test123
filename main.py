import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import simpledialog

def connect_db():
    return sqlite3.connect('expenses.db')

def get_users():
    users = {}
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM users')
        rows = cursor.fetchall()
        for row in rows:
            users[row[1]] = row[0]
    return users

def save_expense(description, total_amount, payer_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (description, total_amount, payer_id)
            VALUES (?, ?, ?)
        ''', (description, total_amount, payer_id))
        conn.commit()
        return cursor.lastrowid

def save_payment(expense_id, user_id, amount):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO payments (expense_id, user_id, amount)
            VALUES (?, ?, ?)
        ''', (expense_id, user_id, amount))
        conn.commit()

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Sharing App")

        self.users = get_users()  # Initialize users before creating widgets
        self.create_widgets()

    def create_widgets(self):
        # Labels and Entry fields
        tk.Label(self.root, text="Expense Description:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.desc_entry = tk.Entry(self.root, width=50, font=("Arial", 14))
        self.desc_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Total Amount:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.amount_entry = tk.Entry(self.root, width=20, font=("Arial", 14))
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Payer:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.payer_var = tk.StringVar()
        self.payer_menu = tk.OptionMenu(self.root, self.payer_var, *self.get_user_names())
        self.payer_menu.config(font=("Arial", 14))
        self.payer_menu.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        tk.Button(self.root, text="Save Expense", command=self.save_expense, font=("Arial", 14)).grid(row=3, column=0, columnspan=2, pady=10)

        # Balance display
        tk.Label(self.root, text="Total Balance:", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.balance_label = tk.Label(self.root, text="0.00", font=("Arial", 14))
        self.balance_label.grid(row=4, column=1, padx=10, pady=10)

        
    def get_user_names(self):
        return list(self.users.keys())

    def save_expense(self):
        description = self.desc_entry.get()
        try:
            total_amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Total amount must be a valid number.")
            return

        payer_name = self.payer_var.get()
        payer_id = self.users.get(payer_name)

        if not description or total_amount <= 0 or not payer_id:
            messagebox.showerror("Input Error", "Please fill in all fields correctly.")
            return

        expense_id = save_expense(description, total_amount, payer_id)
        
        # Save expense details
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.payer_var.set('')
        
        # Update balance with the saved expense
        self.update_balance(expense_id, total_amount)

    def update_balance(self, expense_id, total_amount):
        # Initialize a dictionary to store contributions
        self.contributions = {user_id: 0.0 for user_id in self.users.values()}

        while True:
            # Reset paid_amount to zero for each new prompt
            paid_amount = self.prompt_for_contributions(expense_id, total_amount)

            # Calculate the remaining balance
            balance = total_amount - paid_amount

            if balance > 0:
                self.balance_label.config(text=f"{balance:.2f}")
                messagebox.showinfo("Remaining Balance", f"Remaining balance: {balance:.2f}")
            else:
                self.balance_label.config(text="0.00")
                self.show_contributions()
                break

    def prompt_for_contributions(self, expense_id, total_amount):
        paid_amount = 0.0
        while paid_amount < total_amount:
            for name, user_id in self.users.items():
                top_up_amount = tk.simpledialog.askfloat(
                    "Contribution",
                    f"Enter amount {name} will contribute towards clearing the balance:",
                    minvalue=0.0
                )
                if top_up_amount is not None:
                    save_payment(expense_id, user_id, top_up_amount)
                    paid_amount += top_up_amount
                    self.contributions[user_id] += top_up_amount
                    if paid_amount >= total_amount:
                        break
            # Show remaining balance after each contribution
            remaining_balance = total_amount - paid_amount
            if remaining_balance > 0:
                self.balance_label.config(text=f"{remaining_balance:.2f}")
                messagebox.showinfo("Remaining Balance", f"Remaining balance: {remaining_balance:.2f}")

        return paid_amount

    def show_contributions(self):
        contributions_message = "Contribution Summary:\n"
        for name, user_id in self.users.items():
            contributions_message += f"{name}: Ksh {self.contributions[user_id]:.2f}\n"

        messagebox.showinfo("Contributions", contributions_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()
