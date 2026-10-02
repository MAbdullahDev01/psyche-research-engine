from enum import Enum
from pydantic import BaseModel, Field

class ProjectCreateInput(BaseModel):
    title: str = Field(min_length=1)
    question: str = Field(min_length=1)

class ProjectUpdateInput(BaseModel):
    title : str
    question : str

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