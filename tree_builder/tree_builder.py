from __future__ import annotations
from abc import ABC, abstractmethod
import random
import uuid

from aws_lambda_powertools.utilities.validation import validator

import schemas
from component_types import TreeBuilderEvent, TreeBuilderConfig


class TreeNode(ABC):

    @abstractmethod
    def to_postfix(self) -> list[str]:
        pass


class InputTreeNode(TreeNode):
    def __init__(self, input_idx: int):
        self.input_idx = input_idx

    def to_postfix(self) -> list[str]:
        return [("I" + str(self.input_idx))]


class ConstantTreeNode(TreeNode):
    def __init__(self, node_value: float):
        self.node_value = node_value

    def to_postfix(self) -> list[str]:
        return [str(self.node_value)]


class OperationNode(TreeNode):
    def __init__(
            self,
            left_tree: TreeNode,
            right_tree: TreeNode,
            operator: str):
        self.left_node = left_tree
        self.right_node = right_tree
        self.operator = operator

    def to_postfix(self) -> list[str]:
        return (
                self.left_node.to_postfix() +
                self.right_node.to_postfix() +
                [self.operator]
            )


class TreeBuilder:

    def __init__(self, config: TreeBuilderConfig) -> None:
        self.config = config

    def build(self) -> list[str]:
        # Alright, so let's start with a root note:
        tree = self.make_sub_tree(depth=0)
        # We have to convert to postfix:
        return tree.to_postfix()

    def make_sub_tree(self, depth) -> TreeNode:
        if depth == self.config["max_tree_depth"]:
            # We hit max depth, we *MUST* return a terminal node:
            # Which is either an input or a constant:
            is_input = random.choice([True, False])
            if is_input:
                return self.random_input_node()
            else:
                # It's a constant:
                return self.random_constant_node()
        else:
            # Pick a node type:
            node_type = random.choice(["input", "constant", "operation"])
            if node_type == "input":
                return self.random_input_node()
            elif node_type == "constant":
                return self.random_constant_node()
            else:
                return self.random_operation_node(depth)

    def random_operation_node(self, depth) -> OperationNode:
        left_node = self.make_sub_tree(depth + 1)
        right_node = self.make_sub_tree(depth + 1)
        operator = random.choice(["+", "-", "*", "%"])
        node = OperationNode(left_node, right_node, operator)
        return node

    def random_constant_node(self) -> ConstantTreeNode:
        node = ConstantTreeNode(random.random() * 10.0)
        return node

    def random_input_node(self) -> InputTreeNode:
        input_idx = random.randint(0, self.config["num_inputs"] - 1)
        node = InputTreeNode(input_idx)
        return node


@validator(inbound_schema=schemas.INPUT)
def lambda_handler(event: TreeBuilderEvent, context):
    """Builds a single individual, returns in event["individuals"]"""
    config = event["config"]
    metadata = event["metadata"]
    # Make our tree:
    treeBuilder = TreeBuilder(event["config"]["tree_builder"])
    tree = treeBuilder.build()
    tree_id = str(uuid.uuid4())
    return {
        "config": config,
        "metadata": metadata,
        "individuals": {
            tree_id: tree
        }
    }
