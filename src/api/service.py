from uuid import UUID

from fastapi import BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import schema
from src.api.database import get_db
from src.api.models import crud


class Service:
    def __init__(
        self,
        session: AsyncSession = Depends(get_db),
        background_tasks: BackgroundTasks = BackgroundTasks(),
    ) -> None:
        self.session = session
        self.background_tasks = background_tasks

    async def add(
        self,
        query: schema.QueryIn,
    ) -> schema.QueryOut:
        return await crud.query_add(
            self.session,
            query.region_id,
            query.category_id,
            query.query,
        )

    async def stat(
        self,
        obj_id: UUID,
    ) -> list[schema.StatOut]:
        return await crud.stats_get(
            self.session,
            obj_id,
        )
