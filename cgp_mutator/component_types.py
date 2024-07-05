import sys
if sys.version_info < (3, 11):
    from typing_extensions import TypedDict, Any, Dict, NotRequired
else:
    from typing import TypedDict, Any, Dict, NotRequired


class CGPMutatorConfig(TypedDict):
    num_inputs: int
    num_middle_nodes: int
    num_outputs: int
    instruction_set_length: int
    mutation_rate: float


class Config(TypedDict):
    cgp_mutator: CGPMutatorConfig


class CGPMutatorEvent(TypedDict):
    config: Any
    metadata: Any
    # Two cases:
    # a) We're coming from generation builder
    population: NotRequired[Dict[str, Any]]
    fitnesses: NotRequired[Dict[str, Dict[str, float]]]
    # b) We're coming from parent selector:
    parents: NotRequired[Dict[str, Any]]
