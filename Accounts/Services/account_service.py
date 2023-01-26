from Accounts.Models.account import Account
from Accounts.Repositories.account_repository import AccountRepository
from Accounts.Repositories.address_repository import AddressRepository
from Accounts.Repositories.customer_repository import customer_repository

class AccountService():
    def __init__(self, account_repository: AccountRepository, 
            customer_repository: customer_repository, 
            address_repository: AddressRepository) -> None:
        self.account_repository = account_repository
        self.customer_repository = customer_repository
        self.address_repository = address_repository

    def open_account(self, account: Account) -> Account:
        address = self.address_repository.insert(account.customer.address)
        account.customer.address = address
        customer = self.customer_repository.insert(account.customer)
        account.customer = customer
        return self.account_repository.insert(account)

    def get_all_accounts(self) -> 'list[Account]':
        accounts = self.account_repository.get_all()
        for account in accounts:
            account.customer = self.customer_repository.get_by_id(account.customer.id)
            account.customer.address = self.address_repository.get_by_id(account.customer.address_id)
        return accounts

    def get_account(self, account_num: str) -> Account:
        account = self.account_repository.get_account_by_number(account_num)
        account.customer = self.customer_repository.get_by_id(account.customer.id)
        account.customer.address = self.address_repository.get_by_id(account.customer.address_id)
        return account

    def withdraw(self, account_num: str, amount: float) -> Account:
        account = self.account_repository.get_account_by_number(account_num)
        account.current_balance -= amount
        self.account_repository.update(account)
        return self.get_account(account_num)

    def deposit(self, account_number: str, amount: float) -> Account:
        account = self.account_repository.get_account_by_number(account_number)
        account.current_balance += amount
        self.account_repository.update(account)
        return self.get_account(account_number)

    def close_account(self, account_num: str) -> None:
        account = self.get_account(account_num)
        self.account_repository.delete(account.account_id)
        self.address_repository.delete(account.customer.address.address_id)
        self.customer_repository.delete(account.customer.customer_id)