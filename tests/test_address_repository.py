
import unittest
from Accounts.Models.address import Address
from Accounts.Repositories.address_repository import AddressRepository


class TestAddressRepository(unittest.TestCase):
    def setUp(self):
        self.addressRepository = AddressRepository()
        self.inserted_address = self.addressRepository.insert(
            Address(id=0, address="123 Main St", city="Anytown", state="NY", zip_code="12345"))

    def tearDown(self):
        self.addressRepository.delete(self.inserted_address.id)

    def test_get_by_id(self):
        get_address = self.addressRepository.get_by_id(
            self.inserted_address.id)
        self.assertEqual(get_address, self.inserted_address)


if __name__ == "__main__":
    unittest.main()
