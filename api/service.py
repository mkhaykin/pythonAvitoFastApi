from datetime import datetime
from uuid import UUID, uuid4

from fastapi import BackgroundTasks, HTTPException

from api import schema

fake_db = {UUID("b7108af0-efdd-4bf3-90f7-60dc9d58eb25")}
fake_data = set()
fake_answer = [
    schema.StatOut(
        timestamp=datetime.now().timestamp(),
        value=10,
    ),
    schema.StatOut(
        timestamp=datetime.now().timestamp() - 10,
        value=15,
    ),
]


class Service:
    def __init__(
        self,
        background_tasks: BackgroundTasks = BackgroundTasks(),
    ) -> None:
        self.background_tasks = background_tasks

    def add(self, query: schema.AddIn) -> schema.AddOut:
        if (query.region_id, query.category_id, query.query) in fake_data:
            raise HTTPException(
                status_code=409,
                detail="The query with the same params already exists",
            )

        id_obj = uuid4()
        fake_db.add(id_obj)
        fake_data.add((query.region_id, query.category_id, query.query))

        return schema.AddOut(query_id=id_obj)

    def stat(self, obj_id: UUID) -> list[schema.StatOut]:
        if obj_id not in fake_db:
            raise HTTPException(
                status_code=404,
                detail=f"The query with id='{obj_id}' not found",
            )

        return fake_answer
