import datetime

class Transaction: 
    def __init__ (self, name, amount, date, account_number, ending_balance): 
        self.name = name
        self.amount = amount
        self.date = date
        self.account_number = account_number
        self.ending_balance = ending_balance
        
    
    def serialize(self):
        return {
            "name" : self.name,
            "amount" : self.amount,
            "date" : str(self.date),
            "account_number" : self.account_number,
            "ending_balance" : self.ending_balance
        }

class Statement:
    def __init__(self, date, income, ending_balance_month, ending_balance_total, tax_to_pay, expenses, net_profit):
        self.date = date
        self.income = income
        self.ending_balance_month = ending_balance_month
        self.ending_balance_total = ending_balance_total
        self.tax_to_pay = tax_to_pay
        self.expenses = expenses
        self.net_profit = net_profit
    
    def serialize(self):
        return {
            "date" : str(self.date),
            "income" : self.income,
            "ending_balance_month" : self.ending_balance_month,
            "ending_balance_total" : self.ending_balance_total,
            "tax_to_pay" : self.tax_to_pay,
            "expenses" : self.expenses,
            "net_profit" : self.net_profit
        }

    def set_ending_balance_month(self):
        self.ending_balance_month = self.income + self.expenses
    
    def set_tax_and_profit(self):
        self.tax_to_pay = (self.ending_balance_month * 0.25) + ((self.ending_balance_month * 0.75) * 0.25)
        self.net_profit = self.ending_balance_month - self.tax_to_pay

    last_date = ""
    def create_statement(self, operation):
        # Convert operation date '19-10-22' to following format datetime.date(2019, 10, 22)
        date_day = datetime.datetime.strptime(operation.date, "%d/%m/%Y").date()
        # Convert then to following format '201910' 
        # Assign it to date_ to group operations by month (refers to operation date-->month)
        date_ = date_day.strftime("%Y%m")
        # Format of self.date (self refers to Statement date-->month) same as date_ 
        if date_ == self.date: 
            if self.last_date == "": # IF no previous statement THEN set date of current operation
                self.last_date = date_day
            if date_day >= self.last_date: # IF current operation date > previous statement date THEN update ending balance
                self.ending_balance_total = operation.ending_balance

        operation_amount = operation.amount        
        if operation_amount > 0.0:
            self.income = self.income + operation.amount
        else:
            self.expenses = self.expenses + operation.amount


