from fastapi import APIRouter, status, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.async_session import get_async_db
from app.schemas.clean_room import (
    CleanRoomsSchema,
    ShiftsSchema,
    RoomAssignmentsSchema,
    CleanRoomsCreateResp,
    ErrorResp,
)
from app.schemas.clean_room import (
    sampleAddCleanRoom,
    sampleAddRoomAssignment,
    sampleAddShift,
)
from app.crud import clean_room as room_crud

router = APIRouter()


@router.post(
    "/clean",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": CleanRoomsCreateResp},
        status.HTTP_409_CONFLICT: {
            "model": ErrorResp,
            "detail": "Serial Number: 4 number already exists.",
        },
    },
)
async def add_clean_rooms(
    request: CleanRoomsSchema = Body(example=sampleAddCleanRoom),
    db: AsyncSession = Depends(get_async_db),
):
    cleanrooms = await room_crud.add_clean_room(request, db)
    return cleanrooms


@router.post("/assignment", status_code=status.HTTP_201_CREATED)
async def add_room_assignments(
    request: RoomAssignmentsSchema = Body(example=sampleAddRoomAssignment),
    db: AsyncSession = Depends(get_async_db),
):
    cleanrooms = await room_crud.add_room_assignments(request, db)
    return cleanrooms


@router.post("/shift", status_code=status.HTTP_201_CREATED)
async def add_shift(
    request: ShiftsSchema = Body(example=sampleAddShift),
    db: AsyncSession = Depends(get_async_db),
):
    cleanrooms = await room_crud.add_shift(request, db)
    return cleanrooms
