from dataclasses import dataclass
from typing import TypeAlias, TypedDict
from Utils.constants import SUPPORTED_NODETYPES, MODELS
from typing import TypeAlias, Union


class NODETYPE_LIST(list):
    ALLOWED_TYPES = SUPPORTED_NODETYPES

    def __init__(self, *args):
        super().__init__(*args)
        for item in self:
            self._validate(item)

    def _validate(self, item):
        if not isinstance(item, str):
            raise ValueError("NODETYPES only accepts string values.")
        if item not in self.ALLOWED_TYPES:
            raise ValueError(f"'{item}' is not allowed. Allowed types: {self.ALLOWED_TYPES}")

    def append(self, item):
        self._validate(item)
        super().append(item)

    def extend(self, iterable):
        for item in iterable:
            self._validate(item)
        super().extend(iterable)

AxoviaNodeType: TypeAlias = NODETYPE_LIST

class NodeDebug(TypedDict, total=False):
    enter: bool = False
    exit: bool = False
    error: bool = False
    
class Prompt(TypedDict):
    text: str
    var: str
