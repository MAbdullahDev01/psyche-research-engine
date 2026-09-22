from pydantic import BaseModel

class ProjectCreateInput(BaseModel):
    title: str
    question: str