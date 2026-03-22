from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.common_schema import APIResponse
from app.core.response import success_response
from app.core.dependencies import require_admin
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=APIResponse[list[UserResponse]])
def get_all_users(db: Session = Depends(get_db), admin=Depends(require_admin)):
    users = db.query(User).all()

    # ✅ FIX
    user_list = [UserResponse.model_validate(user) for user in users]

    return success_response(user_list, "Users fetched successfully")


@router.put("/users/{user_id}/make-admin", response_model=APIResponse[None])
def make_admin(
    user_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = "admin"
    db.commit()

    return success_response(None, "User promoted to admin")


@router.put("/users/{user_id}/remove-admin", response_model=APIResponse[None])
def remove_admin(
    user_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = "user"
    db.commit()

    return success_response(None, "Admin role removed")


@router.delete("/users/{user_id}", response_model=APIResponse[None])
def delete_user(
    user_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return success_response(None, "User deleted successfully")
