from uuid import UUID

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import schema
from src.api.models import crud


async def test_query_not_exist(
    async_session: AsyncSession,
) -> None:
    with pytest.raises(HTTPException):
        await crud.query_get(
            async_session,
            UUID("00000000-0000-0000-0000-000000000000"),
        )


@pytest.mark.parametrize(
    ("region_id", "category_id", "query"),
    [
        (2, 3, "test"),
        (None, 3, "test"),
        (None, None, "test"),
        (None, None, None),
    ],
)
async def test_query_get(
    async_session: AsyncSession,
    region_id: int,
    category_id: int,
    query: str,
) -> None:
    query_id = (
        await crud.query_add(
            session=async_session,
            region_id=region_id,
            category_id=category_id,
            query=query,
        )
    ).query_id

    result: schema.QueryGet = await crud.query_get(async_session, query_id)

    assert result.query_id == query_id
    assert result.region_id == region_id
    assert result.category_id == category_id
    assert result.query == query
