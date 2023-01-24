from dbconnect import cursor
from Accounts.Models.address import Address

class AddressRepository():
    def insert(self, address: Address) -> Address:
        cursor.execute("""
            INSERT INTO address
                (Street, City, State, ZipCode) VALUES
                (%(street)s, %(city)s, %(state)s, %(zip_code)s)
                RETURNING id
            """, {
            'street': address.street,
            'city': address.city,
            'state': address.state,
            'zip_code': address.zip_code
        })
        address.address_id = cursor.fetchone()[0]
        return address