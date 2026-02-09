from pydantic import BaseModel, EmailStr
from typing import Literal
from pydantic import ConfigDict



TicketStatus = Literal["open", "in_progress", "resolved"]

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TicketCreate(BaseModel):
    title: str
    description: str | None = None
    user_id: int


class TicketOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: TicketStatus
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TicketStatus | None = None