from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import (
    donor,
    process,
    production_plan,
    production_process,
    products,
    resources,
    clean_room,
    auth
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    pass


# app = FastAPI(lifespan=lifespan)
app = FastAPI()
app.include_router(donor.router, prefix="/donor", tags=["Donor"])
app.include_router(process.router, prefix="/process", tags=["Tissue Process"])
app.include_router(
    production_plan.router, prefix="/api/v1/production", tags=["Production Plan"]
)
app.include_router(
    production_process.router, prefix="/production-process", tags=["Production Process"]
)
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(clean_room.router, prefix="/api/v1/rooms", tags=["Clean Rooms"])
app.include_router(resources.router, prefix="/api/v1/resources", tags=["Resources"])
app.include_router(auth.router,prefix="/api/v1/auth", tags=["Auth"])