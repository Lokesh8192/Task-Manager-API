from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.core.enums import TaskStatus  # ✅ FIXED


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus  # ✅ better
    created_at: datetime

    class Config:
        from_attributes = True


class BulkTaskCreate(BaseModel):
    tasks: List[TaskCreate]
