from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["expense_tracker"]
expenses_collection = db["expenses"]

def add_expense():
    try:
        title = input("Enter expense title: ")
        amount = float(input("Enter expense amount: "))
        category = input("Enter expense category: ")

        expense = {
            "title": title,
            "amount": amount,
            "category": category,
            "date": datetime.now()
        }
        expenses_collection.insert_one(expense)
        print(" Expense added successfully!")

    except ValueError:
        print("Please enter a valid amount.")

def view_expenses():
    expenses = expenses_collection.find()

    print("\n All Expenses:")
    for exp in expenses:
        print(
            f"ID: {exp['_id']} | "
            f"{exp['title']} | "
            f"₹{exp['amount']} | "
            f"{exp['category']} | "
            f"{exp['date'].strftime('%d-%m-%Y')}"
        )

def total_expenses():
    total = 0
    for exp in expenses_collection.find():
        total += exp["amount"]

    print(f"\n Total expenses: ₹{total}")

def category_expenses():
    cat = input("Enter category: ")

    expenses = expenses_collection.find({"category": cat})

    print(f"\n Expenses in '{cat}' category:")
    found = False
    for exp in expenses:
        found = True
        print(
            f"ID: {exp['_id']} | "
            f"{exp['title']} | "
            f"₹{exp['amount']} | "
            f"{exp['date'].strftime('%d-%m-%Y')}"
        )

    if not found:
        print("No expenses found in this category.")

def delete_expense():
    expense_id = input("Enter Expense ID to delete: ")

    try:
        result = expenses_collection.delete_one(
            {"_id": ObjectId(expense_id)}
        )

        if result.deleted_count > 0:
            print("Expense deleted successfully!")
        else:
            print("No expense found with that ID.")

    except:
        print("Invalid ID format.")

def main():
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expenses")
        print("4. Expenses by Category")
        print("5. Delete Expense")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            total_expenses()
        elif choice == '4':
            category_expenses()
        elif choice == '5':
            delete_expense()
        elif choice == '6':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

# Run the program
main()
