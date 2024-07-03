from typing import TypedDict, Any


class TreeBuilderConfig(TypedDict):
    max_tree_depth: int
    num_inputs: int


class Config(TypedDict):
    tree_builder: TreeBuilderConfig


class TreeBuilderEvent(TypedDict):
    config: Config
    metadata: Any
