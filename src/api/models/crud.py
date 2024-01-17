from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import models, schema


async def query_add(
    session: AsyncSession,
    region_id: int | None = None,
    category_id: int | None = None,
    query: str | None = "",
) -> schema.QueryOut:
    db_obj = models.Query(
        region_id=region_id,
        category_id=category_id,
        query=query,
    )
    try:
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'The query "region_id={region_id} category_id={category_id} query={query}" is duplicated',
        )
    except DatabaseError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="DB error while creating",
        )

    return schema.QueryGet.model_validate(db_obj.__dict__)


async def query_get(
    session: AsyncSession,
    query_id: UUID,
) -> schema.QueryGet:
    db_obj: models.Query | None
    db_obj = await session.get(models.Query, query_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'The query with id "{query_id}" not found',
        )
    return schema.QueryGet.model_validate(db_obj.__dict__)


async def stats_get(
    session: AsyncSession,
    query_id: UUID,
) -> list[schema.StatOut]:
    _ = await query_get(session, query_id)

    query = (
        select(
            models.Stat.timestamp,
            models.Stat.value,
        )
        .where(models.Stat.query_id == query_id)
        .order_by(models.Stat.timestamp)
    )

    try:
        result = await session.execute(query)
    except DatabaseError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="DB error",
        )

    return [
        schema.StatOut.model_validate(
            {
                "timestamp": db_obj.timestamp,
                "value": db_obj.value,
            },
        )
        for db_obj in result
    ]
