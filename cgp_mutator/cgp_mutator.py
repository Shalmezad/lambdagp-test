

from typing import Any, Dict
import random
import uuid

from component_types import CGPMutatorEvent, Config


def handle_generation_builder_event(event: CGPMutatorEvent):
    # We 100% need a new individual at this point:
    # We only need 1, so no need to store anything in metadata
    return {
        "config": event["config"],
        "metadata": event["metadata"],
        "popupulation": event["population"],
        "fitnesses": event["fitnesses"],
        "is_done": False
    }


def mutate(parent: list[list[int]], config: Config) -> list[list[int]]:
    num_in = config["cgp_mutator"]["num_inputs"]
    num_mid = config["cgp_mutator"]["num_middle_nodes"]
    num_out = config["cgp_mutator"]["num_outputs"]
    instruction_set_length = config["cgp_mutator"]["instruction_set_length"]
    mutation_rate = config["cgp_mutator"]["mutation_rate"]
    # Go through each:
    for i in range(num_mid):
        in_max = i + num_in
        if random.random() < mutation_rate:
            parent[i][0] = random.randrange(0, in_max)
        if random.random() < mutation_rate:
            parent[i][1] = random.randrange(0, in_max)
        if random.random() < mutation_rate:
            parent[i][2] = random.randrange(0, instruction_set_length)
    for i in range(num_out):
        if random.random() < mutation_rate:
            source = random.randrange(0, num_in + num_mid)
            parent[num_mid + i] = [source]
    return parent


def handle_parent_selector_event(event: CGPMutatorEvent):
    config = event["config"]
    parents = event["parents"]
    children = {}
    for parent_id in parents:
        child = mutate(parents[parent_id], config)
        child_id = str(uuid.uuid4())
        children[child_id] = child
    return {
        "config": config,
        "metadata": event["metadata"],
        "children": children,
        "is_done": True
    }


def lambda_handler(event: CGPMutatorEvent, context):
    # Where are we coming from?
    if "population" in event:
        # We're coming from generation builder:
        return handle_generation_builder_event(event)
    else:
        # We're coming from parent selector:
        return handle_parent_selector_event(event)
