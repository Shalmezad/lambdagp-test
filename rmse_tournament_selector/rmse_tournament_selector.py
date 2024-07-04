from math import sqrt
import random
from typing import Dict

from component_types import RMSETournamentSelectorEvent


def get_rmse(fitnesses: Dict[str, float]):
    # Assume each value is an abs error:
    count = 0
    sum = 0
    for case_id in fitnesses:
        count += 1
        sum += pow(fitnesses[case_id], 2)
    return sqrt(sum/count)


def lambda_handler(event: RMSETournamentSelectorEvent, context):
    # Grab our config:
    config = event["config"]
    tournament_size = config["rmse_tournament_selector"]["tournament_size"]
    # Get our list of ids:
    ids = list(event["population"].keys())
    # Get a subset:
    tournament_ids = random.sample(ids, k=tournament_size)
    # Go through and pick the smallest rmse:
    best_id = None
    best_rmse = None
    fitnesses = event["fitnesses"]
    for indv_id in tournament_ids:
        rmse_value = get_rmse(fitnesses[indv_id])
        if not best_rmse or rmse_value <= best_rmse:
            best_rmse = rmse_value
            best_id = indv_id
    # At this point, we have our best:
    return {
        "config": config,
        "metadata": event["metadata"],
        "parents": {
            best_id: event["population"][best_id]
        }
    }
