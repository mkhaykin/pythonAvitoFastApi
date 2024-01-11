import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .test_utils import query_add


@pytest.mark.parametrize(
    ("region_id", "category_id", "query"),
    [
        (2, 3, "test"),
        (None, 3, "test"),
        (None, None, "test"),
        (None, None, None),
    ],
)
async def test_query_add(
    async_session: AsyncSession,
    region_id: int,
    category_id: int,
    query: str,
) -> None:
    await query_add(async_session, region_id, category_id, query)


@pytest.mark.parametrize(
    ("region_id", "category_id", "query"),
    [
        (2, 3, "test"),
        (None, 3, "test"),
        (None, None, "test"),
        (None, None, None),
    ],
)
async def test_query_add_duplicate(
    region_id: int,
    category_id: int,
    query: str,
    async_session: AsyncSession,
    clear_tables: None,  # noqa: U100
) -> None:
    await query_add(async_session, region_id, category_id, query)
    with pytest.raises(HTTPException):
        await query_add(async_session, region_id, category_id, query)
