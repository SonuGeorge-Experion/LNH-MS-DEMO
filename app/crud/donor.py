from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.donor import Donors
from app.schemas.donor import DonorSchema


async def add_donor(request: DonorSchema, db: AsyncSession):

    new_donor = Donors(
        donor_id=request.donor_id,
        znumber=request.znumber,
        name=request.name,
        age=request.age,
        region=request.region,
        other_factors=request.other_factors,
    )
    print("New Donor to be added:", new_donor)
    db.add(new_donor)
    await db.commit()
    await db.refresh(new_donor)
    return new_donor

async def get_donors(db: AsyncSession,skip: int, limit: int):
    query = select(Donors).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def update_donor(db: AsyncSession, donor_id: int, donor_in: DonorSchema):
    query = select(Donors).where(Donors.donor_id == donor_id)
    result = await db.execute(query)
    db_donor = result.scalar_one_or_none()

    if db_donor:
        update_data = donor_in.model_dump()
        for key, value in update_data.items():
            setattr(db_donor, key, value)
        
        await db.commit()
        await db.refresh(db_donor)
    
    return db_donor