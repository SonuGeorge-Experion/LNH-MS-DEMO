from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import resources as resources_crud
from app.db.async_session import get_async_db
from app.dependencies.auth import require_roles
from app.schemas.resources import MaterialSchema, MaterialSchemaOut, MaterialSchemaCreate, MachineSchemaCreate, MachineSchemaOut, MachineSchema

router = APIRouter()


@router.post(
    "/materials",
    status_code=status.HTTP_201_CREATED,
)
async def create_material(
    request: MaterialSchemaCreate,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        material = await resources_crud.create_material(db, request)
        return {"resp": f"Material {material.name} has been created"}
    except IntegrityError as ie:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Material already exists or violates a constraint. {ie}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )


@router.post(
    "/machines",
    status_code=status.HTTP_201_CREATED,
)
async def create_machine(
    request: MachineSchemaCreate,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        machine = await resources_crud.create_machine(db, request)
        return {"resp": f"Machine {machine.name} has been created"}
    except IntegrityError as ie:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Machine already exists or violates a constraint. {ie}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )


@router.get(
    "/machines",
    status_code=status.HTTP_200_OK,
    response_model=List[MachineSchemaOut],
)
async def list_machines(
    offset: int = Query(0, ge=0),
    limit: int = Query(5, ge=1, le=100),
    current_user = Depends(require_roles("LNH-API-Role-User1")),
    db: AsyncSession = Depends(get_async_db),
):
    try:
        machines = await resources_crud.list_machines(db, offset=offset, limit=limit)
        return machines
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )


@router.get(
    "/machines/{machine_id}",
    status_code=status.HTTP_200_OK,
    response_model=MachineSchemaOut,
)
async def get_machine(machine_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        machine = await resources_crud.get_machine_by_id(db, machine_id)
        if not machine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
        return machine
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )


@router.put(
    "/machines/{machine_id}",
    status_code=status.HTTP_200_OK,
    response_model=MachineSchemaOut,
)
async def update_machine(
    machine_id: int,
    request: MachineSchema,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        machine = await resources_crud.update_machine(db, machine_id, request)
        if not machine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
        return machine
    except IntegrityError as ie:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Update would violate a constraint. {ie}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )


@router.delete(
    "/machines/{machine_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_machine(
    machine_id: int,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        deleted = await resources_crud.delete_machine(db, machine_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")
        return {"resp": f"Machine {machine_id} has been deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )


@router.get(
    "/materials",
    status_code=status.HTTP_200_OK,
    response_model=List[MaterialSchemaOut],
)
async def list_materials(
    offset: int = Query(0, ge=0),
    limit: int = Query(5, ge=1, le=100),
    db: AsyncSession = Depends(get_async_db),
):
    try:
        materials = await resources_crud.list_materials(db, offset=offset, limit=limit)
        return materials
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )


@router.get(
    "/materials/{material_id}",
    status_code=status.HTTP_200_OK,
    response_model=MaterialSchemaOut,
)
async def get_material(material_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        material = await resources_crud.get_material_by_id(db, material_id)
        if not material:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")
        return material
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )


@router.put(
    "/materials/{material_id}",
    status_code=status.HTTP_200_OK,
    response_model=MaterialSchemaOut,
)
async def update_material(
    material_id: int,
    request: MaterialSchema,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        material = await resources_crud.update_material(db, material_id, request)
        if not material:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")
        return material
    except IntegrityError as ie:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Update would violate a constraint. {ie}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )


@router.delete(
    "/materials/{material_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_material(
    material_id: int,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        deleted = await resources_crud.delete_material(db, material_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")
        return {"resp": f"Material {material_id} has been deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )
