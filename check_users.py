# check_users.py
import sqlite3

def check_users():
    with sqlite3.connect('expenses.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM users')
        rows = cursor.fetchall()
        if rows:
            print("Users in the database:")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}")
        else:
            print("No users found in the database.")

if __name__ == "__main__":
    check_users()
