from fastapi import APIRouter, Depends

from app.schemas.projects_schemas import ProjectCreateInput, ProjectUpdateInput
from app.services.project_services import add_project,delete_a_project, get_project_by_id, list_projects, update_a_project 
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
    return {"message": "Project created successfully."}

@router.get("/")
def list_all_projects(user = Depends(get_current_user)) -> list:
    user_id = user.payload["sub"]
    projects = list_projects(user_id)
    return projects

@router.get("/{project_id}")
def get_project(project_id: str, user = Depends(get_current_user)):
    try:
        user_id = user.payload["sub"]
        project = get_project_by_id(project_id, user_id)
        if project is None:
            return {"error": "Project not found."}
        return project
    except Exception as e:
        print(f"Error retrieving project: {e}")
        return {"error": "Failed to retrieve project."}

@router.patch("/{project_id}")
def update_project(input : ProjectUpdateInput, project_id: str, user = Depends(get_current_user)):
    try:
        user_id = user.payload["sub"]
        update_a_project(input.title, input.question, project_id, user_id)
        updated_project = get_project_by_id(project_id, user_id)
        if updated_project is None:
            return {"error": "Project not found."}
        return updated_project
    except Exception as e:
            print(f"Error retrieving project: {e}")
            return {"error": "Failed to update project."}

@router.delete("/{project_id}")
def delete_project(project_id: str, user = Depends(get_current_user)) -> dict[str, str]:
    try:
            user_id = user.payload["sub"]
            project = get_project_by_id(project_id, user_id)
            if project is None:
                return {"error": "Project not found."}
            delete_a_project(project_id, user_id)
            return {"message": "Project deleted successfully."}
    except Exception as e:
        print(f"Error retrieving project: {e}")
        return {"error": "Failed to delete project."}