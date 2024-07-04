from __future__ import annotations
from typing import Union


class TreeNode():
    left_child: Union["TreeNode", None]
    right_child: Union["TreeNode", None]
    token: str

    def is_input_node(self) -> bool:
        return self.token.startswith("I")

    def is_operand(self) -> bool:
        return self.token in ["+", "-", "*", "%"]
    
    def is_leaf_node(self) -> bool:
        return not self.is_operand()
    
    def size(self) -> int:
        if self.is_leaf_node():
            return 1
        else:
            return 1 + self.left_child.size() + self.right_child.size()

    def get_child(self, child_idx: int) -> TreeNode:
        # Event though the representation is postfix,
        # Our indexing here is going to be infix
        # First, are we by ourselves?
        if self.is_leaf_node():
            return self
        # Ok, so we have children
        left_size = self.left_child.size()
        if child_idx < left_size:
            return self.left_child.get_child(child_idx)
        elif child_idx == left_size:
            return self
        else:
            # It's in the right hand tree
            # So subtract out the size:
            child_idx -= left_size
            return self.right_child.get_child(child_idx)

    def set_child(self, child_idx: int, node: TreeNode) -> TreeNode:
        # Ok, we need to replace a subtree
        if self.is_leaf_node():
            # Replacing all of us:
            return node
        # Ok, so we have children
        left_size = self.left_child.size()
        if child_idx < left_size:
            self.left_child = self.left_child.set_child(child_idx, node)
            return self
        elif child_idx == left_size:
            # Replacing all of us:
            return node
        else:
            # It's in the right hand tree
            # So subtract out the size:
            child_idx -= left_size
            self.right_child = self.right_child.set_child(child_idx, node)
            return self

    def to_postfix(self) -> list[str]:
        if self.is_leaf_node:
            return [self.token]
        else:
            return (
                self.left_child.to_postfix() +
                self.right_child.to_postfix() +
                [self.token]
            )


class TreeParser:
    @staticmethod
    def parse(postfix_str: list[str]) -> TreeNode:
        # Go through the list:
        stack: list[TreeNode] = []
        for token in postfix_str:
            node = TreeNode()
            node.token = token
            # Are we an operand?
            if node.is_operand():
                # Pop two off the stack:
                node.right_child = stack.pop()
                node.left_child = stack.pop()
            stack.append(node)
        return stack.pop()
