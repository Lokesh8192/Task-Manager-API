from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.schemas.common_schema import APIResponse
from app.services import auth_service
from app.core.response import success_response

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=APIResponse[UserResponse])
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = auth_service.register_user(db, user)

    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")

    return success_response(new_user, "User registered successfully")


@router.post("/login", response_model=APIResponse[dict])
def login(user: UserLogin, db: Session = Depends(get_db)):
    result = auth_service.login_user(db, user.login, user.password)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return success_response(result, "Login successful")
