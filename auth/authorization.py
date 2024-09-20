# auth/authorization.py
from fastapi import HTTPException, Depends
from models.models import User
from auth.authentication import get_current_user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    print("current_user.is_active----->",current_user.is_active)
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def admin_required(current_user: User = Depends(get_current_active_user)):
    print("current_user.role----->",current_user.is_active)
    print('current_user.role---->',current_user.role)
    print('current_user.role != "admin"---->',current_user.role != "admin")
     
    if current_user.role != "admin":
        print("***********yıldız yıldız ********************")
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user

# routers/user_routes.py (Değiştirilmesi gereken import satırı)
from auth.authorization import get_current_active_user
