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
        }
        )
        address.address_id = cursor.fetchone()[0]
        return address

    def get_by_id(self, address_id) -> Address:
        cursor.execute("""
            SELECT AddressID, Street, City, State, ZipCode FROM
                address WHERE AddressID=%(address_id)s
            """, {
            'address_id': address_id
            }
            )
        row = cursor.fetchone()
        return Address.construct(address_id=row[0], street=row[1], city=row[2], state=row[3], zip_code=row[4])

    def delete(self, address_id) -> None:
        cursor.execute("""
            DELETE FROM address WHERE AddressID=%(address_id)s
            """, {
                'address_id': address_id
            }
            )    