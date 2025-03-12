from dataclasses import dataclass, field
from Utils.decorators import nodewrap
from Utils.types import AxoviaNodeType, NodeDebug
from Utils.states import WorkflowState


class AxoviaNode:

    def __init__(self):
        self.prompt: str = "Axovia>  "
        self.debug: NodeDebug = field(default_factory=NodeDebug)

    def method(self, state: WorkflowState) -> dict[str, str]:
        raise NotImplementedError("method not implemented")

    def output(self, msg: str):
        print(f"{self.prompt} {msg}")
