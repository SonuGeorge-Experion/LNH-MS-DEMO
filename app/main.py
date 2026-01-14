from contextlib import asynccontextmanager

from fastapi import FastAPI


from app.routers import donor, process, production_plan, products, resources

@asynccontextmanager
async def lifespan(app: FastAPI):
    pass


# app = FastAPI(lifespan=lifespan)
app = FastAPI()
app.include_router(donor.router, prefix="/donor", tags=["Donor"])
app.include_router(process.router, prefix="/process", tags=["Tissue Process"])
app.include_router(
    production_plan.router, prefix="/production", tags=["Production Plan"]
)
app.include_router(products.router, prefix="/tissue_category", tags=["Tissue_Category"])
app.include_router(resources.router, prefix="/resources", tags=["Resources"])

