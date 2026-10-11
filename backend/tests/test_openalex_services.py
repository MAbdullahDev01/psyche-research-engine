from app.schemas.papers_schemas import Params, PaperFilters
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
    import pytest

    with pytest.raises(ValidationError):
        Params(
            query="robotics",
            page=0,
            per_page=20,
            filters=PaperFilters(type="article", from_publication_date="2025-01-01"),
        )
