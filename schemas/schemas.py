# schemas/schemas.py dosyasını güncelleyelim:

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from utils.value_objects2 import Money, AccountNumber


class CustomResponse(BaseModel):
    message: str

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    account_number: str
    role: str #= "user"  # Varsayılan değer olarak "user"
   
class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None  # Opsiyonel rol alanı

class UserResponse(UserBase):
    id: int
    balance: Money
    account_number: AccountNumber
    role: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    amount: float
    currency: str

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    money: Money
    transaction_type: str
    created_at:datetime

    class Config:
        orm_mode = True
