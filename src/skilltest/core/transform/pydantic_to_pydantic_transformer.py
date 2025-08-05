from typing import Callable, Iterable, TypeVar

from pydantic import BaseModel

from .abstract_transformer import AbstractTransformer

InputModelT = TypeVar("InputModelT", bound=BaseModel)
OutputModelT = TypeVar("OutputModelT", bound=BaseModel)


class PydanticToPydanticTransformer(AbstractTransformer[InputModelT, OutputModelT]):
    def __init__(
        self,
        input_model_type: type[InputModelT],
        output_model_type: type[OutputModelT],
        transform_definition: Callable[[InputModelT], OutputModelT],
    ):
        self.input_model_type = input_model_type
        self.output_model_type = output_model_type
        self.transform_definition = transform_definition

    def transform(self, input: Iterable[InputModelT]) -> Iterable[OutputModelT]:
        for entry in input:
            yield self.transform_definition(entry)
