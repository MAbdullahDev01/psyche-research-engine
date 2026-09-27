from fastapi import APIRouter, Depends

from app.schemas.papers_schemas import Params, SearchPapersResponse
from app.services.openalex_services import fetch_papers
from app.services.user_services import get_current_user

router = APIRouter(prefix="/api/papers", tags=["papers"])

@router.post("/search/papers")
def search_papers(
    params: Params,
    user=Depends(get_current_user),
) -> SearchPapersResponse:
    return fetch_papers(params)