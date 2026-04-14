from sqlalchemy.orm import Session
from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate
from typing import List, Optional


def create_todo(db: Session, todo: TodoCreate) -> Todo:
    db_todo = Todo(
        title=todo.title, description=todo.description, completed=todo.completed
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Todo]:
    return db.query(Todo).offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int) -> Optional[Todo]:
    return db.query(Todo).filter(Todo.id == todo_id).first()


def update_todo(db: Session, todo_id: int, todo: TodoUpdate) -> Optional[Todo]:
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        return None

    for key, value in todo.model_dump().items():
        setattr(db_todo, key, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int) -> bool:
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        return False

    db.delete(db_todo)
    db.commit()
    return True
