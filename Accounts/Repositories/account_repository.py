# import psycopg2
from dbconnect import cursor
from Accounts.Models.account import Account

class AccountRepository():
    def insert(self, account: Account) -> Account:
        # with psycopg2.connect() as db:
        #     with db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO account
                (AccountNumber, Customer, CurrentBalance) VALUES
                (%(account_num)s, %(customer_id)s, %(current_balance)s)
                RETURNING id
            """, {
            'account_num': account.account_num,
            'customer_id': account.customer_id,
            'current_balance': account.current_balance,
        })
        account.account_id = cursor.fetchone()[0]
        return account