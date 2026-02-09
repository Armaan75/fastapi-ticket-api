from fastapi import FastAPI

from .db import Base, engine
from .routers import users, tickets
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(tickets.router)


@app.get("/")
def root():
    return {"message": "FastAPI is running"}
