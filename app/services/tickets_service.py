from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Ticket, User
from ..schemas import TicketCreate, TicketUpdate

def create_ticket(db: Session, payload: TicketCreate, current_user: User) -> Ticket:
    ticket = Ticket(
        title=payload.title,
        description=payload.description,
        user_id=current_user.id,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def get_ticket(db: Session, ticket_id: int) -> Ticket:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

def assert_owner(ticket: Ticket, current_user: User) -> None:
    if ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

def update_ticket(db: Session, ticket: Ticket, payload: TicketUpdate) -> Ticket:
    if payload.title is not None:
        ticket.title = payload.title
    if payload.description is not None:
        ticket.description = payload.description
    if payload.status is not None:
        ticket.status = payload.status

    db.commit()
    db.refresh(ticket)
    return ticket

def delete_ticket(db: Session, ticket: Ticket) -> dict:
    db.delete(ticket)
    db.commit()
    return {"deleted": True, "ticket_id": ticket.id}
