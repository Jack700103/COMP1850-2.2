"""
This is a python script which will import and run your code from cinema.py to let you test it without adding code
which might break the autograder.

You can run this and use the menu to check your code works:
python test.py

You should not need to change any of this code, and you can see an example of the outputs in example_output.txt
"""


import sqlite3
import sys

# Importing your functions from the cinema.py file
try:
    from cinema import customer_tickets, screening_sales, top_customers_by_spend
except ImportError as e:
    print("Could not import functions from cinema.py.")
    print("Make sure cinema.py is in the same folder and contains the required functions.")
    print("Import error:", e)
    sys.exit(1)

DB_PATH = "tickets.db"

# This is just a function to print out your results nicely.
def print_rows(headers, rows, max_rows=50):
    if rows is None:
        print("Function returned None (did you forget to return a list?)")
        return
    if not rows:
        print("No results.")
        return

    rows_to_show = rows[:max_rows]
    widths = [len(h) for h in headers]

    for row in rows_to_show:
        for i, item in enumerate(row):
            widths[i] = max(widths[i], len(str(item)))

    def fmt_row(vals):
        return " | ".join(str(v).ljust(widths[i]) for i, v in enumerate(vals))

    line = "-+-".join("-" * w for w in widths)
    print(line)
    print(fmt_row(headers))
    print(line)
    for row in rows_to_show:
        print(fmt_row(row))
    print(line)

    if len(rows) > max_rows:
        print(f"(Showing {max_rows} of {len(rows)} rows.)")

# function to validate the inputs
def get_int(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid whole number.")

# This displays and runs the menu
def menu(conn):
    while True:
        print("\n=== Cinema Query Checker ===")
        print("1. Customer tickets (customer_tickets)")
        print("2. Screening sales (screening_sales)")
        print("3. Top customers by spend (top_customers_by_spend)")
        print("0. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            customer_id = get_int("Enter customer_id: ")
            rows = customer_tickets(conn, customer_id)
            print_rows(["Film Title", "Screen", "Price"], rows)

        elif choice == "2":
            rows = screening_sales(conn)
            print_rows(["Screening ID", "Film Title", "Tickets Sold"], rows)

        elif choice == "3":
            limit = get_int("How many customers to show (limit)? ")
            rows = top_customers_by_spend(conn, limit)
            print_rows(["Customer Name", "Total Spent"], rows)

        elif choice == "0":
            break

        else:
            print("Invalid option. Please try again.")


def main():
    try:
        conn = sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        print(f"Could not open database '{DB_PATH}'.")
        print("SQLite error:", e)
        return

    try:
        menu(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()