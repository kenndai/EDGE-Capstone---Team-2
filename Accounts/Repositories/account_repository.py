from unittest import result
from dbconnect import cursor
import psycopg2
from Accounts.Models.account import Account
from Accounts.Models.customer import Customer


class AccountRepository():

    host = "localhost"
    database = "accounts"
    user = ""
    password = ""

    def insert(self, account: Account) -> Account:
        with psycopg2.connect() as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO account
                        (AccountNumber, CustomerID, CurrentBalance) VALUES
                        (%(account_num)s, %(customer_id)s, %(current_balance)s)
                        RETURNING id
                    """, {
                    'account_num': account.account_num,
                    'customer_id': account.customer.id,
                    'current_balance': account.current_balance,
                })
                account.account_id = cursor.fetchone()[0]
        return account

    def get_account_by_number(self, account: Account) -> Account:
        with psycopg2.connect() as db:
            with db.cursor() as cursor:
                cursor.execute("SELECT * FROM account WHERE AccountNumber = %(account_num)s", {
                    'acccount_num': account.account_num
                })
                row = cursor.fetchone()
        return Account.construct(account_id=row[0], account_num=row[1], customer=Customer.construct(customer_id=row[2]), current_balance=round(row[3], 2))

    def get_all(self) -> 'list[Account]':
        result_accounts = []
        with psycopg2.connect() as db:
            with db.cursor() as cursor:
                cursor.execute("SELECT * FROM account")
                all_accounts = cursor.fetchall()

        for acc in all_accounts:
            result_accounts.append(Account.construct(account_id=acc[0], account_num=acc[1], customer=Customer.construct(customer_id=acc[2]), current_balance=round(acc[3], 2)))

        return result_accounts

    def update(self, account: Account) -> None:
        with psycopg2.connect() as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    UPDATE account
                    SET AccountNumber=%(account_num)s, CustomerID=%(custoemr_id)s, CurrentBalance=%(current_balance)s
                    WHERE ID=%(id)s
                    """, {
                        "account_id": account.account_id,
                        "account_num": account.account_num,
                        "customer_id": account.customer.id,
                        "current_balance": account.current_balance
                    })

    def delete(self, account_id) -> None:
        with psycopg2.connect() as db:
            with db.cursor() as cursor:
                cursor.execute("DELETE FROM account WHERE ID=%(account_id)s", {
                    'account_id': account_id
                })


