from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task_schema import TaskResponse
from sqlalchemy import or_, asc, desc
from app.core.enums import TaskStatus


# 🔹 Create Task
def create_task(db: Session, task, user_id: int):
    new_task = Task(
        title=task.title,
        description=task.description,
        status=getattr(task, "status", TaskStatus.pending),
        user_id=user_id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# 🔹 Bulk Create
def create_bulk_tasks(db: Session, tasks, user_id: int):
    task_objects = [
        Task(
            title=task.title,
            description=task.description,
            status=getattr(task, "status", "pending"),  # ✅ NEW
            user_id=user_id,
        )
        for task in tasks
    ]

    db.add_all(task_objects)
    db.commit()

    for task in task_objects:
        db.refresh(task)

    return task_objects


# 🔹 Get Tasks (ROLE + SOFT DELETE + STATUS + PAGINATION)
def get_tasks(
    db: Session,
    user_id: int,
    role: str,
    limit: int,
    offset: int,
    search: str = None,
    status: str = None,  # ✅ NEW
    sort_by: str = "created_at",
    order: str = "desc",
):
    # ✅ ROLE + SOFT DELETE
    if role == "admin":
        query = db.query(Task).filter(Task.is_deleted == False)
    else:
        query = db.query(Task).filter(Task.user_id == user_id, Task.is_deleted == False)

    # ✅ Filter: status
    if status:
        query = query.filter(Task.status == status)

    # ✅ Search
    if search:
        query = query.filter(
            or_(Task.title.ilike(f"%{search}%"), Task.description.ilike(f"%{search}%"))
        )

    # ✅ Total count
    total = query.count()

    # ✅ Sorting
    sort_column = getattr(Task, sort_by, Task.created_at)

    if order.lower() == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    # ✅ Pagination
    tasks = query.offset(offset).limit(limit).all()

    # ✅ Convert to Pydantic
    task_list = [TaskResponse.model_validate(t) for t in tasks]

    return {"items": task_list, "total": total, "limit": limit, "offset": offset}


# 🔹 Get by ID (ROLE + SOFT DELETE)
def get_task_id(db: Session, task_id: int, user_id: int, role: str):
    query = db.query(Task).filter(
        Task.id == task_id, Task.is_deleted == False  # ✅ IMPORTANT
    )

    if role != "admin":
        query = query.filter(Task.user_id == user_id)

    return query.first()


# 🔹 Update Task (ROLE BASED)
def update_task(db: Session, task_id: int, task, user_id: int, role: str):
    db_task = get_task_id(db, task_id, user_id, role)

    if not db_task:
        return None

    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task


# 🔹 Delete Task (SOFT DELETE)
def delete_task(db: Session, task_id: int, user_id: int, role: str):
    db_task = get_task_id(db, task_id, user_id, role)

    if not db_task:
        return None

    # ❌ HARD DELETE REMOVED
    # db.delete(db_task)

    # ✅ SOFT DELETE
    db_task.is_deleted = True
    db.commit()

    return db_task
