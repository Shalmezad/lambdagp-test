import unittest
from simple_population_builder import setup_metadata, lambda_handler


class TestSimplePopulationBuilderSetupMetadata(unittest.TestCase):
    def test_leaves_existing_noncomponent_metadata(self):
        existing_metadata = {
            "foo": "bar"
        }
        new_metadata = setup_metadata(existing_metadata)
        self.assertEqual(new_metadata["foo"], "bar")

    def test_creates_initial_metadata(self):
        new_metadata = setup_metadata({})
        self.assertIn("simple_population_builder", new_metadata)
        self.assertIn("population", new_metadata["simple_population_builder"])
        population = new_metadata["simple_population_builder"]["population"]
        self.assertEqual(population, {})

    def test_leaves_existing_component_metadata(self):
        existing_metadata = {
            "simple_population_builder": {
                "population": {
                    "foo": "bar"
                }
            }
        }
        new_metadata = setup_metadata(existing_metadata)
        population = new_metadata["simple_population_builder"]["population"]
        self.assertEqual(population["foo"], "bar")


class TestSimplePopulationBuilderLambdaHandler(unittest.TestCase):
    def test_needs_more_individuals(self):
        event = {
            "config": {
                "simple_population_builder": {
                    "population_size": 3
                }
            }
        }
        result = lambda_handler(event, {})
        self.assertEqual(result["is_done"], False)

    def test_given_full_population(self):
        event = {
            "config": {
                "simple_population_builder": {
                    "population_size": 2
                }
            },
            "individuals": {
                "foo": "bar",
                "biz": "baz"
            }
        }
        result = lambda_handler(event, {})
        # We should be done:
        self.assertEqual(result["is_done"], True)
        # Our population should include the passed individuals:
        self.assertEqual(result["population"], {
            "foo": "bar",
            "biz": "baz"
        })

    def test_cycle(self):
        config = {
            "simple_population_builder": {
                "population_size": 2
            }
        }
        event1 = {
            "config": config,
            "individuals": {
                "foo": "bar"
            }
        }
        result1 = lambda_handler(event1, {})
        # We only have 1 individual:
        self.assertEqual(result1["is_done"], False)
        event2 = {
            # Tack on the metadata, which should include the first individual
            "metadata": result1["metadata"],
            "config": config,
            "individuals": {
                "biz": "baz"
            }
        }
        result2 = lambda_handler(event2, {})
        # We should be done:
        self.assertEqual(result2["is_done"], True)
        # Our population should include the passed individuals:
        self.assertEqual(result2["population"], {
            "foo": "bar",
            "biz": "baz"
        })


if __name__ == '__main__':
    unittest.main()
