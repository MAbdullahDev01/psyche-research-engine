from pydantic import BaseModel, Field

class ProjectCreateInput(BaseModel):
    title: str = Field(min_length=1)
    question: str = Field(min_length=1)

class ProjectUpdateInput(BaseModel):
    title : str
    question : str