from typing import TypedDict, Any, Dict, NotRequired


class SimplePopulationBuilderConfig(TypedDict):
    population_size: int


class Config(TypedDict):
    simple_population_builder: SimplePopulationBuilderConfig


class SimplePopulationBuilderMetadata(TypedDict):
    population: NotRequired[Dict[str, Any]]


class Metadata(TypedDict):
    simple_population_builder: NotRequired[SimplePopulationBuilderMetadata]


class SimplePopulationBuilderEvent(TypedDict):
    # Individuals will only exist
    # if we're coming from an individual builder component
    individuals: NotRequired[Dict[str, Any]]
    config: Config
    metadata: NotRequired[Metadata]
