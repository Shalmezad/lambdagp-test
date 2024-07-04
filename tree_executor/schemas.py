INPUT = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://shalmezad.com/github/lambdagp-test/tree-executor/input-schema.json",  # noqa: E501
    "title": "Tree GP Input",
    "description": "Input validation schema for tree GP executor",
    "type": "object",
    "required": ["individual", "cases"],
    "properties": {
        "individual": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "cases": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["case_input", "case_metadata"],
                "properties": {
                    "case_input": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        }
                    },
                    "case_metadata": {
                        "type": "object"
                    }
                }
            }
        }
    },
    "examples": [
        {
            "cases": [
                {
                    "case_metadata": {
                        "foo": "bar"
                    },
                    "case_input": [0.5, 0.7]
                }
            ],
            "individual": ["I0", "2", "+", "I1", "*"],
            "config": {}
        }
    ],
}

OUTPUT = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://shalmezad.com/github/lambdagp-test/tree-executor/output-schema.json",  # noqa: E501
    "title": "Tree GP Output",
    "description": "Output validation schema for tree GP executor",
    "type": "object",
    "required": ["individual", "cases"],
    "properties": {
        "individual": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "cases": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["case_output", "case_metadata"],
                "properties": {
                    "case_output": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        }
                    },
                    "case_metadata": {
                        "type": "object"
                    }
                }
            }
        }
    },
    "examples": [
        {
            "cases": [
                {
                    "case_metadata": {
                        "foo": "bar"
                    },
                    "case_output": [0.5, 0.7]
                }
            ],
            "individual": ["I0", "2", "+", "I1", "*"],
            "config": {}
        }
    ],
}
