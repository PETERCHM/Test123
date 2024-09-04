# add_users.py
import sqlite3

def add_users():
    with sqlite3.connect('expenses.db') as conn:
        cursor = conn.cursor()
        
        # List of users to add
        users = ['Alice', 'Bob', 'Charlie']
        
        for user in users:
            cursor.execute('''
                INSERT OR IGNORE INTO users (name)
                VALUES (?)
            ''', (user,))
        
        conn.commit()
        print("Users added successfully.")

if __name__ == "__main__":
    add_users()
