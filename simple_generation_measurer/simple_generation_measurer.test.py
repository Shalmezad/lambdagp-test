import unittest
from simple_generation_measurer import handle_generation_runner_event


class TestHandleGenerationRunnerEvent(unittest.TestCase):
    def test_leaves_existing_noncomponent_metadata(self):
        existing_metadata = {
            "foo": "bar"
        }
        event = {
            "config": {},
            "metadata": existing_metadata,
            "population": {
                "some": "indv"
            }
        }
        result = handle_generation_runner_event(event)
        self.assertEqual(result["metadata"]["foo"], "bar")

    def test_adds_metadata(self):
        event = {
            "config": {},
            "metadata": {},
            "population": {
                "foo": "bar"
            }
        }
        result = handle_generation_runner_event(event)
        result_meta = result["metadata"]["simple_generation_measurer"]
        self.assertEqual(result_meta["population"]["foo"], "bar")
        self.assertEqual(result_meta["fitnesses"], {})


if __name__ == '__main__':
    unittest.main()
