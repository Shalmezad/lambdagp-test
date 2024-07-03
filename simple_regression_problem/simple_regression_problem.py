from typing import Dict, List
from component_types import SimpleRegressionProblemEvent


def measure_fitness(cases: Dict[str, List[float]]) -> Dict[str, float]:
    fitnesses = {}
    # We have a dictionary of case_ids / outputs
    for case_id in cases:
        # We control the case_id. We cheated and used the input for the id:
        input = float(case_id)
        # Here, we're going to use the example from:
        #   "Genetic Programming An Introduction" by Wolfgang Banzhaf et al
        # Which is the function x^2 / 2 for the input range [0.0, 1.0)
        expected_output = pow(input, 2.0) / 2.0
        actual_output = cases[case_id][0]
        # Our fitness is simply the difference between the two:
        fitness = abs(expected_output - actual_output)
        fitnesses[case_id] = fitness
    return fitnesses


def measure_fitnesses(case_results: Dict[str, Dict[str, List[float]]]) -> Dict[str, Dict[str, float]]:
    # Alright, we have our ind_id: {case_id: [outputs]}
    # We need to measure each fitness:
    fitnesses = {}
    for individual_id in case_results:
        fitness = measure_fitness(case_results[individual_id])
        fitnesses[individual_id] = fitness
    return fitnesses


def handle_executor_event(event: SimpleRegressionProblemEvent):
    """Handles an event from an Individual Executor component"""
    # Alright, so we have `case_results`
    # Let's get our fitnesses:
    fitnesses = measure_fitnesses(event["case_results"])
    # And build our payload (this one doesn't need to do cycles)
    return {
        "config": event["config"],
        "metadata": event["metadata"],
        "is_done": True,
        "fitnesses": fitnesses
    }

def handle_generation_event(event: SimpleRegressionProblemEvent):
    """Handles an event from a Generation Measurer component"""
    # We're going to make our cases:
    # Which is the function x^2 / 2 for the input range [0.0, 1.0)
    case_inputs = [x / 10.0 for x in range(0, 10, 1)]
    cases = {}
    for input in case_inputs:
        case_id = str(input)
        # There's only 1 input:
        cases[case_id] = [input]
    # Now to build our payload:
    return {
        "config": event["config"],
        "metadata": event["metadata"],
        "is_done": False,
        "cases": cases,
        "individuals": event["individuals"]
    }


def lambda_handler(event: SimpleRegressionProblemEvent, context):
    # Are we coming from "Generation Measurer" or "Individual Executor" ?
    if "individuals" in event:
        # We're from Generation Measuer:
        return handle_generation_event(event)
    else:
        # We're from individual executor
        return handle_executor_event(event)