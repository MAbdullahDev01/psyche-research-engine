from unittest.mock import Mock

import httpx
import pytest
from fastapi import HTTPException

from app.schemas.papers_schemas import Params, PaperFilters
from app.services import openalex_services
from app.services.openalex_services import _clean_query, map_openalex_work


def test_clean_query_removes_question_words_and_punctuation():
    assert _clean_query("What are the applications of RL in robotics?") == "applications rl robotics"


def test_map_openalex_work_normalizes_authors_abstract_and_urls():
    work = {
        "id": "https://openalex.org/W123",
        "display_name": "Reinforcement learning in robotics",
        "publication_year": 2025,
        "doi": "https://doi.org/10.0000/example",
        "authorships": [
            {"author": {"display_name": "Ada Researcher"}},
            {"author": {"display_name": "Alan Scientist"}},
            {"author": {}},
        ],
        "abstract_inverted_index": {"robotics": [2], "Learning": [0], "in": [1]},
        "primary_location": {"landing_page_url": "https://example.org/paper"},
    }

    paper = map_openalex_work(work)

    assert paper.openalex_id == "https://openalex.org/W123"
    assert paper.authors == ["Ada Researcher", "Alan Scientist"]
    assert paper.abstract == "Learning in robotics"
    assert paper.landing_page_url == "https://example.org/paper"


def test_search_parameters_schema_rejects_invalid_pagination():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        Params(
            query="robotics",
            page=0,
            per_page=20,
            filters=PaperFilters(type="article", from_publication_date="2025-01-01"),
        )


def test_fetch_papers_sends_openalex_search_and_filters(monkeypatch):
    params = Params(
        query="How are neural networks used in robotics?",
        page=2,
        per_page=15,
        filters=PaperFilters(type="article", from_publication_date="2024-01-01"),
    )
    response = Mock()
    response.json.return_value = {
        "meta": {"count": 1},
        "results": [{"id": "https://openalex.org/W1", "display_name": "Robotics", "authorships": []}],
    }
    response.raise_for_status.return_value = None

    class FakeClient:
        def __init__(self, timeout):
            assert timeout == 10.0

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def get(self, url, params):
            assert url == "https://api.openalex.org/works"
            assert params["search"] == "neural networks robotics"
            assert params["page"] == 2
            assert params["per-page"] == 15
            assert params["filter"] == "type:article,from_publication_date:2024-01-01"
            return response

    monkeypatch.setattr(openalex_services.httpx, "Client", FakeClient)
    result = openalex_services.fetch_papers(params)

    assert result.total == 1
    assert result.page == 2
    assert result.papers[0].title == "Robotics"


def test_fetch_papers_maps_upstream_network_errors_to_503(monkeypatch):
    params = Params(
        query="robotics",
        page=1,
        per_page=20,
        filters=PaperFilters(type="article", from_publication_date="2025-01-01"),
    )

    class FakeClient:
        def __init__(self, timeout):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def get(self, url, params):
            request = httpx.Request("GET", url)
            raise httpx.ConnectError("network unavailable", request=request)

    monkeypatch.setattr(openalex_services.httpx, "Client", FakeClient)
    with pytest.raises(HTTPException) as exc:
        openalex_services.fetch_papers(params)

    assert exc.value.status_code == 503


def test_fetch_papers_rejects_malformed_upstream_json(monkeypatch):
    params = Params(
        query="robotics",
        page=1,
        per_page=20,
        filters=PaperFilters(type="article", from_publication_date="2025-01-01"),
    )
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.side_effect = ValueError("not json")

    class FakeClient:
        def __init__(self, timeout):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def get(self, url, params):
            return response

    monkeypatch.setattr(openalex_services.httpx, "Client", FakeClient)
    with pytest.raises(HTTPException) as exc:
        openalex_services.fetch_papers(params)

    assert exc.value.status_code == 502
