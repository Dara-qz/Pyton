class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def rotate_right(self, root):
        left_child = root.left
        temp = left_child.right

        left_child.right = root
        root.left = temp

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        left_child.height = 1 + max(self.get_height(left_child.left), self.get_height(left_child.right))

        return left_child

    def rotate_left(self, root):
        right_child = root.right
        temp = right_child.left

        right_child.left = root
        root.right = temp

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        right_child.height = 1 + max(self.get_height(right_child.left), self.get_height(right_child.right))

        return right_child

    def insert(self, root, value):
        if not root:
            return Node(value)

        if value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Left-heavy
        if balance > 1:
            if value < root.left.value:  # Left-left case
                return self.rotate_right(root)
            elif value > root.left.value:  # Left-right case
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)

        # Right-heavy
        if balance < -1:
            if value > root.right.value:  # Right-right case
                return self.rotate_left(root)
            elif value < root.right.value:  # Right-left case
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)

        return root


if __name__ == "__main__":
    avl_tree = AVLTree()
    root = None

    values_to_insert = [20, 4, 15, 70, 50, 80, 10, 5, 3, 25]
    for value in values_to_insert:
        root = avl_tree.insert(root, value)

    print("Висота кореня:", avl_tree.get_height(root))
    print("Баланс кореня:", avl_tree.get_balance(root))
