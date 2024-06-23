from aws_lambda_powertools.utilities.validation import validator

import schemas


class TreeExecutor:
    def __init__(self, program, config):
        self.program = program
        self.config = config

    def is_input_node(self, node):
        return node.startswith("I")

    def is_operand(self, node):
        return node in ["+", "-", "*", "%"]

    def get_input(self, node, inputs):
        node_idx_str = node.replace('I', '')
        node_idx = int(node_idx_str)
        return inputs[node_idx]

    def operate(self, lhs, rhs, operand):
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
            raise 'Unknown operator {}'.format(operand)

    def evaluate(self, case):
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
def lambda_handler(event, context):
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
