from fastapi import HTTPException, status

from app.db.supabase import supabase
from app.schemas.papers_schemas import PaperCreate, SavedPaper
from app.schemas.projects_schemas import Project


def add_project(title: str, question: str, user_id: str) -> Project:
    try:
        response = (
            supabase.table("projects")
            .insert({"user_id": user_id, "title": title, "question": question})
            .execute()
        )
        if not response.data:
            raise RuntimeError("Project insert returned no row.")
        return Project(**response.data[0])
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project.",
        ) from exc


def get_project_by_id(project_id: str, user_id: str) -> Project | None:
    try:
        response = (
            supabase.table("projects")
            .select("*")
            .eq("id", project_id)
            .eq("user_id", user_id)
            .execute()
        )
        return Project(**response.data[0]) if response.data else None
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get project.",
        ) from exc


def list_projects(user_id: str) -> list[Project]:
    try:
        response = supabase.table("projects").select("*").eq("user_id", user_id).execute()
        return [Project(**item) for item in response.data]
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list projects.",
        ) from exc


def update_a_project(
    title: str, question: str, project_id: str, user_id: str
) -> Project | None:
    try:
        response = (
            supabase.table("projects")
            .update({"title": title, "question": question})
            .eq("id", project_id)
            .eq("user_id", user_id)
            .execute()
        )
        return Project(**response.data[0]) if response.data else None
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update project.",
        ) from exc


def delete_a_project(project_id: str, user_id: str) -> None:
    try:
        supabase.table("projects").delete().eq("id", project_id).eq("user_id", user_id).execute()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete project.",
        ) from exc


def add_paper_to_project_service(
    project_id: str, paper: PaperCreate, user_id: str
) -> SavedPaper:
    project = get_project_by_id(project_id, user_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    try:
        existing = (
            supabase.table("papers").select("*").eq("openalex_id", paper.openalex_id).execute()
        )
        if existing.data:
            paper_row = existing.data[0]
        else:
            try:
                inserted = (
                    supabase.table("papers")
                    .insert(
                        {
                            "openalex_id": paper.openalex_id,
                            "title": paper.title,
                            "authors": paper.authors,
                            "publication_year": paper.publication_year,
                            "abstract": paper.abstract,
                            "landing_page_url": paper.landing_page_url,
                            "doi": paper.doi,
                        }
                    )
                    .select("*")
                    .execute()
                )
                if not inserted.data:
                    raise RuntimeError("Paper insert returned no row.")
                paper_row = inserted.data[0]
            except Exception:
                # Another request may have inserted the globally unique OpenAlex work
                # between the lookup and insert. Re-read before treating it as a failure.
                raced = (
                    supabase.table("papers")
                    .select("*")
                    .eq("openalex_id", paper.openalex_id)
                    .execute()
                )
                if not raced.data:
                    raise
                paper_row = raced.data[0]

        supabase.table("project_papers").upsert(
            {"project_id": project_id, "paper_id": paper_row["id"]},
            on_conflict="project_id,paper_id",
            ignore_duplicates=True,
        ).execute()
        return _saved_paper_from_row(paper_row)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add paper to project.",
        ) from exc


def list_papers_for_project(project_id: str) -> list[SavedPaper]:
    try:
        response = (
            supabase.table("project_papers")
            .select("papers(id, openalex_id, title, authors, publication_year, abstract, landing_page_url, doi)")
            .eq("project_id", project_id)
            .execute()
        )
        return [
            _saved_paper_from_row(row["papers"])
            for row in response.data
            if isinstance(row.get("papers"), dict)
        ]
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list papers for project.",
        ) from exc


def remove_paper_from_project(project_id: str, paper_id: str) -> None:
    try:
        existing = (
            supabase.table("project_papers")
            .select("project_id")
            .eq("project_id", project_id)
            .eq("paper_id", paper_id)
            .maybe_single()
            .execute()
        )
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Saved paper not found."
            )
        (
            supabase.table("project_papers")
            .delete()
            .eq("project_id", project_id)
            .eq("paper_id", paper_id)
            .execute()
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove paper from project.",
        ) from exc


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
