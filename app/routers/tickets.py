from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from ..db import get_db
from ..models import Ticket, User
from ..schemas import (
    TicketCreate,
    TicketOut,
    TicketUpdate,
    TicketListResponse,
    TicketStatus,
    TicketPriority,
)
from ..auth import get_current_user
from ..services import tickets_service

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", response_model=TicketOut)
def create_ticket(
    payload: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return tickets_service.create_ticket(db, payload, current_user)


@router.get("", response_model=TicketListResponse)
def list_tickets(
    status: TicketStatus | None = None,
    priority: TicketPriority | None = None,
    q: str | None = None,
    limit: int = Query(20, ge=1, le=100),
    skip: int = Query(0, ge=0),
    sort: str = "-created_at",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only show current user's tickets
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

    return {"items": items, "limit": limit, "skip": skip, "total": total}


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = tickets_service.get_ticket(db, ticket_id)
    tickets_service.assert_owner(ticket, current_user)
    return ticket


@router.patch("/{ticket_id}", response_model=TicketOut)
def update_ticket(
    ticket_id: int,
    payload: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = tickets_service.get_ticket(db, ticket_id)
    tickets_service.assert_owner(ticket, current_user)
    return tickets_service.update_ticket(db, ticket, payload)


@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = tickets_service.get_ticket(db, ticket_id)
    tickets_service.assert_owner(ticket, current_user)
    return tickets_service.delete_ticket(db, ticket)