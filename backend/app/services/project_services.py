from fastapi import HTTPException

from app.db.supabase import supabase
from app.schemas.papers_schemas import PaperCreate, SavedPaper
from app.schemas.projects_schemas import Project

def add_project(title : str, question : str, user_id : str) -> Project:
    try:
        response = (
            supabase.table("projects")
            .insert(
                {
                    "user_id": user_id,
                    "title": title,
                    "question": question,
                }
            )
            .execute()
        )
        print(response)
    except Exception as e:
        # Error logging for debugging purposes
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to create project"
        )
    return Project(**response.data[0])

def get_project_by_id(project_id: str, user_id: str) -> Project | None:
    try:
        response = (
            supabase.table("projects")
            .select("*")
            .eq("id", project_id)
            .eq("user_id", user_id)
            .execute()
        )
        if response.data:
            return Project(**response.data[0])
        else:
            return None
    except Exception as e:
        # Error logging for debugging purposes
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to get project"
        )

def list_projects(user_id: str) -> list[Project]:
    try:
        response = (
            supabase.table("projects")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return [Project(**item) for item in response.data]
    except Exception as e:
        # Error logging for debugging purposes
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to list projects"
        )

def update_a_project(title: str, question : str, project_id : str, user_id : str) -> Project:
    try:
        response = (
            supabase.table("projects")
            .update(
                {
                "title": title,
                "question" : question,
                }
            )
            .eq("id", project_id)
            .eq("user_id", user_id)
            .execute()
        )
    except Exception as e:
        # Error logging for debugging purposes
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to update project"
        )

    return Project(**response.data[0])

def delete_a_project(project_id : str, user_id : str):
    try:
            response = (
                supabase.table("projects")
                .delete()
                .eq("id", project_id)
                .eq("user_id", user_id)
                .execute()
            )
    except Exception as e:
        # Error logging for debugging purposes
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to delete project"
        )

def add_paper_to_project_service(
    project_id: str,
    paper: PaperCreate,
    user_id: str
) -> SavedPaper:
    try:
        # 1. Make sure project exists and belongs to user
        project = get_project_by_id(project_id, user_id)

        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )

        # 2. Check whether paper already exists
        existing_paper = (
            supabase
            .table("papers")
            .select("*")
            .eq("openalex_id", paper.openalex_id)
            .execute()
        )

        if existing_paper.data:
            paper_row = existing_paper.data[0]

        else:
            # 3. Create paper
            new_paper = (
                supabase
                .table("papers")
                .insert({
                    "openalex_id": paper.openalex_id,
                    "title": paper.title,
                    "authors": paper.authors,
                    "publication_year": paper.publication_year,
                    "abstract": paper.abstract,
                    "landing_page_url": paper.landing_page_url,
                    "doi": paper.doi,
                })
                .select("*")
                .execute()
            )

            print("new_paper:", new_paper)
            print("new_paper.data:", new_paper.data)

            paper_row = new_paper.data[0]
        paper_id = paper_row["id"]

        supabase.table("project_papers").upsert(
            {
                "project_id": project_id,
                "paper_id": paper_id,
            },
            on_conflict="project_id,paper_id",
            ignore_duplicates=True,
        ).execute()

        return _saved_paper_from_row(paper_row)

    except HTTPException:
        raise

    except Exception as e:
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to add paper to project"
        )


def list_papers_for_project(project_id: str) -> list[SavedPaper]:
    try:
        response = (
            supabase
            .table("project_papers")
            .select("papers(id, openalex_id, title, authors, publication_year, abstract, landing_page_url, doi)")
            .eq("project_id", project_id)
            .execute()
        )
        return [
            _saved_paper_from_row(row["papers"])
            for row in response.data
            if isinstance(row.get("papers"), dict)
        ]
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to list papers for project"
        )


def remove_paper_from_project(project_id: str, paper_id: str) -> None:
    try:
        existing_link = (
            supabase
            .table("project_papers")
            .select("project_id")
            .eq("project_id", project_id)
            .eq("paper_id", paper_id)
            .maybe_single()
            .execute()
        )
        if not existing_link.data:
            raise HTTPException(status_code=404, detail="Saved paper not found")

        (
            supabase
            .table("project_papers")
            .delete()
            .eq("project_id", project_id)
            .eq("paper_id", paper_id)
            .execute()
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to remove paper from project"
        )


def _saved_paper_from_row(row: dict) -> SavedPaper:
    return SavedPaper(
        id=str(row["id"]),
        openalex_id=row["openalex_id"],
        title=row["title"],
        authors=row.get("authors") or [],
        publication_year=row.get("publication_year"),
        abstract=row.get("abstract"),
        landing_page_url=row.get("landing_page_url"),
        doi=row.get("doi"),
    )