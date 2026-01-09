import datetime
import decimal
from typing import Optional, Text

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKeyConstraint,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Enum

from app.db.base_class import Base


class Processes(Base):
    __tablename__ = "processes"
    __table_args__ = (
        ForeignKeyConstraint(
            ["donor_id"], ["donors.donor_id"], name="processes_donor_id_fkey"
        ),
        ForeignKeyConstraint(
            ["plan_id"], ["production_plans.plan_id"], name="processes_plan_id_fkey"
        ),
        # ForeignKeyConstraint(
        #     ["room_assignment_id"],
        #     ["room_assignments.assignment_id"],
        #     name="processes_room_assignment_id_fkey",
        # ),
        ForeignKeyConstraint(
            ["tissue_id"], ["tissues.tissue_id"], name="processes_tissue_id_fkey"
        ),
        ForeignKeyConstraint(
            ["workflow_id"],
            ["workflows.workflow_id"],
            name="processes_workflow_id_fkey",
        ),
        PrimaryKeyConstraint("process_id", name="processes_pkey"),
    )

    process_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_id: Mapped[Optional[int]] = mapped_column(Integer)
    # room_assignment_id: Mapped[Optional[int]] = mapped_column(Integer)
    workflow_id: Mapped[Optional[int]] = mapped_column(Integer)
    donor_id: Mapped[Optional[int]] = mapped_column(Integer)
    tissue_id: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(
        Enum(
            "planned",
            "in_progress",
            "completed",
            "deviated",
            name="process_status_enum",
        ),
        server_default=text("'planned'::process_status_enum"),
    )
    start_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    end_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    # donor: Mapped[Optional["Donors"]] = relationship(
    #     "Donors", back_populates="processes"
    # )
    # plan: Mapped[Optional["ProductionPlans"]] = relationship(
    #     "ProductionPlans", back_populates="processes"
    # )
    # room_assignment: Mapped[Optional["RoomAssignments"]] = relationship(
    #     "RoomAssignments", foreign_keys=[room_assignment_id], back_populates="processes"
    # )
    # tissue: Mapped[Optional["Tissues"]] = relationship(
    #     "Tissues", back_populates="processes"
    # )
    # workflow: Mapped[Optional["Workflows"]] = relationship(
    #     "Workflows", back_populates="processes"
    # )
    # room_assignments: Mapped[Optional["RoomAssignments"]] = relationship(
    #     "RoomAssignments",
    #     uselist=False,
    #     foreign_keys="[RoomAssignments.process_id]",
    #     back_populates="process",
    # )
    # process_comments: Mapped[list["ProcessComments"]] = relationship(
    #     "ProcessComments", back_populates="process"
    # )
    # verifications: Mapped[list["Verifications"]] = relationship(
    #     "Verifications", back_populates="process"
    # )
    # workflow_steps: Mapped[list["WorkflowSteps"]] = relationship(
    #     "WorkflowSteps", back_populates="process"
    # )


class ProcessComments(Base):
    __tablename__ = "process_comments"
    __table_args__ = (
        ForeignKeyConstraint(
            ["process_id"],
            ["processes.process_id"],
            name="process_comments_process_id_fkey",
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["technicians.technician_id"],
            name="process_comments_user_id_fkey",
        ),
        PrimaryKeyConstraint("comment_id", name="process_comments_pkey"),
    )

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    process_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    comment_text: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    # process: Mapped[Optional["Processes"]] = relationship(
    #     "Processes", back_populates="process_comments"
    # )
    # user: Mapped[Optional["Technicians"]] = relationship(
    #     "Technicians", back_populates="process_comments"
    # )


class WorkflowStepTemplates(Base):
    __tablename__ = "workflow_step_templates"
    __table_args__ = (
        ForeignKeyConstraint(
            ["workflow_id"],
            ["workflows.workflow_id"],
            name="workflow_step_templates_workflow_id_fkey",
        ),
        PrimaryKeyConstraint("template_step_id", name="workflow_step_templates_pkey"),
    )

    template_step_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    step_num: Mapped[int] = mapped_column(Integer, nullable=False)
    workflow_id: Mapped[Optional[int]] = mapped_column(Integer)
    section: Mapped[Optional[str]] = mapped_column(String(50))
    action: Mapped[Optional[str]] = mapped_column(Text)

    # workflow: Mapped[Optional["Workflows"]] = relationship(
    #     "Workflows", back_populates="workflow_step_templates"
    # )


class Workflows(Base):
    __tablename__ = "workflows"
    __table_args__ = (
        ForeignKeyConstraint(
            ["category_id"],
            ["tissue_categories.category_id"],
            name="workflows_category_id_fkey",
        ),
        PrimaryKeyConstraint("workflow_id", name="workflows_pkey"),
    )

    workflow_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[Optional[int]] = mapped_column(Integer)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    template_json: Mapped[Optional[dict]] = mapped_column(JSONB)
    version: Mapped[Optional[str]] = mapped_column(String(10))
    is_active: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text("true")
    )

    # processes: Mapped[list["Processes"]] = relationship(
    #     "Processes", back_populates="workflow"
    # )
    # category: Mapped[Optional["TissueCategories"]] = relationship(
    #     "TissueCategories", back_populates="workflows"
    # )
    # workflow_step_templates: Mapped[list["WorkflowStepTemplates"]] = relationship(
    #     "WorkflowStepTemplates", back_populates="workflow"
    # )


class WorkflowSteps(Base):
    __tablename__ = "workflow_steps"
    __table_args__ = (
        ForeignKeyConstraint(
            ["process_id"],
            ["processes.process_id"],
            name="workflow_steps_process_id_fkey",
        ),
        PrimaryKeyConstraint("step_id", name="workflow_steps_pkey"),
    )

    step_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    process_id: Mapped[Optional[int]] = mapped_column(Integer)
    step_num: Mapped[Optional[int]] = mapped_column(Integer)
    initials: Mapped[Optional[str]] = mapped_column(String(10))
    verified_by_initials: Mapped[Optional[str]] = mapped_column(String(10))
    spin_program: Mapped[Optional[str]] = mapped_column(String(20))
    spin_count: Mapped[Optional[int]] = mapped_column(Integer)
    actual_duration: Mapped[Optional[str]] = mapped_column(String(20))
    temp_start: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    temp_stop: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    temp_compliant: Mapped[Optional[bool]] = mapped_column(Boolean)
    na_performed: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text("false")
    )
    deviation_notes: Mapped[Optional[str]] = mapped_column(Text)
    start_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    # process: Mapped[Optional["Processes"]] = relationship(
    #     "Processes", back_populates="workflow_steps"
    # )
