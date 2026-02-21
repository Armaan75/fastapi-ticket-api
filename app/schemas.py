from pydantic import BaseModel, EmailStr
from typing import Literal, List
from pydantic import ConfigDict
from pydantic import Field
from datetime import datetime

TicketStatus = Literal["open", "in_progress", "resolved"]

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str | None = None
    password: str = Field(min_length=8, max_length=72)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TicketCreate(BaseModel):
    title: str
    description: str | None = None

class TicketOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: TicketStatus
    user_id: int
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    updated_at: datetime


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TicketStatus | None = None

class TicketListResponse(BaseModel):
    items: List["TicketOut"]
    limit: int
    offset: int
    total: int

from enum import Enum

class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"

class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"