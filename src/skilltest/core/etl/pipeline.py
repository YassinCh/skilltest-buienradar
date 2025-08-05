from typing import Any, Generic, Sequence, TypeVar

from .extract import AbstractSource
from .load import ModelLoader
from .transform import AbstractTransformer

OutputT = TypeVar("OutputT")
TransformerT = TypeVar("TransformerT")


class Pipeline(Generic[OutputT]):
    def __init__(
        self,
        source: AbstractSource,
        loader: ModelLoader = ModelLoader(),
        transformers: Sequence[AbstractTransformer[Any, Any]] = (),
    ):
        self.source = source
        self.loader = loader
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
        self.loader.load_into_db(data)
