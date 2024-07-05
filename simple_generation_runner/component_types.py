import sys
if sys.version_info < (3, 11):
    from typing_extensions import TypedDict, Any, Dict, NotRequired
else:
    from typing import TypedDict, Any, Dict, NotRequired


class SimpleGenerationRunnerConfig(TypedDict):
    max_generations: int


class Config(TypedDict):
    simple_generation_runner: SimpleGenerationRunnerConfig


class SimpleGenerationRunnerMetadata(TypedDict):
    current_generation: NotRequired[int]


class Metadata(TypedDict):
    simple_generation_runner: NotRequired[SimpleGenerationRunnerMetadata]


class SimpleGenerationRunnerEvent(TypedDict):
    population: Dict[str, Any]
    config: Config
    metadata: Metadata
