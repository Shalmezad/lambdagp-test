import unittest
from aws_lambda_powertools.utilities.validation import validate
from treeexecutor import TreeExecutor, lambda_handler
import schemas


class TestTreeExecutor(unittest.TestCase):

    def test_is_input_node_on_input_node(self):
        tree = TreeExecutor([], {})
        self.assertEqual(tree.is_input_node("I1"), True)

    def test_is_input_node_on_operand(self):
        tree = TreeExecutor([], {})
        self.assertEqual(tree.is_input_node("+"), False)

    def test_is_input_node_on_constant(self):
        tree = TreeExecutor([], {})
        self.assertEqual(tree.is_input_node("3.14159"), False)

    def test_is_operand_on_operand(self):
        tree = TreeExecutor([], {})
        self.assertEqual(tree.is_operand("+"), True)

    def test_is_operand_on_input(self):
        tree = TreeExecutor([], {})
        self.assertEqual(tree.is_operand("I1"), False)

    def test_is_operand_on_constant(self):
        tree = TreeExecutor([], {})
        self.assertEqual(tree.is_operand("3.14159"), False)

    def test_get_input(self):
        tree = TreeExecutor([], {})
        self.assertEqual(tree.get_input("I1", [1, 2, 3]), 2)

    def test_operate_addition(self):
        tree = TreeExecutor([], {})
        self.assertEqual(tree.operate(1, 2, "+"), 3)

    def test_operate_division_safety(self):
        tree = TreeExecutor([], {})
        self.assertEqual(tree.operate(1, 0, "%"), 0)


class TestHandler(unittest.TestCase):
    def test_handler_output_values(self):
        # We're going to test (I0 + 2) * I1:
        gene = ["I0", "2", "+", "I1", "*"]
        inputs = [3, 4]
        event = {
            "cases": [
                {
                    "case_metadata": {},
                    "case_input": inputs
                }
            ],
            "individual": gene,
            "config": {}
        }
        result = lambda_handler(event, {})
        # Need to unwrap a bit:
        output = result["cases"][0]["case_output"][0]
        self.assertAlmostEqual(output, 20.0)

    def test_handler_output_schema(self):
        # We're going to test (I0 + 2) * I1:
        gene = ["I0", "2", "+", "I1", "*"]
        inputs = [3, 4]
        event = {
            "cases": [
                {
                    "case_metadata": {},
                    "case_input": inputs
                }
            ],
            "individual": gene,
            "config": {}
        }
        result = lambda_handler(event, {})
        validate(event=result, schema=schemas.OUTPUT)


if __name__ == '__main__':
    unittest.main()
