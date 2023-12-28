from fastapi import APIRouter

api = APIRouter()


@api.get("/add")
async def add() -> dict:
    return {"action": "add"}


@api.get("/stat")
async def stat() -> dict:
    return {"action": "stat"}
