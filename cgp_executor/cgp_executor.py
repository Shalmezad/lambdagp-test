
from typing import Any, TypedDict

from component_types import CGPExecutorEvent, Config


class CaseOutput(TypedDict):
    case_output: list[float]
    case_metadata: Any


class CaseInput(TypedDict):
    case_input: list[float]
    case_metadata: Any


class CGPExecutor:
    program: list[list[int]]
    config: Config
    num_in: int
    num_mid: int
    num_out: int

    def __init__(self, program: list[list[int]], config: Config):
        self.program = program
        self.config = config
        self.num_in = config["cgp_executor"]["num_inputs"]
        self.num_mid = config["cgp_executor"]["num_middle_nodes"]
        self.num_out = config["cgp_executor"]["num_outputs"]

    def get_node(self, node_idx: int, inputs: list[float]) -> float:
        # Is it an input node?
        if node_idx < self.num_in:
            return inputs[node_idx]
        # Ok, we're a middle node. Get the node:
        program_node_idx = node_idx - self.num_in
        node = self.program[program_node_idx]
        # 0 is lhs, 1 is rhs, 2 is op:
        lhs = self.get_node(node[0], inputs)
        rhs = self.get_node(node[1], inputs)
        op = self.config["cgp_executor"]["instruction_set"][node[2]]
        if op == '+':
            return lhs + rhs
        elif op == '-':
            return lhs - rhs
        elif op == '*':
            return lhs * rhs
        elif op == '%':
            if rhs == 0:
                return 0
            else:
                return lhs / rhs
        else:
            raise AttributeError('Unknown operator {}'.format(op))

    def evaluate(self, inputs: list[float]) -> list[float]:
        # Go through each of our output nodes:
        outputs = []
        for i in range(self.config["cgp_executor"]["num_outputs"]):
            # Get the idx:
            program_output_idx = self.num_mid + i
            source_idx = self.program[program_output_idx][0]
            result = self.get_node(source_idx, inputs)
            outputs.append(result)
        return outputs


def lambda_handler(event: CGPExecutorEvent, context):
    individuals = event['individuals']
    config = event['config']
    cases = event['cases']
    case_results = {}
    for individual_id in individuals:
        case_results[individual_id] = {}
        executor = CGPExecutor(individuals[individual_id], config)
        for case_id in cases:
            result = executor.evaluate(cases[case_id])
            case_results[individual_id][case_id] = result
    return {
        "config": config,
        "metadata": event["metadata"],
        "case_results": case_results
    }
