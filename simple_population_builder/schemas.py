INPUT = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://shalmezad.com/github/lambdagp-test/simple_population_builder/input-schema.json",  # noqa: E501
    "title": "Simple Pouplation Builder Input",
    "description": "Input validation schema for the simple population builder",
    "type": "object",
    "required": ["config"],
    "properties": {
        "individuals": {
            "type": "object",
            "minProperties": 1,
        },
        "config": {
            "type": "object",
            "required": ["simple_population_builder"],
            "properties": {
                "simple_population_builder": {
                    "type": "object",
                    "required": ["population_size"],
                    "properties": {
                        "population_size": {
                            "type": "integer",
                            "minimum": 1
                        }
                    }
                }
            }
        }
    }
}
