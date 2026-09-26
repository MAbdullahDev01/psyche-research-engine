from app.core.config import settings

import httpx
import re

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

def fetch_papers(params):

    query = _clean_query(params.query)

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

    with httpx.Client() as client:
        response = client.get(
            "https://api.openalex.org/works",
            params=openalex_params
        )

    return response.json()

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