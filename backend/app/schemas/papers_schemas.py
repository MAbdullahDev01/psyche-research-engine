from pydantic import BaseModel, Field

class Paper(BaseModel):
    openalex_id: str
    title: str
    authors: list[str]
    publication_year: int | None = None
    abstract: str | None = None
    landing_page_url: str | None = None
    doi: str | None = None

class PaperCreate(Paper):
    pass

class PaperFilters(BaseModel):
    type: str = Field(min_length=1)
    from_publication_date: str = Field(min_length=10)

class Params(BaseModel):
    query: str = Field(min_length=1)
    page: int = Field(ge=1)
    per_page: int = Field(ge=1, le=100)
    filters : PaperFilters

class SavedPaper(BaseModel):
    id: str
    openalex_id: str
    title: str
    authors: list[str]
    publication_year: int | None = None
    abstract: str | None = None
    landing_page_url: str | None = None
    doi: str | None = None

class SearchPapersResponse(BaseModel):
    papers: list[Paper]
    page: int
    per_page: int
    total: int | None = None