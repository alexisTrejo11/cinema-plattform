from pydantic import BaseModel

class PaginationParams(BaseModel):
    offset: int = 0
    limit: int = 10
