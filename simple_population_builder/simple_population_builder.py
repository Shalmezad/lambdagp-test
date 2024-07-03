

from aws_lambda_powertools.utilities.validation import validator

import schemas
from component_types import (
    Metadata,
    SimplePopulationBuilderMetadata,
    SimplePopulationBuilderEvent
    )


def setup_metadata(metadata: Metadata):
    if "simple_population_builder" not in metadata:
        new_meta = SimplePopulationBuilderMetadata()
        metadata["simple_population_builder"] = new_meta
    if "population" not in metadata["simple_population_builder"]:
        metadata["simple_population_builder"]['population'] = {}

    return metadata


@validator(inbound_schema=schemas.INPUT)
def lambda_handler(event: SimplePopulationBuilderEvent, context):
    config = event["config"]
    metadata = event["metadata"] if "metadata" in event else Metadata()
    # Create the metadata if needed
    metadata = setup_metadata(metadata)

    population = metadata["simple_population_builder"]["population"]

    # Do we have any individuals to add?
    if "individuals" in event:
        # Tack them on:
        for ind_id in event["individuals"]:
            individual = event["individuals"][ind_id]
            population[ind_id] = individual

    # Do we have enough?
    required_size = config["simple_population_builder"]["population_size"]
    current_size = len(population)
    if current_size >= required_size:
        # We have enough, so stop building
        # Clear out our metadata as we no longer need it:
        del metadata["simple_population_builder"]
        return {
            "config": config,
            "metadata": metadata,
            "is_done": True,
            "population": population
        }
    else:
        # We need more individuals:
        return {
            "config": config,
            "metadata": metadata,
            "is_done": False
        }
