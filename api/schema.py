from uuid import UUID

from pydantic import BaseModel, Field


class AddIn(BaseModel):
    region_id: int | None = Field(description="region id")
    category_id: int | None = Field(description="category id")
    query: str | None = Field(description="search query")


class AddOut(BaseModel):
    query_id: UUID


class StatIn(BaseModel):
    query_id: UUID


class StatOut(BaseModel):
    timestamp: float = Field()
    value: int = Field()


class Message(BaseModel):
    detail: str
