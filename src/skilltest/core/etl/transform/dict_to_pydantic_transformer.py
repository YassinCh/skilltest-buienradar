from typing import Iterable, TypeVar

from pydantic import BaseModel

from ..extract import FetchItem
from .abstract_transformer import AbstractTransformer

ModelT = TypeVar("ModelT", bound=BaseModel)


class DictToPydanticTransformer(AbstractTransformer[FetchItem, ModelT]):
    def __init__(self, model_type: type[ModelT]):
        self.model_type = model_type

    def transform(self, input: Iterable[FetchItem]) -> Iterable[ModelT]:
        for entry in input:
            yield self.model_type(**entry.data)
