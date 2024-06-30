INPUT = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://shalmezad.com/github/lambdagp-test/tree-builder/input-schema.json",  # noqa: E501
    "title": "Tree GP Input",
    "description": "Input validation schema for tree GP builder",
    "type": "object",
    "required": ["config"],
    "properties": {
        "config": {
            "type": "object",
            "required": ["tree_max_depth", "num_inputs"],
            "properties": {
                "tree_max_depth": {
                    "type": "integer",
                    "minimum": 1
                },
                "num_inputs": {
                    "type": "integer",
                    "minimum": 1
                }
            }
        }
    },
    "examples": [
        {
            "config": {
                "max_tree_depth": 4,
                "num_inputs": 2
            }
        }
    ],
}

OUTPUT = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://shalmezad.com/github/lambdagp-test/tree-builder/output-schema.json",  # noqa: E501
    "title": "Tree GP Output",
    "description": "Output validation schema for tree GP builder",
    "type": "object",
    "required": ["individual"],
    "properties": {
        "individual": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
    },
    "examples": [
        {
            "individual": ["I0", "2", "+", "I1", "*"],
            "config": {}
        }
    ],
}
