INPUT = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://shalmezad.com/github/lambdagp-test/cgp_builder/input-schema.json",  # noqa: E501
    "title": "CGP Builder Input",
    "description": "Input validation schema for the CGP Builder",
    "type": "object",
    "required": ["config"],
    "properties": {
        "config": {
            "type": "object",
            "required": ["cgp_builder"],
            "properties": {
                "cgp_builder": {
                    "type": "object",
                    "required": [
                        "num_inputs",
                        "num_middle_nodes",
                        "num_outputs",
                        "instruction_set_length"],
                    "properties": {
                        "num_inputs": {
                            "type": "integer",
                            "minimum": 1
                        },
                        "num_middle_nodes": {
                            "type": "integer",
                            "minimum": 1
                        },
                        "num_outputs": {
                            "type": "integer",
                            "minimum": 1
                        },
                        "instruction_set_length": {
                            "type": "integer",
                            "minimum": 1
                        }
                    }
                }
            }
        }
    }
}
