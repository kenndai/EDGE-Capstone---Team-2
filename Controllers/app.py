import uvicorn
from fastapi import FastAPI
from Accounts.Models.account import Account
from Accounts.Services.account_service import AccountService
from Accounts.Repositories.account_repository import AccountRepository
from Accounts.Repositories.customer_repository import customer_repository
from Accounts.Repositories.address_repository import AddressRepository
from typing import List

app = FastAPI()
address_repository = AddressRepository()
customer_repository = customer_repository()
account_repository = AccountRepository()
account_service = AccountService(account_repository, customer_repository, address_repository)

@app.post('/api/accounts')
async def open_account(account: Account) -> Account:
    if account.current_balance < 25.0:
        raise ValueError('$25.00 minimum required on account opening')
    return account_service.open_account(account)

@app.get('/api/accounts', response_model=List[Account])
async def retrieve_accounts() -> List[Account]:
    return account_service.get_all_accounts()

@app.get('/api/accounts/{account_number}')
async def retrieve_account(account_number) -> Account:
    return account_service.get_account(account_number)

@app.put('/api/accounts/{account_number}/withdraw/{amount}')
async def withdraw(account_number, amount) -> Account:
    mod = float(amount)
    if mod <= 0:
        raise ValueError('Invalid amount specified on withdrawal')
    account = account_service.get_account(account_number)
    if mod > account.current_balance:
        raise ValueError('Withdrawal not completed because of potential overdraw')
    return account_service.withdraw(account_number, mod)

@app.put('/api/accounts/{account_number}/deposit/{amount}')
async def deposit(account_number, amount) -> Account:
    mod = float(amount)
    if mod <= 0:
        raise ValueError('Invalid amount specified on depost')
    return account_service.deposit(account_number, mod)

@app.delete('/api/accounts/{account_number}')
async def close_account(account_number) -> None:
    account_service.close_account(account_number)

if __name__ == "__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=8080,reload=True) #,timeout_keep_alive=3600,debug=True,workers=10)
