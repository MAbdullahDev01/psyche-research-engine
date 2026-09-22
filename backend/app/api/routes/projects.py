from fastapi import APIRouter, Depends

from app.services.project_services import add_project
from app.schemas.projects_schemas import ProjectCreateInput
from app.services.user_services import get_current_user

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.post("/")
def create_project(input: ProjectCreateInput, user = Depends(get_current_user)):
    try:
        user_id = user.payload["sub"]
        title = input.title
        question = input.question
        add_project(title, question, user_id)

    except Exception as e:
        print(f"Error creating project: {e}")
        return {"error": "Failed to create project."}
    print(f"Creating project with title: {input.title} and question: {input.question}")
    return {"message": "Project created successfully."}