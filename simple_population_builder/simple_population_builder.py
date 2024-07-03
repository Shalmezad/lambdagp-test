from typing import TypedDict, Any, Dict, NotRequired

from aws_lambda_powertools.utilities.validation import validator

import schemas


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


def setup_metadata(metadata: Metadata):
    if "simple_population_builder" not in metadata:
        metadata["simple_population_builder"] = SimplePopulationBuilderMetadata()
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
