from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from ..models import Ticket, User
from ..schemas import (
    TicketCreate,
    TicketUpdate,
    TicketListResponse,
    TicketStatus,
    TicketPriority,
)


def create_ticket(db: Session, payload: TicketCreate, current_user: User) -> Ticket:
    ticket = Ticket(
        title=payload.title,
        description=payload.description,
        user_id=current_user.id,
        priority=payload.priority.value,
        status="open",
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
        ticket.status = payload.status.value
    if payload.priority is not None:
        ticket.priority = payload.priority.value

    db.commit()
    db.refresh(ticket)
    return ticket


def delete_ticket(db: Session, ticket: Ticket) -> dict:
    ticket_id = ticket.id
    db.delete(ticket)
    db.commit()
    return {"deleted": True, "ticket_id": ticket_id}


def list_tickets(
    db: Session,
    current_user: User,
    status: TicketStatus | None = None,
    priority: TicketPriority | None = None,
    q: str | None = None,
    limit: int = 20,
    skip: int = 0,
    sort: str = "-created_at",
) -> TicketListResponse:
    query = db.query(Ticket).filter(Ticket.user_id == current_user.id)

    if status:
        query = query.filter(Ticket.status == status.value)

    if priority:
        query = query.filter(Ticket.priority == priority.value)

    if q:
        q_like = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Ticket.title.ilike(q_like),
                Ticket.description.ilike(q_like),
            )
        )

    total = query.with_entities(func.count(Ticket.id)).scalar() or 0

    allowed = {"created_at", "updated_at", "priority", "status", "title", "id"}
    desc_order = sort.startswith("-")
    field = sort[1:] if desc_order else sort

    if field not in allowed:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {field}")

    sort_col = getattr(Ticket, field)
    query = query.order_by(sort_col.desc() if desc_order else sort_col.asc())

    items = query.offset(skip).limit(limit).all()

    return TicketListResponse(
        items=items,
        limit=limit,
        skip=skip,
        total=total,
    )