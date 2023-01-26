import unittest
from unittest.mock import Mock
from Accounts.Models.address import Address
from Accounts.Repositories.address_repository import AddressRepository
from Accounts.Models.customer import Customer
from Accounts.Repositories.customer_repository import CustomerRepository
from Accounts.Models.account import Account
from Accounts.Repositories.account_repository import AccountRepository
from Accounts.Services.account_service import AccountService


class TestAccountService(unittest.TestCase):
    def setUp(self):
        self.address = Address(id=1, address="123 Main St",
                               city="Anytown", state="NY", zip_code="12345")
        self.customer = Customer(id=1, first_name="John",
                                 last_name="Doe", address=self.address, email_address="test@test.com")
        self.account = Account(id=1, account_number="000",
                               customer=self.customer, current_balance=100.0)
        self.address_repository = Mock()
        self.customer_repository = Mock()
        self.account_repository = Mock()
        self.account_service = AccountService(
            self.account_repository, self.customer_repository, self.address_repository)

    def test_open_account(self):
        self.address_repository.insert = Mock(return_value=self.address)
        self.customer_repository.insert = Mock(return_value=self.customer)
        self.account_repository.insert = Mock(return_value=self.account)
        new_account = self.account_service.open_account(self.account)
        self.assertEqual(new_account, self.account)

    def test_get_all_accounts(self):
        self.account_repository.get_all = Mock(return_value=[self.account])
        self.customer_repository.get_by_id = Mock(return_value=self.customer)
        self.address_repository.get_by_id = Mock(return_value=self.address)
        accounts = self.account_service.get_all_accounts()
        self.assertEqual(accounts, [self.account])

    def test_get_account(self):
        self.account_repository.get_by_account_number = Mock(
            return_value=self.account)
        self.customer_repository.get_by_id = Mock(return_value=self.customer)
        self.address_repository.get_by_id = Mock(return_value=self.address)
        account = self.account_service.get_account("000")
        self.assertEqual(account, self.account)

    def test_withdraw(self):
        self.account_repository.get_by_account_number = Mock(
            return_value=self.account)
        self.account_repository.update = Mock(return_value=None)
        account = self.account_service.withdraw("000", 10.0)
        self.assertEqual(account.current_balance, 90.0)

    def test_deposit(self):
        self.account_repository.get_by_account_number = Mock(
            return_value=self.account)
        self.account_repository.update = Mock(return_value=None)
        account = self.account_service.deposit("000", 10.0)
        self.assertEqual(account.current_balance, 110.0)

    def test_close_account(self):
        self.account_repository.get_by_account_number = Mock(
            return_value=self.account)
        self.account_repository.delete = Mock(return_value=None)
        self.customer_repository.delete = Mock(return_value=None)
        self.address_repository.delete = Mock(return_value=None)
        self.account_service.close_account("000")
        self.account_repository.delete.assert_called_with(1)
        self.customer_repository.delete.assert_called_with(
            self.account.customer.id)
        self.address_repository.delete.assert_called_with(
            self.account.customer.address.id)


if __name__ == "__main__":
    unittest.main()
