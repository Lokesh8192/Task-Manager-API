from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class UserRole(str, Enum):
    user = "user"
    admin = "admin"
