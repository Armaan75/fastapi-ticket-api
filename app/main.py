from fastapi import FastAPI

from .db import Base, engine
from .routers import users, tickets

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(tickets.router)


@app.get("/")
def root():
    return {"message": "FastAPI is running"}
