from pydantic import BaseModel

class PaperFilters(BaseModel):
    type: str
    from_publication_date: str

class Params(BaseModel):
    query : str
    page : int
    per_page : int
    filters : PaperFilters