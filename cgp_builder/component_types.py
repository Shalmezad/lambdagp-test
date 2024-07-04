from typing import TypedDict, Any


class CGPBuilderConfig(TypedDict):
    num_inputs: int
    num_middle_nodes: int
    num_outputs: int
    instruction_set_length: int


class Config(TypedDict):
    cgp_builder: CGPBuilderConfig


class CGPBuilderEvent(TypedDict):
    config: Config
    metadata: Any
