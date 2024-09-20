# repositories/user_repository.py
from sqlalchemy.orm import Session
from models.models import User, Transaction

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user_balance(self, user: User, amount: float):
        user.balance += amount
        self.db.commit()
        self.db.refresh(user)
        return user

    def create_transaction(self, transaction: Transaction):
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
