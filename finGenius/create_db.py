import sqlite3
from datetime import date
import os
import traceback

DB_FILE = "expenses.db"

def create_table():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    amount REAL NOT NULL
                )
            """)
            conn.commit()
    except Exception as e:
        print("Error creating table:", e)
        traceback.print_exc()

def show_table_schema():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            cur.execute("PRAGMA table_info(expenses)")
            cols = cur.fetchall()
            if not cols:
                print("Table 'expenses' does not exist or has no columns.")
            else:
                print("\nexpenses table schema:")
                print("cid | name | type | notnull | dflt_value | pk")
                for c in cols:
                    print(c)
    except Exception as e:
        print("Error reading schema:", e)
        traceback.print_exc()

def add_expense(date_str, category, description, amount):
    # validate amount
    try:
        amount = float(amount)
    except ValueError:
        raise ValueError("Amount must be a number (e.g., 250 or 250.50).")

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            # explicitly specify columns to avoid schema/order mismatch
            cur.execute(
                "INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
                (date_str, category, description, amount)
            )
            conn.commit()
            print("✅ Expense added.")
    except sqlite3.OperationalError as e:
        print("SQLite OperationalError:", e)
        print("Tip: run option 3 (Show schema) from the menu to inspect the table. If schema is wrong, use option 4 to reset DB.")
        traceback.print_exc()
    except Exception as e:
        print("Error adding expense:", e)
        traceback.print_exc()

def view_expenses():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM expenses")
            rows = cur.fetchall()
            if not rows:
                print("\nNo expenses found. Add one (menu option 1).")
                return
            print("\nID | Date       | Category    | Description           | Amount")
            print("-" * 70)
            for r in rows:
                print(r)
    except Exception as e:
        print("Error reading expenses:", e)
        traceback.print_exc()

def add_expense_interactive():
    print("\nAdd new expense (leave date empty for today):")
    d = input("Date (YYYY-MM-DD): ").strip()
    if not d:
        d = date.today().isoformat()
    cat = input("Category: ").strip() or "Other"
    desc = input("Description: ").strip()
    amt = input("Amount: ").strip()
    try:
        add_expense(d, cat, desc, amt)
    except Exception as e:
        print("Failed to add expense:", e)

def main_menu():
    create_table()
    while True:
        print("\n--- Expense Tracker Menu ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show DB Table Schema (debug)")
        print("4. Reset DB (delete expenses.db) — irreversible")
        print("5. Exit")
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            add_expense_interactive()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_table_schema()
        elif choice == "4":
            confirm = input("Type YES (uppercase) to delete the DB file: ")
            if confirm == "YES":
                try:
                    if os.path.exists(DB_FILE):
                        os.remove(DB_FILE)
                        print("DB file deleted. Table will be recreated on next action.")
                    else:
                        print("No DB file found to delete.")
                except Exception as e:
                    print("Failed to delete DB:", e)
            else:
                print("Canceled.")
        elif choice == "5":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()


