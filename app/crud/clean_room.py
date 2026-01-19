from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, exists, select
import re
import asyncpg

from app.schemas.clean_room import CleanRoomsSchema, ShiftsSchema, RoomAssignmentsSchema
from app.db.models.clean_room import CleanRooms, RoomAssignments, Shifts


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


async def col_duplicate(db: AsyncSession, param, check_value) -> bool:
    if isinstance(check_value, int):
        base_clause = param == check_value
    else:
        base_clause = func.lower(param) == check_value.lower()
    exists_stmt = select(exists().where(base_clause))
    is_duplicate = await db.scalar(exists_stmt)
    return is_duplicate
