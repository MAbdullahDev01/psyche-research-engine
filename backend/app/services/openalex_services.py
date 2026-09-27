import re

import httpx
from fastapi import HTTPException, status

from app.schemas.papers_schemas import Paper, Params, SearchPapersResponse

STOP_WORDS = {
    "what",
    "are",
    "is",
    "the",
    "of",
    "in",
    "on",
    "how",
    "why",
    "when",
    "where",
    "can",
    "do",
    "does",
    "used",
    "using",
    "for",
    "to",
    "a",
    "an",
}

def fetch_papers(params: Params) -> SearchPapersResponse:

    query = _clean_query(params.query)
    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query must contain at least one searchable term.",
        )

    filters = ",".join(
        f"{key}:{value}"
        for key, value in params.filters.model_dump().items()
    )

    openalex_params = {
        "search": query,
        "page": params.page,
        "per-page": params.per_page,
        "filter": filters,
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(
                "https://api.openalex.org/works",
                params=openalex_params,
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="OpenAlex rejected the paper search request.",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAlex is unavailable. Please try again.",
        ) from exc

    payload = response.json()
    return SearchPapersResponse(
        papers=[map_openalex_work(work) for work in payload.get("results", [])],
        page=params.page,
        per_page=params.per_page,
        total=payload.get("meta", {}).get("count"),
    )


def map_openalex_work(work: dict) -> Paper:
    authorships = work.get("authorships")
    authors = [
        author_name
        for authorship in (authorships if isinstance(authorships, list) else [])
        if isinstance(authorship, dict)
        and isinstance(authorship.get("author"), dict)
        and isinstance(
            author_name := authorship.get("author", {}).get("display_name"),
            str,
        )
        and author_name
    ]
    abstract_inverted_index = work.get("abstract_inverted_index")
    abstract = None
    if isinstance(abstract_inverted_index, dict):
        words_by_position = [
            (position, word)
            for word, positions in abstract_inverted_index.items()
            if isinstance(word, str)
            if isinstance(positions, list)
            for position in positions
            if isinstance(position, int)
        ]
        abstract = " ".join(
            word
            for _, word in sorted(words_by_position, key=lambda item: item[0])
        ) or None

    primary_location = work.get("primary_location")
    landing_page_url = (
        primary_location.get("landing_page_url")
        if isinstance(primary_location, dict)
        else None
    )
    return Paper(
        openalex_id=work.get("id", ""),
        title=work.get("display_name", ""),
        authors=authors,
        publication_year=work.get("publication_year"),
        abstract=abstract,
        landing_page_url=landing_page_url,
        doi=work.get("doi"),
    )

def _clean_query(query: str) -> str:
    query = query.lower()
    query = re.sub(r"[^\w\s]", "", query)

    words = query.split()

    keywords = [
        word
        for word in words
        if word not in STOP_WORDS
    ]

    return " ".join(keywords)