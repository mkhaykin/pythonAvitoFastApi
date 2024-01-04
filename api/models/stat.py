from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseModel


class Stat(BaseModel):
    query_id = Column(
        UUID(as_uuid=True),
        ForeignKey("query.id", ondelete="CASCADE"),
        nullable=False,
    )

    timestamp = Column(Numeric(precision=10, scale=2, asdecimal=True, decimal_return_scale=None))

    value = Column(
        Integer,
        nullable=False,
    )
