from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.schemas.papers_schemas import PaperCreate, SavedPaper
from app.schemas.projects_schemas import Project, ProjectCreateInput, ProjectUpdateInput
from app.services.project_services import (
    add_paper_to_project_service,
    add_project,
    delete_a_project,
    get_project_by_id,
    list_papers_for_project,
    list_projects,
    remove_paper_from_project,
    update_a_project,
)
from app.services.user_services import get_current_user

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(
    input: ProjectCreateInput, user=Depends(get_current_user)
) -> Project:
    return add_project(input.title.strip(), input.question.strip(), user.payload["sub"])


@router.get("/", response_model=list[Project])
def list_all_projects(user=Depends(get_current_user)) -> list[Project]:
    return list_projects(user.payload["sub"])


@router.get("/{project_id}", response_model=Project)
def get_project(project_id: str, user=Depends(get_current_user)) -> Project:
    project = get_project_by_id(project_id, user.payload["sub"])
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    return project


@router.patch("/{project_id}", response_model=Project)
def update_project(
    input: ProjectUpdateInput, project_id: str, user=Depends(get_current_user)
) -> Project:
    project = update_a_project(
        input.title.strip(),
        input.question.strip(),
        project_id,
        user.payload["sub"],
    )
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, user=Depends(get_current_user)) -> Response:
    user_id = user.payload["sub"]
    if get_project_by_id(project_id, user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    delete_a_project(project_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{project_id}/papers", response_model=SavedPaper)
def add_paper_to_project(
    project_id: str,
    paper: PaperCreate,
    user=Depends(get_current_user),
) -> SavedPaper:
    return add_paper_to_project_service(project_id, paper, user.payload["sub"])


@router.get("/{project_id}/papers", response_model=list[SavedPaper])
def list_project_papers(
    project_id: str,
    user=Depends(get_current_user),
) -> list[SavedPaper]:
    if get_project_by_id(project_id, user.payload["sub"]) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    return list_papers_for_project(project_id)


@router.delete(
    "/{project_id}/papers/{paper_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_project_paper(
    project_id: str,
    paper_id: str,
    user=Depends(get_current_user),
) -> Response:
    if get_project_by_id(project_id, user.payload["sub"]) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    remove_paper_from_project(project_id, paper_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
