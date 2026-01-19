from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.process import Processes, Workflows
from app.db.models.production_plan import ProductionPlans
from app.db.models.products import Tissues, Products, TissueCategories
from app.schemas.production_plan import ProductionPlanSchema


async def create_production_plan(request: ProductionPlanSchema, db: AsyncSession):
    prod_plan = ProductionPlans(**request.model_dump())
    db.add(prod_plan)
    await db.commit()
    await db.refresh(prod_plan)
    return prod_plan


async def get_donor_production_plan_with_workflow(donor_id: int, db: AsyncSession):
    """
    Docstring for get_donor_production_plan_with_workflow

    :param donor_id: Description
    :type donor_id: int
    :param db: Description
    :type db: AsyncSession

    Join production plan and tissue to identify the category,
    then using the category pick the workflow id for the particular
    tissue

    SQL Query
    *********
    INSERT INTO processes(
    plan_id,
    workflow_id,
    donor_id,
    tissue_id
    )

    SELECT
        pln.plan_id,
        wk.workflow_id,
        ts.donor_id,
        ts.tissue_id
    FROM production_plans pln
    JOIN tissues ts
        ON ts.tissue_id = pln.tissue_id
    JOIN (
        SELECT
            category_id,
            workflow_id
        FROM workflows
        WHERE is_active = true
        ORDER BY category_id, version DESC
    ) wk
        ON wk.category_id = ts.category_id
    WHERE
        ts.donor_id = 1001
        AND pln.status = 'approved';
    """
    print("donor id ----------", donor_id)
    wk_subq = (
        select(Workflows.category_id, Workflows.workflow_id)
        .where(Workflows.is_active.is_(True))
        .order_by(
            Workflows.category_id,
            Workflows.version.desc(),
        )
        .subquery()
    )

    select_stmt = (
        select(
            ProductionPlans.plan_id,
            wk_subq.c.workflow_id,
            Tissues.donor_id,
            Tissues.tissue_id,
        )
        .join(
            Tissues,
            Tissues.tissue_id == ProductionPlans.tissue_id,
        )
        .join(
            wk_subq,
            wk_subq.c.category_id == Tissues.category_id,
        )
        .where(
            Tissues.donor_id == donor_id,
            ProductionPlans.status == "approved",
        )
    )

    insert_stmt = (
        insert(Processes)
        .from_select(
            ["plan_id", "workflow_id", "donor_id", "tissue_id"],
            select_stmt,
        )
        .returning(Processes.plan_id)
    )

    result = await db.execute(insert_stmt)

    plan_ids = [row.plan_id for row in result]

    # 2. Update ProductionPlans status for those plan_ids
    # update_stmt = ( update(ProductionPlans).where(
    # ProductionPlans.plan_id.in_(plan_ids)).values(status="processed")
    # )
    # session.execute(update_stmt)
    await db.commit()
    # rows = result.mappings().all()
    # print(rows)
    return {"db: success"}


async def list_production_plans(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    donor_ids: list[int] = None,
):


    stmt = (
        select(
            *ProductionPlans.__table__.c,
            Products.name.label("product_name"),
            Products.base_dimensions.label("product_base_dimensions"),
            TissueCategories.name.label("category_name"),
            Tissues.bundle_details["type"].astext.label("tissue_type"),
        )
        .join(Products, ProductionPlans.product_id == Products.product_id)
        .join(TissueCategories, Products.category_id == TissueCategories.category_id)
        .join(Tissues, ProductionPlans.tissue_id == Tissues.tissue_id)
    )

    if status:
        stmt = stmt.where(ProductionPlans.status == status)

    if donor_ids:
        stmt = stmt.where(Tissues.donor_id.in_(donor_ids))

    stmt = stmt.offset(skip).limit(limit)

    result = await db.execute(stmt)
    return result.mappings().all()
