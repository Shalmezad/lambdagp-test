import sys
if sys.version_info < (3, 11):
    from typing_extensions import TypedDict, Any, Dict, NotRequired, List
else:
    from typing import TypedDict, Any, Dict, NotRequired, List


class SimpleRegressionProblemEvent(TypedDict):
    config: Any
    metadata: Any
    # Two possible types of events:
    # 1) Coming from Generation Measurer:
    individuals: NotRequired[Dict[str, Any]]
    # 2) Coming from Individual Executor:
    case_results: NotRequired[Dict[str, Dict[str, List[float]]]]
