from typing import TypedDict, Any, Dict, NotRequired


class SimpleGenerationBuilderConfig(TypedDict):
    population_size: int


class Config(TypedDict):
    simple_generation_builder: SimpleGenerationBuilderConfig


class SimpleGenerationBuilderMetadata(TypedDict):
    previous_population: NotRequired[Dict[str, Any]]
    new_population: NotRequired[Dict[str, Any]]
    fitnesses: NotRequired[Dict[str, Dict[str, float]]]


class Metadata(TypedDict):
    simple_generation_builder: NotRequired[SimpleGenerationBuilderMetadata]


class SimpleGenerationBuilderEvent(TypedDict):
    config: Config
    metadata: Metadata
    # Two cases:
    # a) We're coming from generation grader
    population: NotRequired[Dict[str, Any]]
    fitnesses: NotRequired[Dict[str, Dict[str, float]]]
    # b) We're coming from "Child Builder":
    children: NotRequired[Dict[str, Any]]
