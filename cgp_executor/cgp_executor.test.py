import unittest
from cgp_executor import CGPExecutor


class TestCGPExecutorGetNode(unittest.TestCase):
    def test_get_input_node(self):
        config = {
            "cgp_executor": {
                "num_inputs": 3,
                "num_middle_nodes": 2,
                "num_outputs": 2
            }
        }
        gene = []
        executor = CGPExecutor(gene, config)
        result = executor.get_node(0, [3.14, 7.77, 9.00])
        self.assertAlmostEqual(result, 3.14)

    def test_get_middle_node(self):
        config = {
            "cgp_executor": {
                "num_inputs": 3,
                "num_middle_nodes": 2,
                "num_outputs": 2,
                "instruction_set": ["+"]
            }
        }
        # Input 0, input 1, op +
        gene = [[0, 1, 0]]
        executor = CGPExecutor(gene, config)
        result = executor.get_node(3, [3.14, 2.00, 9.00])
        self.assertAlmostEqual(result, 5.14)



if __name__ == '__main__':
    unittest.main()
