from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.dependencies import get_current_user
from app.database import get_db
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse, BulkTaskCreate
from app.schemas.common_schema import APIResponse
from app.services import task_service
from app.core.response import success_response

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# 🔹 Create Task
@router.post("/", response_model=APIResponse[TaskResponse])
def create(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["user_id"]

    new_task = task_service.create_task(db, task, user_id)
    return success_response(new_task, "Task created successfully")


# 🔹 Bulk Create
@router.post("/bulk", response_model=APIResponse[list[TaskResponse]])
def create_bulk_tasks(
    request: BulkTaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["user_id"]

    tasks = task_service.create_bulk_tasks(db, request.tasks, user_id)
    return success_response(tasks, "Bulk tasks created successfully")


# 🔹 Get All (WITH STATUS + FILTER + PAGINATION)
@router.get("/", response_model=APIResponse[dict])
def get_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = None,  # ✅ NEW
    search: Optional[str] = None,
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
):
    user_id = current_user["user_id"]
    role = current_user["role"]

    result = task_service.get_tasks(
        db=db,
        user_id=user_id,
        role=role,
        limit=limit,
        offset=offset,
        status=status,  # ✅ NEW
        search=search,
        sort_by=sort_by,
        order=order,
    )

    return success_response(result, "Tasks fetched successfully")


# 🔹 Get by ID
@router.get("/{task_id}", response_model=APIResponse[TaskResponse])
def get_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["user_id"]
    role = current_user["role"]

    task = task_service.get_task_id(db, task_id, user_id, role)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return success_response(task, "Task fetched successfully")


# 🔹 Update Task (status + completion handled here)
@router.put("/{task_id}", response_model=APIResponse[TaskResponse])
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["user_id"]
    role = current_user["role"]

    updated = task_service.update_task(db, task_id, task, user_id, role)

    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")

    return success_response(updated, "Task updated successfully")


# 🔹 Delete Task (SOFT DELETE)
@router.delete("/{task_id}", response_model=APIResponse[None])
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["user_id"]
    role = current_user["role"]

    deleted = task_service.delete_task(db, task_id, user_id, role)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return success_response(None, "Task deleted successfully")
