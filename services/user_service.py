# services/user_service.py dosyasını güncelleyelim:
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.models import User, Transaction
from schemas.schemas import UserCreate, TransactionCreate
from auth.authentication import get_password_hash, verify_password
from utils.value_objects2 import Money, AccountNumber

class UserService:
    def __init__(self, db: Session):
        self.db = db
        print("self.db--->",self.db)
   
    def create_user(self, user: UserCreate):
        if user.role=="admin":
            print("11111111111111111111111111111",user)
            user_role_controll = self.db.query(User).filter(User.role == user.role).first()
            print("222222222222222222222222222",user)
            if user_role_controll is None:
                db_user = User(
                    username=user.username,
                    email=user.email,
                    role=user.role,
                    hashed_password=get_password_hash(user.password),
                    account_number=user.account_number,
                    balance_currency="TRY"  # Varsayılan para birimi               
                      )
                print("db_user.username--->",db_user.username)
                self.db.add(db_user)
                self.db.commit()
                self.db.refresh(db_user)
                return db_user
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Admin register yapamazsınız"
                )

        else:           
                db_user = User(
                    username=user.username,
                    email=user.email,
                    role=user.role,
                    hashed_password=get_password_hash(user.password),
                    account_number=user.account_number,
                    balance_currency="TRY"  # Varsayılan para birimi                                       
                     )
                
                print("db_user.username--->",db_user.username)
                self.db.add(db_user)
                self.db.commit()
                self.db.refresh(db_user)
                return db_user

    def authenticate_user(self, username: str, password: str):
        print("authenticate_user--->username,password--->",username,password)
        user = self.db.query(User).filter(User.username == username).first()
        print("authenticate_user--->username,password--->",user.username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        print("authenticate_user--->ok")
        return user

    def deposit(self, user_id: int, transaction: TransactionCreate):
        print(" user_service-->user_id---->", user_id)
        print("user_service-->transaction.__dict__*---->",transaction.__dict__)
        user = self.db.query(User).filter(User.id == user_id).first()
        print("user_service--->user.__dict__--->",user.__dict__)
        if not user:
            return None
        print("--------------11111111111111---------------")
        deposit_money = Money(transaction.amount, transaction.currency)
        print("depoist_money---->",deposit_money)
        if user.balance.currency != deposit_money.currency:
            # Burada para birimi dönüşümü yapılabilir, şimdilik basit tutuyoruz
            return None
        user.balance += deposit_money
        print("user.balance----->",user.balance)
        new_transaction = Transaction(
            user_id=user_id,
            amount=deposit_money.amount,
            currency=deposit_money.currency,
            transaction_type="deposit"
        )
        self.db.add(new_transaction)
        self.db.commit()
        self.db.refresh(user)
        return user

    def withdraw(self, user_id: int, transaction: TransactionCreate):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        withdraw_money = Money(transaction.amount, transaction.currency)
        if user.balance.currency != withdraw_money.currency or user.balance.amount < withdraw_money.amount:
            return None
        user.balance -= withdraw_money
        transaction = Transaction(
            user_id=user_id,
            amount=withdraw_money.amount,
            currency=withdraw_money.currency,
            transaction_type="withdrawal"
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(user)
        return user
