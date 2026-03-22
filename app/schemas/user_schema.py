from datetime import datetime
import re

from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional
from app.core.enums import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    username: Optional[str] = None
    password: str

    # 📧 Email validation
    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v is None:
            return v

        email = v.lower().strip()

        # Length check
        if len(email) > 254:
            raise ValueError("Email is too long")

        # Basic regex (extra strict layer)
        pattern = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")

        # Optional: block disposable domains
        blocked_domains = ["tempmail.com", "10minutemail.com"]
        domain = email.split("@")[-1]

        if domain in blocked_domains:
            raise ValueError("Disposable email addresses are not allowed")

        return email

    # 🔐 Password validation
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")

        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")

        if not re.search(r"[@$!%*?&]", v):
            raise ValueError("Password must contain at least one special character")

        return v

    # 📱 Phone validation
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return v

        if not re.fullmatch(r"[6-9]\d{9}", v):
            raise ValueError("Invalid phone number (must be 10 digits, Indian format)")

        return v

    # 👤 Username validation
    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if v is None:
            return v

        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")

        if not re.fullmatch(r"[a-zA-Z0-9_]+", v):
            raise ValueError(
                "Username can only contain letters, numbers, and underscore"
            )

        return v

    # 🔥 At least one required
    @model_validator(mode="after")
    def validate_one_required(self):
        if not (self.email or self.phone or self.username):
            raise ValueError("At least one of email, phone, or username is required")
        return self


class UserLogin(BaseModel):
    login: str
    password: str

    @field_validator("login")
    @classmethod
    def validate_login(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Login (email/phone/username) is required")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password is too short")
        return v


class UserResponse(BaseModel):
    id: int
    email: Optional[EmailStr]
    phone: Optional[str]
    username: Optional[str]
    role: UserRole   # ✅ NOT str
    created_at: datetime

    class Config:
        from_attributes = True
