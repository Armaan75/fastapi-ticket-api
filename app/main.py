from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from .db import Base, engine, get_db
from .models import User
from .schemas import UserCreate, UserOut
from .models import Ticket
from .schemas import TicketCreate, TicketOut
from .schemas import TicketUpdate


app = FastAPI()

# Create tables on startup (simple dev approach)
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "FastAPI is running"}


@app.post(
    "/users",
    response_model=UserOut,
    responses={
        400: {"description": "Email already exists"}
    }
)

def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(email=payload.email, full_name=payload.full_name)
    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    return user


@app.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.post("/tickets", response_model=TicketOut)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    ticket = Ticket(
        title=payload.title,
        description=payload.description,
        user_id=payload.user_id
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@app.get("/tickets", response_model=list[TicketOut])
def list_tickets(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Ticket)
    if status:
        query = query.filter(Ticket.status == status)
    return query.all()

@app.patch("/tickets/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        return {"error": "Ticket not found"}  # we'll improve this later

    if payload.title is not None:
        ticket.title = payload.title
    if payload.description is not None:
        ticket.description = payload.description
    if payload.status is not None:
        ticket.status = payload.status

    db.commit()
    db.refresh(ticket)
    return ticket
