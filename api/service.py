from uuid import UUID

from fastapi import BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api import schema
from api.database import get_db
from api.models import crud


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
        query: schema.AddIn,
    ) -> schema.AddOut:
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
