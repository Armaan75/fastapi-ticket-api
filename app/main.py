from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import User
from .schemas import UserCreate, UserOut

app = FastAPI()

# Create tables on startup (simple dev approach)
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "FastAPI is running"}


@app.post("/users", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(email=payload.email, full_name=payload.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
