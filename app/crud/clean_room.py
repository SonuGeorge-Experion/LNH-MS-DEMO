from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, exists, select, delete
import re
import asyncpg

from app.schemas.clean_room import (
    CleanRoomsSchema,
    CleanRoomsUpdateSchema,
    ShiftsSchema,
    RoomAssignmentsSchema,
)
from app.db.models.clean_room import CleanRooms, RoomAssignments, Shifts


async def fetch_by_id(id: int, db: AsyncSession, model, id_col_name: str = "id"):
    id_column = getattr(model, id_col_name)
    stmt = select(model).where(id_column == id)
    result = await db.execute(stmt)
    print(f"Res: {result}")
    return result.scalar_one_or_none()


async def col_duplicate(db: AsyncSession, param, check_value) -> bool:
    if isinstance(check_value, int):
        base_clause = param == check_value
    else:
        base_clause = func.lower(param) == check_value.lower()
    exists_stmt = select(exists().where(base_clause))
    is_duplicate = await db.scalar(exists_stmt)
    return is_duplicate


async def add_clean_room(request: CleanRoomsSchema, db: AsyncSession):
    try:
        if await col_duplicate(db, CleanRooms.serial_number, request.serial_number):
            raise IntegrityError(
                statement=f"Serial Number: {request.serial_number} number already exists.",
                params={"serial_number": request.serial_number},
                orig=Exception("Duplicate key value violates unique constraint"),
            )
        cleanrooms = CleanRooms(**request.model_dump())
        db.add(cleanrooms)
        await db.commit()
        await db.refresh(cleanrooms)
        return cleanrooms
    except IntegrityError as e:
        await db.rollback()
        error_cause = str(e.orig)
        if (
            isinstance(error_cause, asyncpg.exceptions.CheckViolationError)
            or "violates check constraint" in error_cause
        ):
            # # constraint_name = getattr(raw_err, "constraint_name", "db_constraint")
            match = re.search(r'check constraint "([^"]+)"', error_cause)
            if match:
                constraint_name = match.group(1).strip()
            else:
                constraint_name = "unknown_constraint"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Validation error: The constraint '{constraint_name}' was violated.",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=e.statement,
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )


async def get_clean_room_by_id(room_id, db):
    clean_room_details = await fetch_by_id(room_id, db, CleanRooms, "room_id")
    return clean_room_details


async def list_clean_rooms(db: AsyncSession, offset: int = 0, limit: int = 100):
    stmt = select(CleanRooms).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_clean_room(id: int, request: CleanRoomsUpdateSchema, db: AsyncSession):
    try:
        room_details = await fetch_by_id(id, db, CleanRooms, "room_id")
        if not room_details:
            return None
        update_room_dict = request.model_dump(exclude_unset=True)
        for key, value in update_room_dict.items():
            if value is not None:
                setattr(room_details, key, value)
        await db.commit()
        await db.refresh(room_details)
        return room_details
    except Exception as e:
        await db.rollback()
        raise e


async def delete_clean_room(id: int, db: AsyncSession):
    try:
        room = await fetch_by_id(id, db, CleanRooms, "room_id")
        if not room:
            return False

        await db.execute(delete(CleanRooms).where(CleanRooms.room_id == id))
        await db.commit()
        return True
    except Exception:
        await db.rollback()
        raise


async def add_room_assignments(request: RoomAssignmentsSchema, db: AsyncSession):
    try:
        if await col_duplicate(db, RoomAssignments.process_id, request.process_id):
            raise IntegrityError(
                statement=f"Process ID: {request.process_id} already exists.",
                params={"process_id": request.process_id},
                orig=Exception("Duplicate key value violates unique constraint"),
            )
        roomassignments = RoomAssignments(**request.model_dump())
        db.add(roomassignments)
        await db.commit()
        await db.refresh(roomassignments)
        return roomassignments
    except IntegrityError as e:
        await db.rollback()
        error_cause = str(e.orig)
        match = re.search(r'(\w+) constraint "([^"]+)"', error_cause)
        if match:
            c_type = match.group(1).lower()  # check, unique, or foreign
            c_name = match.group(2).strip()  # the actual key name

            status_map = {
                "check": status.HTTP_400_BAD_REQUEST,
                "foreign": status.HTTP_400_BAD_REQUEST,
                "unique": status.HTTP_409_CONFLICT,
            }

            detail_msg = f"Database {c_type} violation on '{c_name}'"

            raise HTTPException(
                status_code=status_map.get(c_type, status.HTTP_400_BAD_REQUEST),
                detail=detail_msg,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=e.statement,
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )


async def get_room_assignments_by_id(room_id, db):
    room_assign_details = await fetch_by_id(
        room_id, db, RoomAssignments, "assignment_id"
    )
    return room_assign_details


async def list_room_assignments(db: AsyncSession, offset: int = 0, limit: int = 100):
    stmt = select(RoomAssignments).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_room_assignment(
    id: int, request: RoomAssignmentsSchema, db: AsyncSession
):
    try:
        room_details = await fetch_by_id(id, db, RoomAssignments, "assignment_id")
        if not room_details:
            return None
        update_room_dict = request.model_dump(exclude_unset=True)
        for key, value in update_room_dict.items():
            if value is not None:
                setattr(room_details, key, value)
        await db.commit()
        await db.refresh(room_details)
        return room_details
    except Exception as e:
        await db.rollback()
        raise e


async def delete_assignment(id, db):
    try:
        room = await fetch_by_id(id, db, RoomAssignments, "assignment_id")
        if not room:
            return False

        await db.execute(
            delete(RoomAssignments).where(RoomAssignments.assignment_id == id)
        )
        await db.commit()
        return True
    except Exception:
        await db.rollback()
        raise


async def add_shift(request: ShiftsSchema, db: AsyncSession):
    try:
        shift = Shifts(**request.model_dump())
        db.add(shift)
        await db.commit()
        await db.refresh(shift)
        return shift
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )


async def get_shift_by_id(shift_id, db):
    shift_details = await fetch_by_id(shift_id, db, Shifts, "shift_id")
    return shift_details


async def list_shift(db: AsyncSession, offset: int = 0, limit: int = 100):
    stmt = select(Shifts).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_shift(id: int, request: ShiftsSchema, db: AsyncSession):
    try:
        shift_details = await fetch_by_id(id, db, Shifts, "shift_id")
        if not shift_details:
            return None
        update_shift_dict = request.model_dump(exclude_unset=True)
        for key, value in update_shift_dict.items():
            if value is not None:
                setattr(shift_details, key, value)
        await db.commit()
        await db.refresh(shift_details)
        return shift_details
    except Exception as e:
        await db.rollback()
        raise e


async def delete_shift(id, db):
    try:
        room = await fetch_by_id(id, db, Shifts, "shift_id")
        if not room:
            return False

        await db.execute(delete(Shifts).where(Shifts.shift_id == id))
        await db.commit()
        return True
    except Exception:
        await db.rollback()
        raise
