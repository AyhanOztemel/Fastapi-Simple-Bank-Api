# routers/user_routes.py dosyasını güncelleyelim:

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dbb.database import get_db
from models.models import User
from schemas.schemas import CustomResponse, UserCreate, UserLogin, UserResponse, TransactionCreate
from auth.authentication import get_current_user, create_access_token
from services.user_service import UserService
from fastapi.responses import JSONResponse
from utils.value_objects2 import Money, AccountNumber
router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    print('@router.post("/register"---> içindesiniz')
    registered_user=UserService(db).create_user(user)
    user_response = UserResponse(
        id=registered_user.id,
        username=registered_user.username,
        email=registered_user.email,
        balance=registered_user.balance,
        account_number=AccountNumber(value=registered_user.account_number),
        role=registered_user.role,
        created_at=registered_user.created_at,
        updated_at=registered_user.updated_at,
        is_active=registered_user.is_active
    )
    return user_response

##DAHA PRATİK VE KISA KOD VE DOĞRU YAZIM / TRY EXCEPT KULLANIMI
##    try:
##        registered_user = await UserService(db).create_user(user)
##        return UserResponse(**registered_user.__dict__)  # Unpack using **dict**
##    except Exception as e:
##        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/login")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = UserService(db).authenticate_user(user_login.username, user_login.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    #return {"access_token": access_token, "token_type": "bearer"}
    #return yerine ilave satırlar
    response =JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    print('******router.get("/me"******')
    #return current_user
    # current_user nesnesini UserResponse modeline dönüştürme
    user_response = UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        balance=current_user.balance,
        account_number=AccountNumber(value=current_user.account_number),
        role=current_user.role,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        is_active=current_user.is_active
    )
    
    return user_response

@router.post("/deposit", response_model=UserResponse)
def deposit(transaction: TransactionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    print(" current_user.id---->", current_user.id)
    print("***transaction.__dict__*---->",transaction.__dict__)
    updated_user = UserService(db).deposit(current_user.id, transaction)
    if not updated_user:
        raise HTTPException(status_code=400, detail="Deposit failed")

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

@router.post("/withdraw", response_model=UserResponse)
def withdraw(transaction: TransactionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    updated_user = UserService(db).withdraw(current_user.id, transaction)
    if not updated_user:
        raise HTTPException(status_code=400, detail="Withdrawal failed")
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
