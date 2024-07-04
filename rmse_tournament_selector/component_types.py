from typing import TypedDict, Any, Dict


class RMSETournamentSelectorConfig(TypedDict):
    tournament_size: int


class Config(TypedDict):
    rmse_tournament_selector: RMSETournamentSelectorConfig


class RMSETournamentSelectorEvent(TypedDict):
    config: Config
    metadata: Any
    population: Dict[str, Any]
    fitnesses: Dict[str, Dict[str, float]]
