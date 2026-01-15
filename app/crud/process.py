from sqlalchemy import Integer, case, cast, func, select, true
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload, load_only, selectinload

from app.db.models.donor import Donors
from app.db.models.process import Processes, Workflows, WorkflowSteps
from app.db.models.products import Tissues
from app.schemas.process import ProcessSchema, WorkflowSchema, WorkflowStepsSchema


async def create_process(request: ProcessSchema, db: AsyncSession):
    process = Processes(**request.model_dump())
    db.add(process)
    await db.commit()
    await db.refresh(process)
    return process


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


# async def get_process_template(db: AsyncSession):

#     # workflow id from process using donor id
#     # template from work flow

#     # Aliases (optional, but mirrors your SQL table aliases t, p, w)

#     p = aliased(Processes)
#     w = aliased(Workflows)

#     room_assigned_donor_dict = {}

#     stmt = select(p.tissue_id, p.donor_id, w.template_json).join(
#         w, p.workflow_id == w.workflow_id
#     )

#     results = await db.execute(stmt)

#     process_data = results.mappings().all()

#     for data in process_data:
#         data_dict = dict(data)
#         tissue_id = data.get("tissue_id")
#         donor_id = data.get("donor_id")
#         template_json = data.get("template_json", [])

#         if room_assigned_donor_dict.get(donor_id, []):
#             donor_dict = {"tissue_id": tissue_id, template_json:template_json}
#             room_assigned_donor_dict[donor_id] =

#         print("donor id ------", donor_id)
#         template_json = data.get("template_json", [])
#         # steps = template_json["layout_sections"]["steps_config"]["steps"]

#     #     print("tissue id", data.get("tissue_id"))
#     # process_data[1]["check"] = "check -------"
#     return process_data


stmt = select(Donors).options(
    load_only(Donors.donor_id, Donors.znumber),
    selectinload(Donors.processes).options(
        load_only(Processes.process_id, Processes.workflow_id),
        joinedload(Processes.workflow).options(
            load_only(Workflows.workflow_id, Workflows.template_json)
        ),
        selectinload(Processes.workflow_steps).options(
            load_only(WorkflowSteps.step_id, WorkflowSteps.process_id)
        ),
    ),
)


async def get_process_template(db: AsyncSession):

    # d = aliased(Donors)
    # p = aliased(Processes)

    # stmt = select(
    #     d.donor_id, d.znumber, d.name, p.process_id, p.tissue_id, p.workflow_id
    # ).join(p, d.donor_id == p.donor_id)
    # results = await db.execute(stmt)

    # stmt = select(Donors).options(
    #     load_only(Donors.donor_id, Donors.znumber),
    #     selectinload(Donors.processes).joinedload(Processes.workflow),
    #     selectinload(Donors.processes).selectinload(Processes.workflow_steps),
    # )  # assuming you defined relationship

    stmt = select(Donors).options(
        load_only(Donors.donor_id, Donors.znumber),
        selectinload(Donors.processes).options(
            load_only(Processes.process_id, Processes.workflow_id),
            joinedload(Processes.workflow).options(
                load_only(Workflows.workflow_id, Workflows.template_json)
            ),
            selectinload(Processes.workflow_steps),
            # .options(
            #     load_only(WorkflowSteps.step_id, WorkflowSteps.process_id)
            # ),
        ),
    )
    results = await db.execute(stmt)
    donors = results.scalars().all()

    # for donor in donors:
    #     for process in donor.processes:
    #         wf = process.workflow
    #         allowed = wf.template_json.get("columns", [])
    #         # now build a second query for WorkflowSteps
    #         cols = [getattr(WorkflowSteps, c) for c in allowed]
    #         step_stmt = select(*cols).where(WorkflowSteps.process_id == process.process_id)
    #         steps = db.execute(step_stmt).all()

    return donors
