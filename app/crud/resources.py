from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.resources import Materials, Machines
from app.schemas.resources import MaterialSchema, MachineSchema


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


async def create_machine(db: AsyncSession, request: MachineSchema) -> Machines:
    # Ensure enums are serialized to their values (strings) for SQLAlchemy Enum columns
    payload = request.model_dump()

    new_machine = Machines(**payload)
    db.add(new_machine)

    await db.commit()
    await db.refresh(new_machine)

    return new_machine


async def list_machines(db: AsyncSession, offset: int = 0, limit: int = 100):
    stmt = select(Machines).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_machine_by_id(db: AsyncSession, machine_id: int):
    stmt = select(Machines).where(Machines.machine_id == machine_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def update_machine(db: AsyncSession, machine_id: int, request: MachineSchema):
    machine = await get_machine_by_id(db, machine_id)
    if not machine:
        return None

    data = request.model_dump()

    for field in ["name", "type", "programs", "scancode", "machine_room_id", "status"]:
        if field in data and data[field] is not None:
            setattr(machine, field, data[field])

    await db.commit()
    await db.refresh(machine)
    return machine


async def delete_machine(db: AsyncSession, machine_id: int) -> bool:
    machine = await get_machine_by_id(db, machine_id)
    if not machine:
        return False

    await db.delete(machine)
    await db.commit()
    return True
