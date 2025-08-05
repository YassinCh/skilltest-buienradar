from typing import Any, Generic, Sequence, TypeVar

from sqlmodel import Session

from ..database import engine
from .extract import AbstractSource
from .transform import AbstractTransformer

OutputT = TypeVar("OutputT")
TransformerT = TypeVar("TransformerT")


class Pipeline(Generic[OutputT]):
    def __init__(
        self,
        source: AbstractSource,
        transformers: Sequence[AbstractTransformer[Any, Any]] = (),
    ):
        self.source = source
        self.transformers = list(transformers)

    def add(
        self, transformer: AbstractTransformer[OutputT, TransformerT]
    ) -> "Pipeline[TransformerT]":
        updated_transformers = self.transformers + [transformer]
        return Pipeline(source=self.source, transformers=updated_transformers)

    def run(self) -> None:
        data = self.source.fetch()
        for transformer in self.transformers:
            data = transformer.transform(data)

        # TODO: Move this logic to load and add for example batching logic
        with Session(engine) as session:
            for item in data:
                session.merge(item)
            session.commit()
