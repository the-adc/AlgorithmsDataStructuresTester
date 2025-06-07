class AVLTree:
    class Node:
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None
            self.height = 1

    def __init__(self):
        self.root = None

    def height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))

        # Return new root
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        # Return new root
        return y

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        # Perform normal BST insertion
        if not node:
            return self.Node(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node  # Duplicate keys not allowed

        # Update height
        node.height = 1 + max(self.height(node.left), self.height(node.right))

        # Rebalance if needed
        balance = self.get_balance(node)

        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def pre_order(self):
        self._pre_order(self.root)
        print()

    def _pre_order(self, node):
        if node:
            print(node.key, end=" ")
            self._pre_order(node.left)
            self._pre_order(node.right)

    def visualize(self):
        """Simple text visualization of the tree"""
        lines, *_ = self._visualize_aux(self.root)
        for line in lines:
            print(line)

    def _visualize_aux(self, node):
        """Returns list of strings, width, height, and horizontal coordinate of the root"""
        # No child
        if node.right is None and node.left is None:
            line = f"{node.key}({node.height})"
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child
        if node.right is None:
            lines, n, p, x = self._visualize_aux(node.left)
            s = f"{node.key}({node.height})"
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child
        if node.left is None:
            lines, n, p, x = self._visualize_aux(node.right)
            s = f"{node.key}({node.height})"
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children
        left, n, p, x = self._visualize_aux(node.left)
        right, m, q, y = self._visualize_aux(node.right)
        s = f"{node.key}({node.height})"
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


# Example usage
if __name__ == "__main__":
    avl = AVLTree()
    keys = [10, 20, 30, 40, 50, 25]
    
    print("Inserting keys:", keys)
    for key in keys:
        avl.insert(key)
    
    print("\nPreorder traversal:")
    avl.pre_order()
    
    print("\nTree structure:")
    avl.visualize()