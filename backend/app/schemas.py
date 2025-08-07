# Defines data validation and serialization schemas (e.g., Pydantic)

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from enum import IntEnum


# ----- Enums -----
class ApplicationStatus(IntEnum):
    Applied = 1
    Interviewing = 2
    Offer = 3
    Rejected = 4
    Withdrawn = 5
    Archived = 6


class InteractionType(IntEnum):
    Email = 1
    Call = 2
    Interview = 3
    Event = 4
    Other = 5


class DocumentType(IntEnum):
    Resume = 1
    CoverLetter = 2
    Portfolio = 3


# ----- Base Config -----
class ConfigORM:
    class Config:
        orm_mode = True


# ----- User Schemas -----
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    github_link: Optional[str] = None
    linkedin_link: Optional[str] = None
    portfolio: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    github_link: Optional[str]
    linkedin_link: Optional[str]
    portfolio: Optional[str]


class UserRead(BaseModel, ConfigORM):
    user_id: int
    username: str
    email: EmailStr
    phone_number: Optional[str]
    github_link: Optional[str]
    linkedin_link: Optional[str]
    portfolio: Optional[str]
    created_at: datetime
    updated_at: datetime


# ----- Company Schemas -----
class CompanyCreate(BaseModel):
    company_name: str
    industry: Optional[str] = None
    website: Optional[str] = None


class CompanyUpdate(BaseModel):
    company_name: Optional[str]
    industry: Optional[str]
    website: Optional[str]


class CompanyRead(BaseModel, ConfigORM):
    company_id: int
    company_name: str
    industry: Optional[str]
    website: Optional[str]
    created_at: datetime
    updated_at: datetime


# ----- Document Schemas -----
class DocumentCreate(BaseModel):
    job_application_id: int
    document_type: DocumentType
    file_path: str


class DocumentRead(BaseModel, ConfigORM):
    document_id: int
    job_application_id: int
    document_type: DocumentType
    file_path: str
    upload_date: datetime
    created_at: datetime
    updated_at: datetime


# ----- Interaction Schemas -----
class InteractionCreate(BaseModel):
    job_application_id: int
    interaction_type: InteractionType
    interaction_date: Optional[datetime] = None
    notes: Optional[str] = None


class InteractionRead(BaseModel, ConfigORM):
    interaction_id: int
    job_application_id: int
    interaction_type: InteractionType
    interaction_date: datetime
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


# ----- Task Schemas -----
class TaskCreate(BaseModel):
    job_application_id: Optional[int] = None
    description: str
    due_date: Optional[datetime] = None
    completed: Optional[bool] = Field(default=False)
    notes: Optional[str] = None


class TaskRead(BaseModel, ConfigORM):
    task_id: int
    job_application_id: Optional[int]
    description: str
    due_date: Optional[datetime]
    completed: bool
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


# ----- JobApplication Schemas -----
class JobApplicationCreate(BaseModel):
    user_id: int
    company_id: int
    job_title: str
    application_status: ApplicationStatus
    application_date: Optional[datetime] = None
    job_board: Optional[str] = None
    job_link: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class JobApplicationUpdate(BaseModel):
    job_title: Optional[str]
    application_status: Optional[ApplicationStatus]
    application_date: Optional[datetime]
    job_board: Optional[str]
    job_link: Optional[str]
    location: Optional[str]
    notes: Optional[str]


class JobApplicationRead(BaseModel, ConfigORM):
    job_application_id: int
    user_id: int
    company_id: int
    job_title: str
    application_status: ApplicationStatus
    application_date: datetime
    job_board: Optional[str]
    job_link: Optional[str]
    location: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    # Optionally embed related entities (flatten later if needed)
    documents: List[DocumentRead] = []
    interactions: List[InteractionRead] = []
    tasks: List[TaskRead] = []
