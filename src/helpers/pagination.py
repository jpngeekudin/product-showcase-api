from pydantic import BaseModel, Field
from fastapi import Query


class Pagination(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1)
    sort: int | None = None
    skip: int


def get_pagination(page: int = Query(1), limit: int = Query(10), sort: str | None = None) -> Pagination:
    return Pagination(page=page, limit=limit, sort=sort, skip=(page - 1) * limit)
