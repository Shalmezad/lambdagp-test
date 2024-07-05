from component_types import (
    SimpleGenerationBuilderEvent
    )


def handle_generation_measurer_event(event: SimpleGenerationBuilderEvent):
    # We won't have our metadata, so build it:
    metadata = event["metadata"]
    population = event["population"]
    fitnesses = event["fitnesses"]
    metadata["simple_generation_builder"] = {}
    metadata["simple_generation_builder"]["previous_population"] = population
    metadata["simple_generation_builder"]["fitnesses"] = fitnesses
    metadata["simple_generation_builder"]["new_population"] = {}
    # We 100% need to build a new individual at this point:
    return {
        "config": event["config"],
        "metadata": metadata,
        "popupulation": population,
        "fitnesses": fitnesses,
        "is_done": False
    }


def handle_child_builder_event(event: SimpleGenerationBuilderEvent):
    # For this one, we *SHOULD* have the metadata:
    metadata = event["metadata"]
    new_pop = metadata["simple_generation_builder"]["new_population"]
    # Tack on the new individuals:
    for child_id in event["children"]:
        new_pop[child_id] = event["children"][child_id]
    # Have we hit the required population size yet?
    req_size = event["config"]["simple_generation_builder"]["population_size"]
    if len(new_pop) >= req_size:
        # We're done
        del metadata["simple_generation_builder"]
        return {
            "metadata": metadata,
            "config": event["config"],
            "population": new_pop,
            "is_done": True
        }
    else:
        # Not done, need another individual:
        prev_pop = metadata["simple_generation_builder"]["previous_population"]
        return {
            "metadata": metadata,
            "config": event["config"],
            "is_done": False,
            "population": prev_pop,
            "fitnesses": metadata["simple_generation_builder"]["fitnesses"]
        }


def lambda_handler(event: SimpleGenerationBuilderEvent, context):
    # Where are we coming from?
    if "population" in event:
        # We're coming from generation measuerer:
        return handle_generation_measurer_event(event)
    else:
        # We're coming from child builder event:
        return handle_child_builder_event(event)
