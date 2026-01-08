from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import donor


@asynccontextmanager
async def lifespan(app: FastAPI):
    pass


# app = FastAPI(lifespan=lifespan)
app = FastAPI()
app.include_router(donor.router, prefix="/donor", tags=["Donor"])
