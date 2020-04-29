import csv
import json
from models import Transaction, Statement
import datetime

csv_file = 'export.csv'
data = {}

# # Method without Serialization (only with .__dict__)
# data["Transactions"] = []
transactions = []

def getFloat(str_num):
    try:
        list_ = str_num.split('.')
        amount = ""
        for i in list_:
            amount = amount + i
        amount = amount.split(',')
        amount = float(amount[0] + '.' + amount[1])
        return amount
    except: 
        return 0.0

# # Import the CSVfile with our data 
with open(csv_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if line_count == 0: 
            print("")
        else:
            if len(row) > 0:
                # Configure data to right format we want
                date_ = row[0]
                splited = row[1].split(' ')
                account_num = splited[len(splited) -1]
                name = splited[0]
                transaction_amount = getFloat(row[2])
                ending_balance = getFloat(row[3])
                # Create transactions using class constructor
                transaction = Transaction(
                    name,
                    transaction_amount,
                    date_,
                    account_num,
                    ending_balance
                )
                # Check if operation is new: yes --> add to transactions list
                exists = False
                for operation in transactions:
                    if operation.date == transaction.date:
                        if operation.name == transaction.name:
                            if operation.amount == transaction.amount:
                                exists = True
                if exists != True:
                    # data["Transactions"].append(transaction.__dict__)
                    transactions.append(transaction)
        line_count += 1

# Write to JSONfile 
statements = []

with open('transaction.json', 'w') as json_file:
    data = {}
    data["Transactions"] = []
    for operation in transactions:
        date_ = datetime.datetime.strptime(operation.date, "%d/%m/%Y").date().strftime("%Y%m")
        statement = Statement(date_, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        data["Transactions"].append(operation.serialize())
        exists = False
        for state in statements:
            if state.date == statement.date: # statement with the same date already added in the list (one statement per month)
                exists = True
                if state.date == date_:
                    statement = state
        statement.create_statement(operation)
        statement.set_ending_balance_month()
        statement.set_tax_and_profit()
        if exists != True:
            statements.append(statement)
    json.dump(data, json_file, sort_keys=True, indent=4) 

with open('statement.json', 'w') as json_file:
    data = {}
    data["Statements"] = []
    for state in statements:
        data["Statements"].append(state.serialize())
    json.dump(data, json_file, sort_keys=True, indent=4)

total_income = 0.0
total_expenses = 0.0
total_balance = 0.0
total_taxes = 0.0
total_net_profit = 0.0

for statement in statements: 
    total_income = total_income + statement.income
    total_expenses = total_expenses + statement.expenses
    total_balance = total_balance + statement.ending_balance_month
    total_taxes = total_taxes + statement.tax_to_pay
    total_net_profit = total_net_profit + statement.net_profit

print("---------------------------")
print(f"     Year {statement.date[:4]} Summary")
print("---------------------------")
print(f"Total income:       {total_income}")
print(f"Total expenses:    {total_expenses}")
print(f"Total balance:      {total_balance}")
print(f"Total taxes:       -{total_taxes}")
print("___________________________")
print(f"Total net profit:   {total_net_profit}")
print("")

for statement in statements:
    print(f"--Month summary {statement.date[-2:]}-{statement.date[:4]}--")
    print("-------------------------")
    print(f"Income:         {statement.income}€")
    print(f"Expenses:      {statement.expenses}€")
    print(f"Balance:        {statement.ending_balance_month}€")
    print(f"Tax to pay:    -{statement.tax_to_pay}€")
    print("_________________________")
    print(f"Net Profit:     {statement.net_profit}€")
    print() 
