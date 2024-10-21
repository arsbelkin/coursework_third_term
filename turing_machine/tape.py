class DoubleLinkedList:
    class Node:
        def __init__(self, value=None, prev=None, next=None) -> None:
            self.value = value
            self.prev = prev
            self.next = next

        def __str__(self) -> str:
            return str(self.value)

    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.len = 0

    def is_empty(self):
        return not self.__len

    def push_front(self, value=None) -> None:
        node = self.Node(value=value)
        node.next = self.head
        if self.head is not None:
            self.head.prev = node
        if self.tail is None:
            self.tail = node
        self.head = node
        self.len += 1

    def push_back(self, value=None) -> None:
        node = self.Node(value=value)
        node.prev = self.tail
        if self.head is None:
            self.head = node
        if self.tail is not None:
            self.tail.next = node
        self.tail = node
        self.len += 1

    def pop_front(self) -> Node:
        if self.head is None:
            return

        node = self.head
        if self.head.next is not None:
            self.head.next.prev = None
        else:
            self.tail = None
        self.head = self.head.next
        self.len -= 1

        return node

    def pop_back(self) -> Node:
        if self.tail is None:
            return

        node = self.tail
        if self.tail.prev is not None:
            self.tail.prev.next = None
        else:
            self.head = None
        self.tail = self.tail.prev
        self.len -= 1

        return node

    def get_node(self, index: int) -> Node:
        node = self.head
        n = 0

        while n != index:
            if node is None:
                return node
            node = node.next
            n += 1

        return node

    def __getitem__(self, index: int) -> Node:
        return self.get_node(index)

    def insert(self, index: int, value) -> Node:
        right = self.get_node(index)
        if right is None:
            return self.push_back(value=value)

        left = right.prev
        if left is None:
            return self.push_front(value=value)

        node = self.Node(value=value)
        node.prev = left
        node.next = right
        left.next = node
        right.prev = node

        return node

    def erase(self, index: int) -> Node:
        node = self.get_node(index)
        if node is None:
            return

        if node.prev is None:
            return self.pop_front()

        if node.next is None:
            return self.pop_back()

        left = node.prev
        right = node.next
        left.next = right
        right.prev = left

        return node

    def clear(self) -> None:
        while self.head is not None:
            self.pop_front()

    def print_list(self) -> None:
        current_node = self.head

        while current_node:
            print(
                current_node.value if current_node.value is not None else "_", end=" "
            )
            current_node = current_node.next
        print()

    def __str__(self):
        current_node = self.head
        result = ""
        while current_node:
            result += (
                current_node.value if current_node.value is not None else "_"
            ) + " "
            current_node = current_node.next
        return result
