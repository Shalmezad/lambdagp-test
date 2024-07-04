from typing import TypedDict, Any
from aws_lambda_powertools.utilities.validation import validator

import schemas


class CaseOutput(TypedDict):
    case_output: list[float]
    case_metadata: Any


class CaseInput(TypedDict):
    case_input: list[float]
    case_metadata: Any


class TreeExecutorEvent(TypedDict):
    individual: list[str]
    config: Any
    cases: list[CaseInput]


class TreeExecutorOutput(TypedDict):
    individual: list[str]
    cases: list[CaseOutput]
    config: Any


class TreeExecutor:
    program: list[str]

    def __init__(self, program: list[str], config):
        self.program = program
        self.config = config

    def is_input_node(self, node: str) -> bool:
        return node.startswith("I")

    def is_operand(self, node: str) -> bool:
        return node in ["+", "-", "*", "%"]

    def get_input(self, node: str, inputs: list[float]) -> float:
        node_idx_str = node.replace('I', '')
        node_idx = int(node_idx_str)
        # NOTE: There is a chance the idx is out of range
        # To help prevent that, we're going to wrap:
        node_idx = node_idx % len(inputs)
        return inputs[node_idx]

    def operate(self, lhs: float, rhs: float, operand: str) -> float:
        if operand == '+':
            return lhs + rhs
        elif operand == '-':
            return lhs - rhs
        elif operand == '*':
            return lhs * rhs
        elif operand == '%':
            if rhs == 0:
                return 0
            else:
                return lhs / rhs
        else:
            raise AttributeError('Unknown operator {}'.format(operand))

    def evaluate(self, case: CaseInput) -> CaseOutput:
        # Go through the tree:
        inputs = case["case_input"]
        stack = []
        for node in self.program:
            if self.is_input_node(node):
                stack.append(self.get_input(node, inputs))
            elif self.is_operand(node):
                rhs = stack.pop()
                lhs = stack.pop()
                stack.append(self.operate(lhs, rhs, node))
            else:
                # Should be a constant:
                stack.append(float(node))
        return {
            "case_output": stack,
            # Reflect the metadata for problem tracking:
            "case_metadata": case["case_metadata"]
        }


@validator(inbound_schema=schemas.INPUT)
def lambda_handler(event: TreeExecutorEvent, context) -> TreeExecutorOutput:
    # Gene will be an array of tree nodes in POSTFIX notation
    # ie: (A + B) * C will be ['A', 'B', '+', 'C', '*']
    gene = event['individual']
    config = event['config']
    cases = event['cases']
    executor = TreeExecutor(gene, config)
    output_cases = [executor.evaluate(case) for case in cases]
    return {
        "cases": output_cases,
        "individual": gene,
        "config": config
    }
