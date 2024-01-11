from uuid import UUID

from pydantic import AliasChoices, BaseModel, Field


class AddIn(BaseModel):
    region_id: int | None = Field(description="region id")
    category_id: int | None = Field(description="category id")
    query: str | None = Field(description="search query")


class AddOut(BaseModel):
    query_id: UUID = Field(validation_alias=AliasChoices("query_id", "id"))


class AddGet(AddIn, AddOut):
    pass


class StatIn(BaseModel):
    query_id: UUID


class StatOut(BaseModel):
    timestamp: float = Field()
    value: int = Field()


class Message(BaseModel):
    detail: str
