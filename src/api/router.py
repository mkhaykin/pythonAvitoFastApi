import http

from fastapi import APIRouter, Depends

from src.api import schema
from src.api.service import Service

api = APIRouter()


@api.post(
    path="/add",
    summary="Create monitoring",
    status_code=http.HTTPStatus.CREATED,
    responses={
        404: {
            "model": schema.Message,
            "description": "The category ID or region ID does not exists",
        },
        409: {
            "model": schema.Message,
            "description": "The query with the same params already exists",
        },
    },
    response_model=schema.QueryOut,
    response_description="Return the ID of the created search query",
)
async def add(
    params: schema.QueryIn = Depends(),
    service: Service = Depends(),
) -> schema.QueryOut:
    return await service.add(params)


@api.get(
    path="/stat",
    summary="Get statistic by query id",
    response_model=list[schema.StatOut],
    response_description="Return statistics",
)
async def stat(
    params: schema.StatIn = Depends(),
    service: Service = Depends(),
) -> list[schema.StatOut]:
    return await service.stat(params.query_id)
