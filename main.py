import sqlite3

def connect_db():
    return sqlite3.connect('expenses.db')

def prompt_top_up(balance, users):
    print(f"\nRemaining balance to be cleared: {balance:.2f}")
    top_up_contributors = {}
    
    for name, user_id in users.items():
        top_up_amount = input(f"Enter the amount {name} wants to contribute towards clearing the balance (or press Enter to skip): ")
        if top_up_amount:
            top_up_contributors[user_id] = float(top_up_amount)
    
    return top_up_contributors

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

def get_users():
    users = {}
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM users')
        rows = cursor.fetchall()
        for row in rows:
            users[row[1]] = row[0]  # map name to id
    return users

def main():
    users = get_users()
    if not users:
        print("No users found in the database. Please add users first.")
        return

    # Prompt for expense details
    description = input("Enter the expense description: ")
    total_amount = float(input("Enter the total amount: "))

    # Prompt for the payer
    payer_name = input(f"Who paid the {description}? (Names from database): ")
    payer_id = users.get(payer_name)

    if payer_id is None:
        print("Payer not found in database.")
        return

    # Prompt for custom amounts
    custom_shares = {}
    for name, user_id in users.items():
        custom_amount = input(f"Enter the amount {name} wants to contribute (or press Enter for equal split): ")
        if custom_amount:
            custom_shares[user_id] = float(custom_amount)

    # Save the expense
    expense_id = save_expense(description, total_amount, payer_id)

    # Handle custom shares and remaining balance
    balance = total_amount
    total_paid = 0.0

    # Deduct the custom shares from the balance
    for user_id, amount in custom_shares.items():
        if amount > 0:
            save_payment(expense_id, user_id, amount)
            total_paid += amount
            balance -= amount

    # Handle remaining balance
    while balance > 0:
        print(f"\nRemaining balance: {balance:.2f}")
        top_up_contributors = prompt_top_up(balance, users)
        
        total_contributed = sum(top_up_contributors.values())
        if total_contributed > 0:
            total_paid += total_contributed
            balance -= total_contributed
            for user_id, amount in top_up_contributors.items():
                save_payment(expense_id, user_id, amount)
        
        if balance <= 0:
            print("The balance has been cleared.")
            break
        else:
            print(f"Balance still remaining: {balance:.2f}")

    # Show final payments
    print("\nFinal Payment Summary:")
    with connect_db() as conn:
        cursor = conn.cursor()
        for name, user_id in users.items():
            cursor.execute('''
                SELECT SUM(amount) FROM payments
                WHERE user_id = ?
                AND expense_id = ?
            ''', (user_id, expense_id))
            amount_paid = cursor.fetchone()[0] or 0
            print(f"{name} contributed a total of {amount_paid:.2f}")

    print(f"\nTotal amount paid by all users: {total_paid:.2f}")

if __name__ == "__main__":
    main()
