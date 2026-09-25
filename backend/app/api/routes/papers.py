from fastapi import APIRouter

from app.schemas.papers_schemas import Params
from app.services.openalex_services import fetch_papers

router = APIRouter(prefix="/api/papers", tags=["papers"])

@router.post("/search/papers")
def search_papers(params : Params):
    return fetch_papers(params)