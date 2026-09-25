from app.core.config import settings

import httpx
def fetch_papers(params):

    query = params.query.rstrip("?!.")
    openalex_params = {
        "search": query,
        "page": params.page,
        "per-page": params.per_page,
    }
    with httpx.Client() as client:
        response = client.get(
            "https://api.openalex.org/works",
            params=openalex_params
        )
    print(response)
    print(response.status_code)
    print(response.text)
    return response.json()