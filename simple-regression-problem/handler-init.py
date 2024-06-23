
def make_case(input):
    return {
        # Case metadata can be anything we want.
        # The program *must* return it as it, and not look at it
        # Here, we're going to return the input to evaluate fitness later
        "case_metadata": {
            "input": input
        },
        # Case input is what's fed to the GP program
        # We will *NOT* get this back
        "case_input": [input]
    }


def init(event, context):
    # Initialize should set up anything needed for measuring an individual
    # (ex: regression problems, set up the world)
    # And also return the first set of test cases for the problem.
    # Here, we're going to use the example from:
    #   "Genetic Programming An Introduction" by Wolfgang Banzhaf et al
    # Which is the function x^2 / 2 for the input range [0.0, 1.0)
    case_inputs = [x / 10.0 for x in range(0, 10, 1)]
    cases = [make_case(input) for input in case_inputs]
    return {
        "cases": cases,
        "individual": event["individual"],
        "config": event["config"]
    }

