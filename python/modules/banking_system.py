import requests

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
    
    def get_balance(self):
        return self.balance

    def convert_currency(self, amount, currency):
        response = requests.get(f'https://api.exchangeratesapi.io/latest?base=USD&symbols={currency}')
        if response.status_code != 200:
            raise Exception("Error fetching exchange rate")
        rate = response.json()['rates'][currency]
        return amount * rate