from fastapi import APIRouter, status, Depends, Body, HTTPException, Response
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


@router.delete(
    "/clean/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Clean Room.",
    description="Removes Clean room by ID",
    responses={
        204: {"description": "Clean Room deleted successfully."},
        404: {"description": "Clean Room ID: X not found"},
        500: {"description": "Internal Error Occurred. Please try later."},
    },
)
async def delete_clean_room(room_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        deleted_room = await room_crud.delete_clean_room(room_id, db)
        if not deleted_room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Clean Room ID: {room_id} not found",
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Error Occurred. Please try later.",
        )


@router.post("/assignment", status_code=status.HTTP_201_CREATED)
async def add_room_assignments(
    request: RoomAssignmentsSchema = Body(example=sampleAddRoomAssignment),
    db: AsyncSession = Depends(get_async_db),
):
    cleanrooms = await room_crud.add_room_assignments(request, db)
    return cleanrooms


@router.delete(
    "/assignment/{assignment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletes Assignment.",
    description="Removes Assignment by ID",
    responses={
        204: {"description": "Assignment deleted successfully."},
        404: {"description": "Assignment ID: X not found"},
        500: {"description": "Internal Error Occurred. Please try later."},
    },
)
async def delete_assignment(
    assignment_id: int, db: AsyncSession = Depends(get_async_db)
):
    try:
        deleted_assignment = await room_crud.delete_assignment(assignment_id, db)
        if not deleted_assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Assignment ID: {assignment_id} not found",
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Error Occurred. Please try later.",
        )


@router.post("/shift", status_code=status.HTTP_201_CREATED)
async def add_shift(
    request: ShiftsSchema = Body(example=sampleAddShift),
    db: AsyncSession = Depends(get_async_db),
):
    cleanrooms = await room_crud.add_shift(request, db)
    return cleanrooms


@router.delete(
    "/shift/{shift_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletes Shift.",
    description="Removes Shift by ID",
    responses={
        204: {"description": "Shift deleted successfully."},
        404: {"description": "Shift ID: X not found"},
        500: {"description": "Internal Error Occurred. Please try later."},
    },
)
async def delete_shift(shift_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        deleted_shift = await room_crud.delete_shift(shift_id, db)
        if not deleted_shift:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shift ID: {shift_id} not found",
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Error Occurred. Please try later.",
        )
