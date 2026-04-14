from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, get_db, Base
from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate, Todo
import app.crud as crud

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo CRUD API",
    description="A RESTful API for managing todos with full CRUD operations",
    version="1.0.0",
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)


@app.get("/todos", response_model=List[Todo])
def read_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    todos = crud.get_todos(db=db, skip=skip, limit=limit)
    return todos


@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db=db, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    updated_todo = crud.update_todo(db=db, todo_id=todo_id, todo=todo)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    success = crud.delete_todo(db=db, todo_id=todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}
