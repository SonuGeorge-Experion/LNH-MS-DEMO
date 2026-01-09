from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import process as process_crud
from app.db.async_session import get_async_db
from app.schemas.process import WorkflowSchema, WorkflowStepsSchema

router = APIRouter()


@router.post(
    "/workflow/",
    status_code=status.HTTP_201_CREATED,
)
async def create_workflow(
    request: WorkflowSchema,
    db: AsyncSession = Depends(get_async_db),
):

    try:
        workflow = await process_crud.create_workflow(request, db)
        return {"resp": f"Workflow created for process {workflow.name}"}
    except IntegrityError as ie:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Workflow steps already exist for process. {ie}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Error Occurred. Please try later. {e}",
        )


@router.post("/workflow-steps/", status_code=status.HTTP_201_CREATED)
async def populate_workflow_data(
    request: WorkflowStepsSchema,
    db: AsyncSession = Depends(get_async_db),
):
    workflow_steps = await process_crud.create_workflow_steps(request, db)
    return {"resp": f"Workflow steps created for process {workflow_steps.step_id}"}


@router.get(
    "/workflow-steps/{process_id}",
    status_code=status.HTTP_200_OK,
)
async def get_workflow_for_process(
    process_id: int,
    db: AsyncSession = Depends(get_async_db),
):

    workflow_steps = await process_crud.get_process_based_workflow(process_id, db)
    return workflow_steps
