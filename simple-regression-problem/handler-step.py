
def measure_fitness(case):
    # An output will have:
    case_output = case["case_output"]
    case_metadata = case["case_metadata"]
    input = case_metadata["input"]
    # Now, the metadata we attached is a single value,
    # but outputs is an array of 1, so:
    fitness = abs(input - case_output[0])
    # We need to format it:
    return {
        "case_id": str(input),
        "fitness": fitness
    }


def step(event, context):
    # Step will receive the latest output,
    # and should step the world, and either:
    # a) Return a new set of input cases
    # b) Return isFinished with cases/fitnesses
    # For this problem, we sent all our inputs in the first set, so:
    cases = event["cases"]
    fitnesses = [measure_fitness(case) for case in cases]
    return {
        "isFinished": True,
        "fitnesses": fitnesses,
        "individual": event["individual"],
        "config": event["config"]
    }
