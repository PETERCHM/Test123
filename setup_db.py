# setup_db.py
import sqlite3

def create_tables():
    with sqlite3.connect('expenses.db') as conn:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')

        # Create expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                total_amount REAL NOT NULL,
                payer_id INTEGER,
                FOREIGN KEY (payer_id) REFERENCES users(id)
            )
        ''')

        # Create payments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_id INTEGER,
                user_id INTEGER,
                amount REAL NOT NULL,
                FOREIGN KEY (expense_id) REFERENCES expenses(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        conn.commit()

if __name__ == "__main__":
    create_tables()
