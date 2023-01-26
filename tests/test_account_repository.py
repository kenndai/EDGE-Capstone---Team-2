import unittest
from accounts.models.address import Address
from accounts.repositories.address import AddressRepository
from accounts.models.customer import Customer
from accounts.repositories.customer import CustomerRepository
from accounts.models.account import Account
from accounts.repositories.account import AccountRepository


class TestAccountRepository(unittest.TestCase):
    def setUp(self):
        self.addressRepository = AddressRepository()
        self.customerRepository = CustomerRepository()
        self.accountRepository = AccountRepository()
        self.inserted_address = self.addressRepository.insert(
            Address(id=0, address="123 Main St", city="Anytown", state="NY", zip_code="12345"))
        self.inserted_customer = self.customerRepository.insert(
            Customer(id=0, first_name="John", last_name="Doe", address=self.inserted_address, email_address="test@test.com"))
        self.inserted_account = self.accountRepository.insert(
            Account(id=0, account_number="123456789", customer=self.inserted_customer, current_balance=100.00))

    def tearDown(self):
        self.accountRepository.delete(self.inserted_account.id)
        self.customerRepository.delete(self.inserted_customer.id)
        self.addressRepository.delete(self.inserted_address.id)

    def test_get_by_account_number(self):
        get_account = self.accountRepository.get_by_account_number(
            self.inserted_account.account_number)
        self.inserted_account.customer = Customer.construct(
            id=self.inserted_customer.id)
        self.assertEqual(get_account, self.inserted_account)

    def test_get_all(self):
        try:
            inserted_address2 = self.addressRepository.insert(
                Address(id=0, address="123 Main St", city="Anytown", state="NY", zip_code="12345"))
            inserted_customer2 = self.customerRepository.insert(
                Customer(id=0, first_name="John", last_name="Doe", address=inserted_address2, email_address="test@test.com"))
            inserted_account2 = self.accountRepository.insert(Account(id=0, account_number="987654321",
                                                                      customer=inserted_customer2, current_balance=100.00))
            accounts = self.accountRepository.get_all()
            self.assertGreaterEqual(len(accounts), 2)
            self.inserted_account.customer = Customer.construct(
                id=self.inserted_customer.id)
            inserted_account2.customer = Customer.construct(
                id=inserted_customer2.id)
            self.assertTrue(self.inserted_account in accounts)
            self.assertTrue(inserted_account2 in accounts)
        finally:
            self.accountRepository.delete(inserted_account2.id)
            self.customerRepository.delete(inserted_customer2.id)
            self.addressRepository.delete(inserted_address2.id)

    def test_update(self):
        current = self.accountRepository.get_by_account_number(
            self.inserted_account.account_number)
        current.current_balance = 200.00
        self.accountRepository.update(current)
        updated = self.accountRepository.get_by_account_number(
            self.inserted_account.account_number)
        self.assertEqual(updated.id, self.inserted_account.id)
        self.assertEqual(updated.account_number,
                         self.inserted_account.account_number)
        self.assertEqual(updated.customer.id,
                         self.inserted_account.customer.id)
        self.assertEqual(updated.current_balance, 200.00)


if __name__ == "__main__":
    unittest.main()
