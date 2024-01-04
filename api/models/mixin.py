from typing import Any, ClassVar
from uuid import uuid4

from sqlalchemy import DDL, Column, DateTime, FromClause, event, func
from sqlalchemy.dialects.postgresql import UUID


class Mixin:  # for mypy
    __table__: ClassVar[FromClause]
    __tablename__: Any


class MixinID(Mixin):
    id = Column(  # noqa A003
        UUID(as_uuid=True),
        server_default=func.gen_random_uuid(),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )


class MixinTimeStamp(Mixin):
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
    )

    @classmethod
    def __create_func_for_update_at(cls) -> None:
        func_ddl = DDL(
            """DO $$
            BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'refresh_updated_at') THEN
                CREATE FUNCTION public.refresh_updated_at()
                RETURNS TRIGGER
                LANGUAGE plpgsql NOT LEAKPROOF AS
                $BODY$
                    BEGIN
                       NEW.updated_at := now();
                        RETURN NEW;
                    END
                $BODY$;
            END IF;
        END;
        $$;
        """,
        )
        event.listen(cls.__table__, "before_create", func_ddl)

    @classmethod
    def __create_trigger_for_table(cls) -> None:
        trig_ddl = DDL(
            f"""
                    CREATE TRIGGER tr_{cls.__tablename__}_updated_at BEFORE UPDATE
                    ON {cls.__tablename__}
                    FOR EACH ROW EXECUTE PROCEDURE
                    refresh_updated_at();
                """,
        )
        event.listen(cls.__table__, "after_create", trig_ddl)

    #
    @classmethod
    def __declare_last__(cls) -> None:
        cls.__create_func_for_update_at()
        cls.__create_trigger_for_table()
