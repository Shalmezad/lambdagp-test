import random
import uuid

from aws_lambda_powertools.utilities.validation import validator

import schemas
from component_types import CGPBuilderConfig, CGPBuilderEvent


def build_individual(config: CGPBuilderConfig):
    num_inputs = config["num_inputs"]
    # Alright, so we build up the middle nodes:
    nodes = []
    for i in range(config["num_middle_nodes"]):
        # Pick random input nodes
        lhs = random.randrange(0, num_inputs + i)
        rhs = random.randrange(0, num_inputs + i)
        # Pick an operator:
        op = random.randrange(0, config["instruction_set_length"])
        nodes.append([lhs, rhs, op])
    # Now add the output nodes:
    for i in range(config["num_outputs"]):
        # Pick random source node:
        source = random.randrange(0, num_inputs + config["num_middle_nodes"])
        nodes.append([source])
    return nodes


@validator(inbound_schema=schemas.INPUT)
def lambda_handler(event: CGPBuilderEvent, context):
    # We need to build an individual:
    individual = build_individual(event["config"]["cgp_builder"])
    ind_id = str(uuid.uuid4())
    return {
        "config": event["config"],
        "metadata": event["metadata"],
        "individuals": {
            ind_id: individual
        }
    }
