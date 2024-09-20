# auth/authentication.py
from fastapi import Depends, HTTPException, status,Request,Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from dbb.database import get_db
from models.models import User
import hashlib
import os

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

##def verify_password(plain_password, hashed_password):
##    salt = hashed_password[:32]  # İlk 32 karakter salt olarak kullanılır
##    return hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000).hex() == hashed_password[32:]
##def verify_password(plain_password, hashed_password):
##    # `hashed_password` bir `str` değilse `bytes`'a dönüştürülmelidir
##    if isinstance(hashed_password, str):
##        hashed_password = bytes.fromhex(hashed_password)
##    
##    # `salt`'ı `bytes`'a dönüştürün
##    salt = hashed_password[:32]  # İlk 32 byte'ı salt olarak kullanır
##    # `pbkdf2_hmac` işlemini yap
##    return hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000).hex() == hashed_password.hex()
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Hash'lenmiş şifreden salt ve key'i ayır
    salt = bytes.fromhex(hashed_password[:64])  # İlk 64 karakter salt'tır (32 byte * 2)
    stored_key = bytes.fromhex(hashed_password[64:])  # Geri kalan karakterler key'tir

    # Plain password'ı hash'le ve saklanan key ile karşılaştır
    key = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
    return key == stored_key

def get_password_hash(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + key.hex()

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

"""
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user"""
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    print("111111111111111111111111111111111111111111111")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("222222222222222222222222222222222222222222222222")
    # Çerezden token'ı al
    access_token = request.cookies.get("access_token")
    print("3333----------------->access_token------>",access_token)

    if not access_token:
        print("----------------------access_token:ERROR------------------------")
        raise credentials_exception
    
    try:
        print("4444444444444444444444444444444444444444444444444")
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        print("5555555555555555555555555555555555555555555555555555")
        username: str = payload.get("sub")
        print("************-----username----->",username)
        if username is None:
            raise credentials_exception

    except JWTError:
        print("----------------------JWTError:ERROR------------------------")
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    print("user------------>",user.username)
    if user is None:
        raise credentials_exception
    
    return user
