from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password
from app.core.config import settings


def create_default_admin(db: Session):
    # 🔍 Check if admin exists
    admin = db.query(User).filter(User.role == "admin").first()

    if admin:
        print("✅ Admin already exists")
        return

    # 🔥 Create admin from ENV
    new_admin = User(
        email=settings.ADMIN_EMAIL,
        username=settings.ADMIN_USERNAME,
        password=hash_password(settings.ADMIN_PASSWORD),
        role="admin",
    )

    db.add(new_admin)
    db.commit()

    print("🔥 Default admin created from .env")
