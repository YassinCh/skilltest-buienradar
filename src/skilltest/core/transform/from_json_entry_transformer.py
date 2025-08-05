import json
from typing import Iterable, Sequence

from ..extract import FetchItem
from .abstract_transformer import AbstractTransformer


class FromJsonToEntryTransformer(AbstractTransformer[FetchItem, FetchItem]):
    # TODO: Better name for this class
    def __init__(self, data_path: Sequence[str]):
        self.data_path = data_path

    def transform(self, input: Iterable[FetchItem]) -> Iterable[FetchItem]:
        # TODO: this uses hard coded key which isn't great
        json_string = "".join(item.data["line"] for item in input)
        json_data = json.loads(json_string)

        for element in self.data_path:
            if element not in json_data:
                raise ValueError(f"{element} key of data_path not found in json data")
            json_data = json_data[element]
        for entry in json_data:
            yield FetchItem(data=entry)
