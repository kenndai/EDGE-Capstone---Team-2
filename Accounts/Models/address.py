from pydantic import BaseModel

class Address(BaseModel):
    address_id: int
    address: str
    city: str
    state: str
    zip_code: str