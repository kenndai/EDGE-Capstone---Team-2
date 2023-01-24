from pydantic import BaseModel
from Accounts.Models.address import Address
from Accounts.Models.customer import Customer

class Account(BaseModel):
    id: int
    account_num: str
    customer_id: Customer.id
    current_balance: float