from typing import Iterable

import httpx

from .abstract_source import AbstractSource
from .fetch_item import FetchItem


class HttpSource(AbstractSource):
    def __init__(self, url: str):
        self.url = url

    def fetch(self) -> Iterable[FetchItem]:
        response = httpx.get(self.url)
        for line in response.iter_lines():
            # TODO: Key right now is a string potential improved using typedDict
            yield FetchItem(data=dict(line=line))
