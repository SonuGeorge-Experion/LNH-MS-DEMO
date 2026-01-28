from fastapi import APIRouter, status, Depends, Body, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.db.async_session import get_async_db
from app.schemas.clean_room import (
    CleanRoomsSchema,
    CleanRoomsUpdateSchema,
    CleanRoomsUpdateRespSchema,
    ShiftsSchema,
    ShiftsUpdateRespSchema,
    RoomAssignmentsSchema,
    RoomAssignmentsRespSchema,
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


@router.patch(
    "/clean/{room_id}",
    response_model=CleanRoomsUpdateRespSchema,
    summary="Update Clean Room Details",
    responses={200: {"description": "Clean Room updated successfully."}},
)
async def update_clean_room(
    room_id: int,
    request: CleanRoomsUpdateSchema = Body(example=sampleAddCleanRoom),
    db: AsyncSession = Depends(get_async_db),
):
    try:
        updated_room_details = await room_crud.update_clean_room(room_id, request, db)
        if not updated_room_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Clean Room ID: {room_id} not found",
            )
        return updated_room_details
    except IntegrityError as e:
        await db.rollback()
        if "clean_rooms_serial_number_key" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Serial Number {request.serial_number} already exists.",
            )
        if "clean_rooms_serial_number_check" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Validation error: The constraint clean_rooms_serial_number_check was violated.",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Data Integrity violation"
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Error Occurred. Please try later.",
        )


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


@router.patch(
    "/assignment/{assignment_id}",
    response_model=RoomAssignmentsRespSchema,
    summary="Update Room Assignment Details",
    responses={200: {"description": "Room Assignment updated successfully."}},
)
async def update_room_assignment(
    assignment_id: int,
    request: RoomAssignmentsSchema = Body(example=sampleAddRoomAssignment),
    db: AsyncSession = Depends(get_async_db),
):
    try:
        updated_room_details = await room_crud.update_room_assignment(
            assignment_id, request, db
        )
        if not updated_room_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room Assignment ID: {assignment_id} not found",
            )
        return updated_room_details
    except IntegrityError as e:
        await db.rollback()
        error_msg = str(e.orig).lower()
        if "room_assignments_process_id_key" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Process ID {request.process_id} already exists.",
            )
        elif "unique_room_shift" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Room Number {request.room_id} and Shift {request.shift_id} combo already exists.",
            )
        fk_map = {
            "fk_process_link": "Process Id",
            "room_assignments_room_id_fkey": "Clean Room Id",
            "room_assignments_shift_id_fkey": "Shift Id",
        }
        detail = next(
            (f"Invalid {v}" for k, v in fk_map.items() if k in error_msg), None
        )
        if not detail:
            detail = "Data Integrity violation"

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Error Occurred. Please try later.",
        )


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


@router.patch(
    "/shift/{shift_id}",
    response_model=ShiftsUpdateRespSchema,
    summary="Update Shift Details",
    responses={200: {"description": "Shift updated successfully."}},
)
async def update_shift(
    shift_id: int,
    request: ShiftsSchema = Body(example=sampleAddShift),
    db: AsyncSession = Depends(get_async_db),
):
    try:
        updated_shift_details = await room_crud.update_shift(shift_id, request, db)
        if not updated_shift_details:
            print("Exceppp")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shift ID: {shift_id} not found",
            )
        return updated_shift_details
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Data Integrity violation"
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Error Occurred. Please try later.",
        )


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
