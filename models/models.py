# models/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Numeric,Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime
from utils.value_objects2 import Money, AccountNumber

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(128))  # Uzunluğu 128'e çıkardık
    balance_amount = Column(Numeric(10, 2), default=0.0)
    balance_currency = Column(String, default="TRY")
    role = Column(String, default="user")
    account_number = Column(String, unique=True , nullable=True)

    transactions = relationship("Transaction", back_populates="user")

    @property
    def balance(self):
        return Money(self.balance_amount, self.balance_currency)

    @balance.setter
    def balance(self, value: Money):
        self.balance_amount = value.amount
        self.balance_currency = value.currency

    @property
    def account(self):
        return AccountNumber(self.account_number)

class Transaction(BaseModel):
    __tablename__ = "transactions"

    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    currency=Column(String)
    transaction_type = Column(String)  # "deposit" veya "withdrawal"

    user = relationship("User", back_populates="transactions")


