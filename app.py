from flask import Flask, render_template, request
from expense import Expense
from datetime import datetime
import calendar

app = Flask(__name__)

# File path for storing expenses
expense_file_path = "expenses.csv"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from the form
        budget = float(request.form['budget'])
        name = request.form['name']
        amount = float(request.form['amount'])
        category = request.form['category']

        # Create Expense object
        expense = Expense(name=name, category=category, amount=amount)

        # Save expense to file
        save_expense_to_file(expense, expense_file_path)

        # Summarize Expenses
        expenses, total_spent, remaining_budget, daily_budget = summarize_expenses(expense_file_path, budget)

        # Return to summary page
        return render_template('summary.html', expenses=expenses, total=total_spent, remaining=remaining_budget, daily=daily_budget)

    return render_template('index.html')

def save_expense_to_file(expense, expense_file_path):
    with open(expense_file_path, 'a') as f:  # Append mode
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")

def summarize_expenses(expense_file_path, budget):
    expenses = []
    total_spent = 0
    remaining_budget = 0
    daily_budget = 0

    try:
        with open(expense_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                expense_name, expense_amount, expense_category = line.strip().split(",")
                line_expense = Expense(name=expense_name, amount=float(expense_amount), category=expense_category)
                expenses.append(line_expense)

        total_spent = sum(x.amount for x in expenses)
        remaining_budget = budget - total_spent
        now = datetime.now()
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        remaining_days = days_in_month - now.day

        if remaining_days > 0:
            daily_budget = remaining_budget / remaining_days

    except FileNotFoundError:
        print("No expenses found! File does not exist.")

    return expenses, total_spent, remaining_budget, daily_budget

if __name__ == "__main__":
    app.run(debug=True)
