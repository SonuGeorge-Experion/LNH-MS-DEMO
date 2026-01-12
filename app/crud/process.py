from sqlalchemy import Integer, case, cast, func, select, true
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.process import Processes, Workflows, WorkflowSteps
from app.schemas.process import WorkflowSchema, WorkflowStepsSchema


async def create_workflow(request: WorkflowSchema, db: AsyncSession):
    workflow = Workflows(**request.model_dump())
    db.add(workflow)
    await db.commit()
    await db.refresh(workflow)
    return workflow


async def create_workflow_steps(request: WorkflowStepsSchema, db: AsyncSession):
    # Validate foreign key: process_id must exist in Processes
    result = await db.execute(
        select(Processes.process_id).where(Processes.process_id == request.process_id)
    )
    if result.scalar_one_or_none() is None:
        raise ValueError(f"Invalid process_id {request.process_id}: does not exist")

    workflow_steps = WorkflowSteps(**request.model_dump())
    db.add(workflow_steps)
    await db.commit()
    await db.refresh(workflow_steps)
    return workflow_steps


# select w.name as workflow_name, step_element from workflows as w
# cross join jsonb_array_elements(w.template_json->'layout_sections'->'steps_config'->'steps')
# as step_element
# where workflow_id=3


# SELECT
#     p.process_id,
#     w.name AS workflow_name,
#     (step_element->>'step_num')::INT AS step_num,
#     step_element->>'title' AS step_title,
#     step_element->>'component' AS component_type
# FROM processes p
# JOIN workflows w on p.workflow_id = w.workflow_id
# CROSS JOIN jsonb_array_elements(w.template_json->'layout_sections'->'steps_config'->'steps')
# as step_element where p.process_id=1

# with template_steps as (SELECT
#     p.process_id,
#     w.name AS workflow_name,
#     (step_element->>'step_num')::INT AS step_num,
#     step_element->>'title' AS step_title,
#     step_element->>'component' AS component_type
# FROM processes p
# JOIN workflows w on p.workflow_id = w.workflow_id
# CROSS JOIN jsonb_array_elements(w.template_json->'layout_sections'->'steps_config'->'steps')
# as step_element where p.process_id=1
# )
# SELECT
#     t.step_num,
#     t.step_title,
#     t.component_type,
# CASE
#     WHEN ws.step_id IS NOT NULL THEN 'DONE'
#     ELSE 'PENDING'
# END AS status,
# ws.initials,
# ws.actual_duration,
# ws.step_num
# FROM template_steps t
# LEFT JOIN workflow_steps ws
#   ON t.process_id = ws.process_id
#  AND t.step_num = ws.step_num
# ORDER BY t.step_num ASC;


async def get_process_based_workflow(process_id: int, db: AsyncSession):
    print("process_id::", process_id)

    step_element = func.jsonb_array_elements(
        Workflows.template_json["layout_sections"]["steps_config"]["steps"]
    ).table_valued("value")

    # stmt = select(step_element.c.value)
    # print(stmt)

    # stmt = (
    #     select(
    #         Workflows.name.label("workflow_name"),
    #         cast(
    #             cast(step_element.c.value, postgresql.JSONB)["step_num"].astext, Integer
    #         ).label("step_num"),
    #         cast(step_element.c.value, postgresql.JSONB)["title"].astext.label(
    #             "step_title"
    #         ),
    #         cast(step_element.c.value, postgresql.JSONB)["component"].astext.label(
    #             "component_type"
    #         ),
    #     )
    #     .select_from(Workflows)
    #     .join(step_element, true(), isouter=False)
    #     .where(Workflows.workflow_id == 3)
    # )

    # stmt = (
    #     select(
    #         Processes.process_id,
    #         Workflows.name.label("workflow_name"),
    #         cast(
    #             cast(step_element.c.value, postgresql.JSONB)["step_num"].astext, Integer
    #         ).label("step_num"),
    #         cast(step_element.c.value, postgresql.JSONB)["title"].astext.label(
    #             "step_title"
    #         ),
    #         cast(step_element.c.value, postgresql.JSONB)["component"].astext.label(
    #             "component_type"
    #         ),
    #     )
    #     .select_from(Processes)
    #     .join(Workflows, Processes.workflow_id == Workflows.workflow_id)
    #     .join(step_element, true())
    #     .where(Processes.process_id == 1)
    # )

    template_steps = (
        select(
            Processes.process_id,
            Workflows.name.label("workflow_name"),
            cast(
                cast(step_element.c.value, postgresql.JSONB)["step_num"].astext, Integer
            ).label("step_num"),
            cast(step_element.c.value, postgresql.JSONB)["title"].astext.label(
                "step_title"
            ),
            cast(step_element.c.value, postgresql.JSONB)["component"].astext.label(
                "component_type"
            ),
        )
        .select_from(Processes)
        .join(Workflows, Processes.workflow_id == Workflows.workflow_id)
        .join(step_element, true())
        .where(Processes.process_id == process_id)
        .cte("template_steps")
    )

    stmt = (
        select(
            template_steps.c.step_num,
            template_steps.c.step_title,
            template_steps.c.component_type,
            case((WorkflowSteps.step_id.isnot(None), "DONE"), else_="PENDING").label(
                "status"
            ),
            WorkflowSteps.initials,
            WorkflowSteps.actual_duration,
            WorkflowSteps.step_data,
        )
        .select_from(template_steps)
        .outerjoin(
            WorkflowSteps,
            (template_steps.c.process_id == WorkflowSteps.process_id)
            & (template_steps.c.step_num == WorkflowSteps.step_num),
        )
        .order_by(template_steps.c.step_num.asc())
    )

    result = await db.execute(stmt)
    return result.mappings().all()
