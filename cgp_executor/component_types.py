from typing import Dict, TypedDict, Any


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
    cases: Dict[str, list[float]]
    individuals: Dict[str, list[list[int]]]
