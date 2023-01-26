import psycopg2
from Accounts.Models.address import Address

class AddressRepository():

    host = "localhost"
    database = "postgres"
    user = "postgres"
    password = "test"

    def insert(self, address: Address) -> Address:
        with psycopg2.connect(host=self.host, database=self.database, user=self.user,
                                password=self.password) as db:
            with db.cursor() as cursor:
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
        with psycopg2.connect(host=self.host, database=self.database, user=self.user,
                                password=self.password) as db:
            with db.cursor() as cursor:    
                cursor.execute("""
                    SELECT ID, Street, City, State, ZipCode FROM
                        address WHERE ID=%(address_id)s
                    """, {
                    'address_id': address_id
                    }
                    )
                row = cursor.fetchone()
        return Address.construct(address_id=row[0], street=row[1], city=row[2], state=row[3], zip_code=row[4])


    def delete(self, address_id) -> None:
        with psycopg2.connect(host=self.host, database=self.database, user=self.user,
                                password=self.password) as db:
            with db.cursor() as cursor: 
                cursor.execute("""
                    DELETE FROM address WHERE ID=%(address_id)s
                    """, {
                        'address_id': address_id
                    }
                    )    