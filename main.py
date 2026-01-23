import threading


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None


class Cache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.lock = threading.RLock()
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def set(self, key, value):
        with self.lock:
            if len(self.cache) < self.capacity or key in self.cache:
                if key not in self.cache:
                    node = Node(key, value)
                    self.cache[key] = node
                    if self.head.next == self.tail:
                        self.head.next = node
                        self.tail.prev = node
                        node.next = self.tail
                        node.prev = self.head
                        t = self.traverse()
                        print(t)
                        return f"Set Key '{key}' with value '{value}'"
                    else:
                        self._move_node_to_head(node, disconnect=False)
                        t = self.traverse()
                        print(t)
                        return f"Set Key '{key}' with value '{value}'"
                else:
                    node = self.cache[key]
                    node.value = value
                    if node.prev == self.head:
                        t = self.traverse()
                        print(t)
                        return f"Set Key '{key}' with value '{value}'"
                    self._move_node_to_head(node)
                    t = self.traverse()
                    print(t)
                    return f"Set Key '{key}' with value '{value}'"
            else:
                old_key = self.tail.prev.key
                temp = self.tail.prev
                temp.prev.next = self.tail
                self.tail.prev = temp.prev
                del self.cache[old_key]
                node = Node(key, value)
                self.cache[key] = node
                self._move_node_to_head(node, disconnect=False)
                t = self.traverse()
                print(t)
                return f"Set Key '{key}' with value '{value}'"

    def get(self, key):
        with self.lock:
            if key not in self.cache:
                return "Key does not exist"
            node = self.cache[key]
            data = node.value
            if node.prev == self.head:
                return data
            self._move_node_to_head(node)
            t = self.traverse()
            print(t)
            return data

    def delete(self, key):
        with self.lock:
            if key not in self.cache:
                t = self.traverse()
                print(t)
                return "Key does not exist"
            node = self.cache[key]
            node.next.prev = node.prev
            node.prev.next = node.next
            del self.cache[key]
            t = self.traverse()
            print(t)
            return "Key deleted"

    def _move_node_to_head(self, node, disconnect=True):
        if disconnect:
            node.next.prev = node.prev
            node.prev.next = node.next
        node.next = self.head.next
        node.prev = self.head
        node.next.prev = node
        self.head.next = node

    def traverse(self):
        with self.lock:
            current = self.head.next
            temp = []
            while current != self.tail:
                temp.append(current.key)
                current = current.next
            return " <-> ".join(temp)


cache = Cache(3)
print(cache.set("a", 1))
print(cache.set("b", 2))
print(cache.set("c", 3))
print(cache.get("a"))
print(cache.set("d", 4))
print(cache.get("b"))
print(cache.get("c"))
print(cache.get("d"))
print(cache.set("c", 33))
print(cache.get("c"))
print(cache.delete("a"))
print(cache.get("a"))
print(cache.delete("x"))
print(cache.set("e", 5))
print(cache.get("d"))
print(cache.get("e"))
print(cache.get("c"))

print(cache.set("e", 55))
print(cache.get("e"))
print(cache.set("f", 6))
print(cache.get("c"))
print(cache.get("f"))
print(cache.delete("f"))
print(cache.get("f"))
print(cache.set("g", 7))
print(cache.get("e"))
print(cache.get("g"))
