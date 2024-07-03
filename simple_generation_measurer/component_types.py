from typing import TypedDict, Any, Dict, NotRequired


class SimpleGenerationMeasuererMetadata(TypedDict):
    population: NotRequired[Dict[str, Any]]
    fitnesses: NotRequired[Dict[str, Dict[str, float]]]


class Metadata(TypedDict):
    simple_generation_measuerer: NotRequired[SimpleGenerationMeasuererMetadata]


class SimpleGenerationMeasuererEvent(TypedDict):
    config: Any
    metadata: Metadata
    # Two cases:
    # a) We're coming from generation runner
    population: NotRequired[Dict[str, Any]]
    # b) We're coming from "Individual Measurer":
    fitnesses: NotRequired[Dict[str, Dict[str, float]]]
