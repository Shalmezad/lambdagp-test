import sys
if sys.version_info < (3, 11):
    from typing_extensions import TypedDict, Any, Dict, NotRequired
else:
    from typing import TypedDict, Any, Dict, NotRequired


class SimpleGenerationMeasurerMetadata(TypedDict):
    population: NotRequired[Dict[str, Any]]
    fitnesses: NotRequired[Dict[str, Dict[str, float]]]


class Metadata(TypedDict):
    simple_generation_measurer: NotRequired[SimpleGenerationMeasurerMetadata]


class SimpleGenerationMeasurerEvent(TypedDict):
    config: Any
    metadata: Metadata
    # Two cases:
    # a) We're coming from generation runner
    population: NotRequired[Dict[str, Any]]
    # b) We're coming from "Individual Measurer":
    fitnesses: NotRequired[Dict[str, Dict[str, float]]]
