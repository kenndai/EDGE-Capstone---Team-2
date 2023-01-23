from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    street: str
    zip_code: str