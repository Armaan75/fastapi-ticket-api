from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Ticket, User
from ..schemas import TicketCreate, TicketOut, TicketUpdate, TicketListResponse
from ..auth import get_current_user
from ..services import tickets_service
from sqlalchemy import func

from fastapi import Query

limit: int = Query(20, ge=1, le=100)
offset: int = Query(0, ge=0)

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", response_model=TicketOut)
def create_ticket(
    payload: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return tickets_service.create_ticket(db, payload, current_user)


from fastapi import Query

@router.get("", response_model=TicketListResponse)
def list_tickets(
    status: str | None = None,
    user_id: int | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort: str = "-created_at",
    db: Session = Depends(get_db),
):
    query = db.query(Ticket)

    if status:
        query = query.filter(Ticket.status == status)
    if user_id:
        query = query.filter(Ticket.user_id == user_id)

    total = query.with_entities(func.count(Ticket.id)).scalar() or 0

    allowed = {"created_at", "updated_at", "priority", "status", "title", "id"}
    desc_order = sort.startswith("-")
    field = sort[1:] if desc_order else sort

    if field not in allowed:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {field}")

    sort_col = getattr(Ticket, field)
    query = query.order_by(sort_col.desc() if desc_order else sort_col.asc())

    items = query.offset(offset).limit(limit).all()

    return {"items": items, "limit": limit, "offset": offset, "total": total}


@router.patch("/{ticket_id}", response_model=TicketOut)
def update_ticket(
    ticket_id: int,
    payload: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    if payload.title is not None:
        ticket.title = payload.title
    if payload.description is not None:
        ticket.description = payload.description
    if payload.status is not None:
        ticket.status = payload.status

    db.commit()
    db.refresh(ticket)
    ticket = tickets_service.get_ticket(db, ticket_id)
    tickets_service.assert_owner(ticket, current_user)
    return tickets_service.update_ticket(db, ticket, payload)



@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return tickets_service.get_ticket(db, ticket_id)

@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(ticket)
    db.commit()
    ticket = tickets_service.get_ticket(db, ticket_id)
    tickets_service.assert_owner(ticket, current_user)
    return tickets_service.delete_ticket(db, ticket)

