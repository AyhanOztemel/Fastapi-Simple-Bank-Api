# services/admin_service.py
from sqlalchemy.orm import Session
from models.models import User
from schemas.schemas import UserUpdate
from fastapi import APIRouter, Depends, HTTPException
from auth.authentication import get_current_user
class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self,current_user: User = Depends(get_current_user)):
        return self.db.query(User).all()
       
    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user(self, user_id: int, user_update: UserUpdate):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        for var, value in vars(user_update).items():
            setattr(user, var, value) if value else None
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        #self.db.delete(user)
        user.is_active= False
        self.db.commit()
        return user
