import datetime
import random
import string
import uuid
from uuid import UUID

import pytest
from fastapi import HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from api import schema
from api.models import crud

from .test_utils import check_query, check_states


def unique_string() -> str:
    return uuid.uuid4().hex


def random_string(
    size: int = 10,
    alphabet: str = string.ascii_lowercase,
) -> str:
    return "".join(random.choice(alphabet) for i in range(size))  # noqa S311


def random_int() -> int:
    return random.randint(1, 100)  # noqa S311


class StateItem(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)  # noqa A003
    query_id: UUID
    timestamp: float = Field(default_factory=datetime.datetime.now().timestamp)
    value: int = Field(default_factory=random_int)


class QueryItem(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)  # noqa A003
    region_id: int | None = Field(default_factory=random_int)
    category_id: int | None = Field(default_factory=random_int)
    query: str | None = Field(default_factory=random_string)
    states: list[StateItem | None] = Field(default_factory=list)


def generate_query_state(
    stat_count: int = 1,
) -> QueryItem:
    td = QueryItem()
    td.states = [StateItem(query_id=td.id) for _ in range(stat_count)]
    return td


async def _create_test_data(
    async_session: AsyncSession,
    data: QueryItem,
) -> None:
    await async_session.execute(
        text(
            "INSERT INTO query (id, region_id, category_id, query) "
            "VALUES (:id, :region_id, :category_id, :query);"  # noqa C812
        ),
        params=data.model_dump(exclude={"states"}),
    )
    if data.states:
        await async_session.execute(
            text(
                "INSERT INTO stat (query_id, timestamp, value) "
                "VALUES (:query_id, :timestamp, :value);"  # noqa C812
            ),
            params=[item.model_dump() for item in data.states if item],
        )
    await async_session.commit()


async def test_stat_not_exist(
    async_session: AsyncSession,
) -> None:
    with pytest.raises(HTTPException):
        await crud.stats_get(
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
async def test_stat_empty(
    async_session: AsyncSession,
    region_id: int,
    category_id: int,
    query: str,
    clear_tables: None,  # noqa U100
) -> None:
    query_id = (
        await crud.query_add(
            async_session,
            region_id=region_id,
            category_id=category_id,
            query=query,
        )
    ).query_id

    result: list[schema.StatOut]
    result = await crud.stats_get(async_session, query_id)
    assert result == []


async def test_stat(
    async_session: AsyncSession,
    clear_tables: None,  # noqa U100
) -> None:
    data = generate_query_state(5)
    await _create_test_data(async_session, data)
    await check_query(
        session=async_session,
        query_id=data.id,
        region_id=data.region_id,
        category_id=data.category_id,
        query=data.query,
    )
    assert await check_states(
        session=async_session,
        query_id=data.id,
        states=data.states,
    )


async def test_stat_without_1(
    async_session: AsyncSession,
    clear_tables: None,  # noqa U100
) -> None:
    data = generate_query_state(5)
    await _create_test_data(async_session, data)
    await check_query(
        session=async_session,
        query_id=data.id,
        region_id=data.region_id,
        category_id=data.category_id,
        query=data.query,
    )
    data.states.pop()
    assert not await check_states(
        session=async_session,
        query_id=data.id,
        states=data.states,
    )


async def test_stat_broken_value(
    async_session: AsyncSession,
    clear_tables: None,  # noqa U100
) -> None:
    data = generate_query_state(5)
    await _create_test_data(async_session, data)
    await check_query(
        session=async_session,
        query_id=data.id,
        region_id=data.region_id,
        category_id=data.category_id,
        query=data.query,
    )
    # Портим значение
    if data.states[0]:
        data.states[0].value = -data.states[0].value
        assert not await check_states(
            session=async_session,
            query_id=data.id,
            states=data.states,
        )
