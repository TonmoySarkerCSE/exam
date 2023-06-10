class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class user_account(User):
    def __init__(self, name, email, address, initial_deposit):
        super().__init__(name, email)
        self.address = address
        self.__balance = initial_deposit
        self.__loan = 0
        self.__transaction_history = []

    @property
    def balance(self):
        return self.__balance

    @property
    def loan(self):
        return self.__loan

    def check_balance(self):
        print("\n____________________________________")
        print(f'Hello {self.name}')
        print(f"Balance : {self.__balance}")
        print("____________________________________\n")

    def deposit(self, amount):
        self.__balance += amount
        self.transaction_history("Deposit", amount)

    def withdraw(self, amount):
        if self.__balance >= amount:
            self.__balance -= amount
            self.transaction_history("Withdraw", amount)

            print("____________________________________")
            print("Withdraw Successfull")
            print("____________________________________")


        else:
            print("Not Enough Balance")

    def transfer(self, amount, receiver):
        if self.__balance >= amount:
            self.__balance -= amount
            self.transaction_history("Transfered", amount)
            receiver.__balance += amount
            receiver.transaction_history("Recrived", amount)
            print("\n____________________________________")
            print("Balance Transferred Successfully")
            print("____________________________________\n")
        else:
            print("\n____________________________________")
            print("Not Enough Balance")
            print("____________________________________\n")

    def Take_loan(self, amount, bank):
        if bank.loan_status():
            if self.__loan == 0 and amount <= 2 * self.__balance:
                self.__loan = amount
                self.__balance += amount
                self.transaction_history("Loan : ", amount)
                print("\n____________________________________")
                print("Your Loan Request is Approved ")
                print("____________________________________\n")
            else:
                print("\n____________________________________")
                print(f"You Can't Loan More Than : {2*self.__balance}")
                print("____________________________________\n")
        else:
            print("\n____________________________________")
            print(f"Dear {self.name}")
            print("Currently Loan Requests are not Accepted .")
            print("____________________________________\n")

    def transaction_history(self, transection_type, amount):
        transaction = {
            "type": transection_type,
            "amount": amount
        }
        self.__transaction_history.append(transaction)

    def show_transaction_history(self):
        print("\n____________________________________")
        print(f"Hello {self.name},\nYour Transaction History :\n")
        for transaction in self.__transaction_history:
            print(f"Type: {transaction['type']}\n Amount: {transaction['amount']}")
        print("____________________________________\n")

    def __repr__(self):
        user_details = f"Name : {self.name}\n"
        user_details += (f"Balance: {self.__balance}____________________________________\n")
        return user_details

class admin_account(User):
    def __init__(self, name, email, password):
        super().__init__(name, email)
        self.password = password

    def Create_Account(self, account, bank):
        bank.Create_Account(account)

    def Total_Balance(self, bank):
        return bank.Total_Balance()

    def Total_Loan(self, bank):
        return bank.Total_Loan()

    def Loan_Service(self, bank, password):
        bank.Loan_Service(password)

class Bank:
    starting_account_no = 100000
    loan_open = False

    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.admins = {}
        self.total_balance = 0
        self.total_loan = 0

    def Create_Account(self, account):
        account_no = self.assign_account_no()
        self.accounts[account_no] = account

    def assign_account_no(self):
        self.starting_account_no += 1
        return self.starting_account_no

    def Total_balance_sum(self):
        self.total_balance = sum(acc.balance for acc in self.accounts.values())

    def Total_loan_sum(self):
        self.total_loan = sum(acc.loan for acc in self.accounts.values())

    def Total_Balance(self):
        self.Total_balance_sum()
        return self.total_balance

    def Total_Loan(self):
        self.Total_loan_sum()
        return self.total_loan

    def available_balance(self):
        return self.total_balance - self.total_loan

    def Loan_Service(self, password):
        admin = self.admins.get(password)
        print("\n____________________________________")
        if admin:
            self.loan_open = not self.loan_open
            print(
                "Loan Service Enabled."
                if self.loan_open
                else "Loan Service Disabled."
            )
        else:
            print("Wrong Admin Password.")
        print("____________________________________\n")

    def loan_status(self):
        return self.loan_open

    def __repr__(self):
        acc_details = f"Bank : {self.name}\n"
        acc_details += "____________________________________\n"
        for acc_no, acc in self.accounts.items():
            acc_details += f"Account No : {acc_no}\n"
            acc_details += f"Account Details :\n{acc}\n"
        return acc_details




# main function
BankAsia = Bank("Bank Asia")

Tonmoy_sarker = user_account("Tonmoy Sarker", "tonmoycreation1@gmail.com", "Bogura", 1000)
Shanto_sarker = user_account("Shanto Sarker", "shantosarker4793@gmail.com", "Bogura", 1000)

BankAsia.Create_Account(Tonmoy_sarker)
BankAsia.Create_Account(Shanto_sarker)

print("\n =============== Deposit Check =============== ")
Tonmoy_sarker.check_balance()
Tonmoy_sarker.deposit(25000)
Tonmoy_sarker.check_balance()

print("\n =============== Withdrow Check =============== ")
Tonmoy_sarker.check_balance()
Tonmoy_sarker.withdraw(6000)
Tonmoy_sarker.check_balance()

print("\n =============== Transfer Check =============== ")
Shanto_sarker.check_balance()
Tonmoy_sarker.check_balance()
Tonmoy_sarker.transfer(5000, Shanto_sarker)
Shanto_sarker.check_balance()
Tonmoy_sarker.check_balance()

print("\n =============== Transaction History Check =============== ")
Tonmoy_sarker.show_transaction_history()
Shanto_sarker.show_transaction_history()

print("\n =============== Loan Check =============== ")
Tonmoy_sarker.Take_loan(5500,BankAsia)
Tonmoy_sarker.check_balance()

password = "password"
adminstrator = admin_account("Admin BankAsia", "admin@bankasia.com", password )
BankAsia.admins[password] = adminstrator

#loan on
BankAsia.Loan_Service(password)

print("\n =============== Loan Check =============== ")
Tonmoy_sarker.check_balance()
Tonmoy_sarker.Take_loan(5500,BankAsia)
Tonmoy_sarker.check_balance()
# loan off
BankAsia.Loan_Service(password)

print("\n ============= Available Balance Of The Bank ============= ")
print("____________________________________\n")
print("Available Balance Of Bank : ", end=" ")
print(adminstrator.Total_Balance(BankAsia))
print("____________________________________\n")

print("\n ============= Total Loan Amount Of Bank ============= ")
print("____________________________________\n")
print("Total Loan Of Bank : ", end=" ")
print(adminstrator.Total_Loan(BankAsia))
print("____________________________________\n")
