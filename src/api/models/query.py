from sqlalchemy import Column, Integer, String, UniqueConstraint

from .base import BaseModel


class Query(BaseModel):
    region_id = Column(Integer, nullable=True)
    category_id = Column(Integer, nullable=True)
    query = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "region_id",
            "category_id",
            "query",
            postgresql_nulls_not_distinct=True,
            name="uc_query",
        ),
    )
