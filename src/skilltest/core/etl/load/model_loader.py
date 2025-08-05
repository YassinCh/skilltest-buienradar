from typing import Any, Iterable

from sqlmodel import Session

from ....database import engine


class ModelLoader:
    # TODO: Add upsert logic and batching logic
    def load_into_db(self, data: Iterable[Any]):
        with Session(engine) as session:
            for item in data:
                session.merge(item)
            session.commit()
