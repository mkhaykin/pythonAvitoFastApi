from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from api import models
from api.models import crud


async def check_query(
    session: AsyncSession,
    query_id: UUID,
    region_id: int | None,
    category_id: int | None,
    query: str | None,
) -> None:
    db_obj = await session.get_one(models.Query, query_id)
    assert db_obj
    assert db_obj.region_id == region_id
    assert db_obj.category_id == category_id
    assert db_obj.query == query


def not_accurate_dict_equal(
    a: dict,
    b: dict,
    keys: tuple[str, ...],
) -> bool:
    return all(key in a and key in b and a[key] == b[key] for key in keys)


def not_accurate_in(
    items: list[dict],
    value: dict,
    keys: tuple[str, ...],
) -> bool:
    for item in items:
        if not_accurate_dict_equal(item, value, keys):
            return True
    return False


def not_accurate_equal(
    a: list[dict],
    b: list[dict],
    keys: tuple[str, ...],
) -> bool:
    if len(a) != len(b):
        return False
    for item in b:
        if not not_accurate_in(a, item, keys):
            return False
    return True


async def check_states(
    session: AsyncSession,
    states: list[Any],
    query_id: UUID,
) -> bool:
    result = [
        item.model_dump()
        for item in await crud.stats_get(
            session=session,
            query_id=query_id,
        )
    ]
    return not_accurate_equal(
        [item.model_dump() for item in states],
        result,
        keys=("timestamp", "value"),
    )  # type


async def query_add(
    session: AsyncSession,
    region_id: int | None,
    category_id: int | None,
    query: str | None,
) -> None:
    query_id = (
        await crud.query_add(
            session,
            region_id=region_id,
            category_id=category_id,
            query=query,
        )
    ).query_id

    await check_query(session, query_id, region_id, category_id, query)
