from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import User
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
    return tickets_service.list_tickets(
        db=db,
        current_user=current_user,
        status=status,
        priority=priority,
        q=q,
        limit=limit,
        skip=skip,
        sort=sort,
    )


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