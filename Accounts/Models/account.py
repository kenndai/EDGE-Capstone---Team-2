from pydantic import BaseModel
from Accounts.Models.address import Address
from Accounts.Models.customer import Customer

class Account(BaseModel):
    account_id: int
    account_num: str
    customer: Customer
    current_balance: float