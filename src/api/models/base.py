from typing import TypeVar

from sqlalchemy import UniqueConstraint, event
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import DeclarativeBase, configure_mappers, declared_attr

from .mixin import MixinID, MixinTimeStamp

UniqueConstraint.argument_for("postgresql", "nulls_not_distinct", None)


@compiles(UniqueConstraint, "postgresql")
def compile_create_uc(create, compiler, **kw):  # noqa: ANN001, ANN003, ANN201
    """Add NULLS NOT DISTINCT if its in args."""
    stmt = compiler.visit_unique_constraint(create, **kw)
    postgresql_opts = create.dialect_options["postgresql"]

    if postgresql_opts.get("nulls_not_distinct"):
        return stmt.rstrip().replace("UNIQUE (", "UNIQUE NULLS NOT DISTINCT (")
    return stmt


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
def _configure_mappers(*args, **kwargs) -> None:  # noqa: ANN002, ANN003, U100
    configure_mappers()
