import unittest
from Accounts.Models.address import Address
from Accounts.Repositories.address_repository import AddressRepository
from Accounts.Models.customer import Customer
from Accounts.Repositories.customer_repository import CustomerRepository


class TestCustomerRepository(unittest.TestCase):
    def setUp(self):
        self.addressRepository = AddressRepository()
        self.customerRepository = CustomerRepository()
        self.inserted_address = self.addressRepository.insert(
            Address(id=0, address="123 Main St", city="Anytown", state="NY", zip_code="12345"))
        self.inserted_customer = self.customerRepository.insert(
            Customer(id=0, first_name="John", last_name="Doe", address=self.inserted_address, email_address="test@test.com"))

    def tearDown(self):
        self.customerRepository.delete(self.inserted_customer.id)
        self.addressRepository.delete(self.inserted_address.id)

    def test_get_by_id(self):
        get_customer = self.customerRepository.get_by_id(
            self.inserted_customer.id)
        self.inserted_customer.address = Address.construct(id=self.inserted_address.id)
        self.assertEqual(get_customer, self.inserted_customer)


if __name__ == "__main__":
    unittest.main()
