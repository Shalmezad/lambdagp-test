from typing import List, TypedDict, Any, Dict, NotRequired


class SimpleRegressionProblemEvent(TypedDict):
    config: Any
    metadata: Any
    # Two possible types of events:
    # 1) Coming from Generation Measurer:
    individuals: NotRequired[Dict[str, Any]]
    # 2) Coming from Individual Executor:
    case_results: NotRequired[Dict[str, Dict[str, List[float]]]]
