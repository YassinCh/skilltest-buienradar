from dataclasses import dataclass
from typing import Any


@dataclass
class FetchItem:
    # TODO: Data is untyped. Suggestion: replace by more specific types
    data: dict[str, Any]
