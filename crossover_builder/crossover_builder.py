

from typing import Any, Dict
import random
import uuid

from component_types import CrossoverBuilderEvent
from tree_parser import TreeParser


def handle_generation_builder_event(event: CrossoverBuilderEvent):
    # We won't have our metadata, so build it:
    metadata = event["metadata"]
    population = event["population"]
    fitnesses = event["fitnesses"]
    metadata["crossover_builder"]["population"] = population
    metadata["crossover_builder"]["fitnesses"] = fitnesses
    metadata["crossover_builder"]["selected_parents"] = {}
    # We 100% need a new individual at this point:
    return {
        "config": event["config"],
        "metadata": metadata,
        "population": population,
        "fitnesses": fitnesses,
        "is_done": False
    }


def make_children(parents: Dict[str, Any]) -> Dict[str, Any]:
    # Here's what we're going to do:
    # We're going to grab two parents:
    parent_ids = list(parents.keys())
    parent_a = parents[parent_ids[0]]
    parent_b = parents[parent_ids[1]]
    # Now, build up the trees:
    tree_a = TreeParser.parse(parent_a)
    tree_b = TreeParser.parse(parent_b)
    # Now get a random subtree in B:
    tree_b_idx = random.randint(0, tree_b.size()-1)
    sub_tree_b = tree_b.get_child(tree_b_idx)
    # And replace a random subtree in A:
    tree_a_idx = random.randint(0, tree_a.size()-1)
    tree_a = tree_a.set_child(tree_a_idx, sub_tree_b)
    tree_id = str(uuid.uuid4())
    return {
        tree_id: tree_a.to_postfix()
    }


def handle_parent_selector_event(event: CrossoverBuilderEvent):
    # Alright, let's grab our metadata:
    metadata = event["metadata"]
    selected_parents = metadata["crossover_builder"]["selected_parents"]
    # Tack on the new parent(s):
    new_parents = event["parents"]
    for parent_id in new_parents:
        selected_parents[parent_id] = new_parents[parent_id]
    # Do we have enough?
    if len(new_parents) >= 2:
        # We have enough, let's build:
        children = make_children(new_parents)
        # Clear out our metadata:
        del metadata["crossover_builder"]
        return {
            "config": event["config"],
            "metadata": metadata,
            "children": children,
            "is_done": True
        }
    else:
        # Don't have enough:
        return {
            "config": event["config"],
            "metadata": metadata,
            "population": metadata["crossover_builder"]["population"],
            "fitnesses": metadata["crossover_builder"]["fitnesses"],
            "is_done": False
        }


def lambda_handler(event: CrossoverBuilderEvent, context):
    # Where are we coming from?
    if "population" in event:
        # We're coming from generation builder:
        return handle_generation_builder_event(event)
    else:
        # We're coming from parent selector:
        return handle_parent_selector_event(event)
