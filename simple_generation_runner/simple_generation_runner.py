
from component_types import (
    Metadata,
    SimpleGenerationRunnerEvent,
    SimpleGenerationRunnerMetadata
)


def setup_metadata(metadata: Metadata):
    if "simple_generation_runner" not in metadata:
        new_meta = SimpleGenerationRunnerMetadata()
        metadata["simple_generation_runner"] = new_meta
    if "current_generation" not in metadata["simple_generation_runner"]:
        metadata["simple_generation_runner"]['current_generation'] = 0

    return metadata


def lambda_handler(event: SimpleGenerationRunnerEvent, context):
    config = event["config"]
    metadata = event["metadata"]
    population = event["population"]

    metadata = setup_metadata(metadata)

    # Get the generation:
    generation = metadata["simple_generation_runner"]["current_generation"]
    generation += 1
    metadata["simple_generation_runner"]["current_generation"] = generation

    # Are we done?
    max_generations = config["simple_generation_runner"]["max_generations"]
    is_done = generation >= max_generations

    return {
        "config": config,
        "metadata": metadata,
        "population": population,
        "is_done": is_done
    }
