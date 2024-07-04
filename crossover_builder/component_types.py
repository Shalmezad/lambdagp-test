from typing import TypedDict, Any, Dict, NotRequired


class CrossoverBuilderMetadata(TypedDict):
    population: NotRequired[Dict[str, Any]]
    fitnesses: NotRequired[Dict[str, Dict[str, float]]]
    selected_parents: NotRequired[Dict[str, Any]]


class Metadata(TypedDict):
    crossover_builder: NotRequired[CrossoverBuilderMetadata]


class CrossoverBuilderEvent(TypedDict):
    config: Any
    metadata: Metadata
    # Two cases:
    # a) We're coming from generation builder
    population: NotRequired[Dict[str, Any]]
    fitnesses: NotRequired[Dict[str, Dict[str, float]]]
    # b) We're coming from parent selector:
    parents: NotRequired[Dict[str, Any]]
