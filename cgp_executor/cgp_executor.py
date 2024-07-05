
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

    def __init__(self, program: list[str], config: Config):
        self.program = program
        self.config = config
        self.num_in = config["cgp_executor"]["num_inputs"]
        self.num_mid = config["cgp_executor"]["num_middle_nodes"]
        self.num_out = config["cgp_executor"]["num_outputs"]

    def get_node(self, node_idx: int, case: CaseInput) -> float:
        # Is it an input node?
        if node_idx < self.num_in:
            return case["case_input"][node_idx]
        # Ok, we're a middle node. Get the node:
        program_node_idx = node_idx - self.num_in
        node = self.program[program_node_idx]
        # 0 is lhs, 1 is rhs, 2 is op:
        lhs = self.get_node(node[0], case)
        rhs = self.get_node(node[1], case)
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

    def evaluate(self, case: CaseInput) -> CaseOutput:
        # Go through each of our output nodes:
        outputs = []
        for i in range(self.config["cgp_executor"]["num_outputs"]):
            # Get the idx:
            program_output_idx = self.num_in + self.num_mid + i
            source_idx = self.program[program_output_idx][0]
            result = self.get_node(source_idx, case)
            outputs.append(result)


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
            "case_output": outputs,
            # Reflect the metadata for problem tracking:
            "case_metadata": case["case_metadata"]
        }


def lambda_handler(event: CGPExecutorEvent, context):
    gene = event['individual']
    config = event['config']
    cases = event['cases']
    executor = CGPExecutor(gene, config)
    output_cases = [executor.evaluate(case) for case in cases]
    return {
        "cases": output_cases,
        "individual": gene,
        "config": config
    }
