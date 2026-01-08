from sqlalchemy.ext.asyncio import AsyncSession

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
