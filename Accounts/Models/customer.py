from pydantic import BaseModel
from Accounts.Models.address import Address

class Customer(BaseModel):
    id: int
    first_name: str
    last_name: str
    email_address: str
    address_id: Address.id