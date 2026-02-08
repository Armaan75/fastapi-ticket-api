from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None

    class Config:
        from_attributes = True  # allows SQLAlchemy -> Pydantic conversion

class TicketCreate(BaseModel):
    title: str
    description: str | None = None
    user_id: int


class TicketOut(BaseModel):
    id: int
    title: str
    description: str | None
    user_id: int

    class Config:
        from_attributes = True
