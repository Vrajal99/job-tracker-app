from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    DateTime,
    Text,
    Boolean,
    Enum as PgEnum,
    ForeignKey,
    func,
)
from datetime import datetime
import enum

from database import Base

# ----- Mixins -----
class TimestampBaseMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

class SoftDeleteBaseMixin:
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)


# ----- Enums -----
class ApplicationStatus(enum.IntEnum):
    APPLIED = 1
    INTERVIEWING = 2
    OFFER = 3
    REJECTED = 4
    WITHDRAWN = 5
    ARCHIVED = 6


class InteractionType(enum.IntEnum):
    EMAIL = 1
    CALL = 2
    INTERVIEW = 3
    EVENT = 4
    OTHER = 5


class DocumentType(enum.IntEnum):
    RESUME = 1
    COVER_LETTER = 2
    PORTFOLIO = 3


# ----- Models -----
class User(Base, TimestampBaseMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    github_link: Mapped[str | None] = mapped_column(String(255), nullable=True)
    linkedin_link: Mapped[str | None] = mapped_column(String(255), nullable=True)
    portfolio: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    applications: Mapped[list["JobApplication"]] = relationship(
        "JobApplication", back_populates="user"
    )


class Company(Base, TimestampBaseMixin):
    __tablename__ = "companies"

    company_id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    industry: Mapped[str | None] = mapped_column(String(255), nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)

    applications: Mapped[list["JobApplication"]] = relationship(
        "JobApplication", back_populates="company"
    )


class JobApplication(Base, TimestampBaseMixin, SoftDeleteBaseMixin):
    __tablename__ = "job_applications"

    job_application_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.company_id"), nullable=False)

    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    application_status: Mapped[ApplicationStatus] = mapped_column(
        PgEnum(ApplicationStatus, name="application_status_enum"), nullable=False
    )
    application_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    job_board: Mapped[str | None] = mapped_column(String(255), nullable=True)
    job_link: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="applications")
    company: Mapped["Company"] = relationship("Company", back_populates="applications")
    documents: Mapped[list["Document"]] = relationship(
        "Document", back_populates="application", cascade="all, delete-orphan"
    )
    interactions: Mapped[list["Interaction"]] = relationship(
        "Interaction", back_populates="application", cascade="all, delete-orphan"
    )
    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="application", cascade="all, delete-orphan"
    )


class Document(Base, TimestampBaseMixin):
    __tablename__ = "documents"

    document_id: Mapped[int] = mapped_column(primary_key=True)
    job_application_id: Mapped[int] = mapped_column(
        ForeignKey("job_applications.job_application_id"), nullable=False
    )
    document_type: Mapped[DocumentType] = mapped_column(
        PgEnum(DocumentType, name="document_type_enum"), nullable=False
    )
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    upload_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    application: Mapped["JobApplication"] = relationship("JobApplication", back_populates="documents")


class Interaction(Base, TimestampBaseMixin):
    __tablename__ = "interactions"

    interaction_id: Mapped[int] = mapped_column(primary_key=True)
    job_application_id: Mapped[int] = mapped_column(
        ForeignKey("job_applications.job_application_id"), nullable=False
    )
    interaction_type: Mapped[InteractionType] = mapped_column(
        PgEnum(InteractionType, name="interaction_type_enum"), nullable=False
    )
    interaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    application: Mapped["JobApplication"] = relationship("JobApplication", back_populates="interactions")


class Task(Base, TimestampBaseMixin):
    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(primary_key=True)
    job_application_id: Mapped[int | None] = mapped_column(
        ForeignKey("job_applications.job_application_id"), nullable=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, server_default="false", nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    application: Mapped["JobApplication"] = relationship("JobApplication", back_populates="tasks")
