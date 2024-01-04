from typing import TypeVar

from sqlalchemy import event
from sqlalchemy.orm import DeclarativeBase, configure_mappers, declared_attr

from .mixin import MixinID, MixinTimeStamp


class Base(DeclarativeBase):
    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseModel(Base, MixinID, MixinTimeStamp):
    __abstract__ = True

    @classmethod
    def __declare_last__(cls) -> None:
        super().__declare_last__()


TBaseModel = TypeVar("TBaseModel", bound=BaseModel)


@event.listens_for(Base.metadata, "before_create")
def _configure_mappers() -> None:  # *args, **kwargs
    configure_mappers()
