from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.resources import Materials
from app.schemas.resources import MaterialSchema


async def create_material(db: AsyncSession, request: MaterialSchema) -> Materials:
    new_material = Materials(**request.model_dump())
    db.add(new_material)

    await db.commit()
    await db.refresh(new_material)

    return new_material


async def list_materials(db: AsyncSession, offset: int = 0, limit: int = 100):
    stmt = select(Materials).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_material_by_id(db: AsyncSession, material_id: int):
    stmt = select(Materials).where(Materials.material_id == material_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def update_material(db: AsyncSession, material_id: int, request: MaterialSchema):
    material = await get_material_by_id(db, material_id)
    if not material:
        return None

    data = request.model_dump()

    for field in ["name", "scancode", "quantity_available", "materials_room_id", "unit"]:
        if field in data and data[field] is not None:
            setattr(material, field, data[field])

    await db.commit()
    await db.refresh(material)
    return material


async def delete_material(db: AsyncSession, material_id: int) -> bool:
    material = await get_material_by_id(db, material_id)
    if not material:
        return False

    await db.delete(material)
    await db.commit()
    return True
