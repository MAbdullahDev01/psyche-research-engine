from enum import Enum

from pydantic import BaseModel, Field, field_validator


class ProjectCreateInput(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    question: str = Field(min_length=1, max_length=2000)

    @field_validator("title", "question", mode="before")
    @classmethod
    def strip_required_text(cls, value):
        return value.strip() if isinstance(value, str) else value


class ProjectUpdateInput(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    question: str = Field(min_length=1, max_length=2000)

    @field_validator("title", "question", mode="before")
    @classmethod
    def strip_required_text(cls, value):
        return value.strip() if isinstance(value, str) else value


class ProjectStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"


class Project(BaseModel):
    id: str
    title: str
    question: str
    status: ProjectStatus = ProjectStatus.DRAFT
    created_at: str
    updated_at: str
