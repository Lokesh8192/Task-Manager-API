from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password, verify_password, create_access_token
from sqlalchemy import or_


def register_user(db: Session, user: UserCreate):
    existing = (
        db.query(User)
        .filter(
            or_(
                User.email == user.email,
                User.phone == user.phone,
                User.username == user.username,
            )
        )
        .first()
    )

    if existing:
        return None

    new_user = User(
        email=user.email,
        phone=user.phone,
        username=user.username,
        password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, login: str, password: str):
    user = (
        db.query(User)
        .filter(or_(User.email == login, User.phone == login, User.username == login))
        .first()
    )

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def login_user(db: Session, login: str, password: str):
    user = authenticate_user(db, login, password)

    if not user:
        return None

    token = create_access_token({"user_id": user.id, "role": user.role})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "phone": user.phone,
            "username": user.username,
            "role": user.role
        },
    }
