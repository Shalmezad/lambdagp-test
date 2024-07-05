from typing import TypedDict, Any


class CGPExecutorConfig(TypedDict):
    num_inputs: int
    num_middle_nodes: int
    num_outputs: int
    instruction_set: list[str]


class Config(TypedDict):
    cgp_executor: CGPExecutorConfig


class CGPExecutorEvent(TypedDict):
    config: Config
    metadata: Any
