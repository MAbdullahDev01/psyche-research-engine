from pydantic import BaseModel

class Params(BaseModel):
    query : str
    page : int
    per_page : int