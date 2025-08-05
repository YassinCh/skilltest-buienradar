from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class AbstractTransformer(ABC, Generic[InputT, OutputT]):
    @abstractmethod
    def transform(self, input: Iterable[InputT]) -> Iterable[OutputT]:
        pass
