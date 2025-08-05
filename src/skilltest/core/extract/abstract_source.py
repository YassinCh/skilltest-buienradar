from abc import ABC, abstractmethod
from typing import Iterable

from .fetch_item import FetchItem


class AbstractSource(ABC):
    @abstractmethod
    def fetch(self) -> Iterable[FetchItem]:
        pass
