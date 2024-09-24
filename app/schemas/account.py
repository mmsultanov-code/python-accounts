from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AccountBalanceRequest(BaseModel):
    account_id: int
    datetime: datetime

class IncomingFundCreate(BaseModel):
    account_id: int
    amount: float
    settlement_date: datetime

class AccountCreate(BaseModel):
    user_id: int

class AccountCreateResponse(BaseModel):
    account_id: int
    balance: float
    user_id: int

class AccountBalanceResponse(BaseModel):
    account_id: int
    balance: float

class IncomingFundCreateResponse(BaseModel):
    fund_id: int
    account_id: int
    amount: float
    settlement_date: datetime

class SettlementResponse(BaseModel):
    message: str