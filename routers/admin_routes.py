# routers/admin_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dbb.database import get_db
from models.models import User
from schemas.schemas import UserResponse, UserUpdate
from auth.authorization import admin_required
from services.admin_service import AdminService
from dbb.database import get_db
from utils.value_objects2 import Money, AccountNumber
#import logging
from typing import List
router = APIRouter()
#logger = logging.getLogger(__name__)
from fastapi import HTTPException


@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    print("Endpoint called")
    print("-----------------999999999999999999999-----------------")
    print("type(current_user)----->", type(current_user))
    all_users = AdminService(db).get_all_users()
    print("tttttttttttttttttttttttttttttttttttttttttttt")
    return [UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            balance=user.balance,
            account_number=AccountNumber(value=user.account_number),
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active
            ) for user in all_users]     

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    return_user=AdminService(db).get_user(user_id)

    user_response = UserResponse(
        id=return_user.id,
        username=return_user.username,
        email=return_user.email,
        balance=return_user.balance,
        account_number=AccountNumber(value=current_user.account_number),
        role=return_user.role,
        created_at=return_user.created_at,
        updated_at=return_user.updated_at,
        is_active=return_user.is_active
    )
    return user_response
    
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    updated_user=AdminService(db).update_user(user_id, user_update)
    user_response = UserResponse(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        balance=updated_user.balance,
        account_number=AccountNumber(value=updated_user.account_number),
        role=updated_user.role,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at,
        is_active=updated_user.is_active
    )
    return user_response 


@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    deleted_user=AdminService(db).delete_user(user_id)
    user_response = UserResponse(
        id=deleted_user.id,
        username=deleted_user.username,
        email=deleted_user.email,
        balance=deleted_user.balance,
        account_number=AccountNumber(value=deleted_user.account_number),
        role=deleted_user.role,
        created_at=deleted_user.created_at,
        updated_at=deleted_user.updated_at,
        is_active=deleted_user.is_active
    )
    return user_response 
