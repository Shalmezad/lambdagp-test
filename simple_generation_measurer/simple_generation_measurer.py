from component_types import (
    SimpleGenerationMeasurerEvent
    )


def handle_generation_runner_event(event: SimpleGenerationMeasurerEvent):
    # We won't have our metadata, so build it:
    metadata = event["metadata"]
    population = event["population"]
    metadata["simple_generation_measurer"] = {}
    metadata["simple_generation_measurer"]["population"] = population
    metadata["simple_generation_measurer"]["fitnesses"] = {}
    # Pick an individual:
    to_test_id = list(population.keys())[0]
    return {
        "config": event["config"],
        "metadata": metadata,
        "is_done": True,
        "individuals": {
            to_test_id: population[to_test_id]
        }
    }


def handle_individual_measurer_event(event: SimpleGenerationMeasurerEvent):
    # For this one, we *SHOULD* have the metadata:
    # Let's take the fitnesses we received and add them to our metadata:
    metadata = event["metadata"]
    population = metadata["simple_generation_measurer"]["population"]
    saved_fitnesses = metadata["simple_generation_measurer"]["fitnesses"]
    for individual_id in event["fitnesses"]:
        fitness = event["fitnesses"][individual_id]
        saved_fitnesses[individual_id] = fitness
    # Now, let's see what individuals are left:
    all_individual_ids = population.keys()
    tested_individual_ids = saved_fitnesses.keys()
    remaining = all_individual_ids - tested_individual_ids
    if len(remaining) == 0:
        # We're done:
        # Clear our metadata:
        del metadata["simple_generation_measurer"]
        return {
            "config": event["config"],
            "metadata": metadata,
            "is_done": True,
            "population": population,
            "fitnesses": saved_fitnesses
        }
    else:
        # Not done
        # Grab an individual:
        to_test_id = list(remaining)[0]
        return {
            "config": event["config"],
            "metadata": metadata,
            "is_done": True,
            "individuals": {
                to_test_id: population[to_test_id]
            }
        }


def lambda_handler(event: SimpleGenerationMeasurerEvent, context):
    # Where are we coming from?
    if "population" in event:
        # We're coming from generation runner:
        return handle_generation_runner_event(event)
    else:
        # We're coming from individual measurer event:
        return handle_individual_measurer_event(event)
