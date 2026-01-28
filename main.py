import threading


class MinHeap:
    def __init__(self):
        self.heap = []
        self.lock = threading.Lock()

    def insert(self, word):
        with self.lock:
            self.heap.append(word)
            index = len(self.heap) - 1
            while index > 0:
                parent = (index - 1) // 2
                if self.heap[index][1] < self.heap[parent][1]:
                    self.heap[index], self.heap[parent] = (
                        self.heap[parent],
                        self.heap[index],
                    )
                    index = parent
                else:
                    break
        return "Word inserted"

    def extract(self):
        with self.lock:
            if not self.heap:
                return None
            if len(self.heap) == 1:
                return self.heap.pop()
            kicked_out = self.heap[0]
            self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
            self.heap.pop()
            index = 0
            while index < len(self.heap):
                left = 2 * index + 1
                right = 2 * index + 2
                smallest = index
                if (
                    left < len(self.heap)
                    and self.heap[smallest][1] > self.heap[left][1]
                ):
                    smallest = left
                if (
                    right < len(self.heap)
                    and self.heap[smallest][1] > self.heap[right][1]
                ):
                    smallest = right
                if smallest == index:
                    break
                self.heap[smallest], self.heap[index] = (
                    self.heap[index],
                    self.heap[smallest],
                )
                index = smallest
        return kicked_out

    def peek(self):
        with self.lock:
            if not self.heap:
                return None
            return self.heap[0]

    def heapify(self, words):
        with self.lock:
            parent = (len(words) - 2) // 2
            for i in range(parent, -1, -1):
                index = i
                while True:
                    left = 2 * index + 1
                    right = 2 * index + 2
                    smallest = index
                    if left < len(words) and words[smallest][1] > words[left][1]:
                        smallest = left
                    if right < len(words) and words[smallest][1] > words[right][1]:
                        smallest = right
                    if smallest == index:
                        break
                    words[smallest], words[index] = words[index], words[smallest]
                    index = smallest
        index_mapping = dict()
        for i, (word, frequency) in enumerate(words):
            index_mapping[word] = i
        return words, index_mapping


class Node:
    def __init__(self):
        self.children = dict()
        self.is_end_of_word = False
        self.top_k = MinHeap()
        self.index_mapping = dict()


class Trie:
    def __init__(self):
        self.root = Node()
        self.frequency = dict()
        self.lock = threading.Lock()

    def insert(self, word):
        with self.lock:
            if word not in self.frequency:
                self.frequency[word] = 1
                current = self.root
                for char in word:
                    if char not in current.children:
                        current.children[char] = Node()
                    if len(current.top_k.heap) < 10:
                        current.top_k.insert((word, 1))
                        current.index_mapping[word] = len(current.top_k.heap) - 1
                    current = current.children[char]
                current.is_end_of_word = True
                return "Word Inserted"
            return "Word already exists"

    def delete(self, word):
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_end_of_word:
                    return False
                node.is_end_of_word = False
                return len(node.children) == 0
            char = word[depth]
            if char not in node.children:
                return False
            if word in node.index_mapping:
                index = node.index_mapping[word]
                del node.top_k.heap[index]
                del node.index_mapping[word]
                node.top_k.heap, node.index_mapping = node.top_k.heapify(
                    node.top_k.heap
                )
            delete_child = _delete(node.children[char], word, depth + 1)
            if delete_child:
                del node.children[char]
                return (not node.is_end_of_word) and (len(node.children) == 0)
            return False

        with self.lock:
            if word not in self.frequency:
                return "Word does not exist"
            _delete(self.root, word, 0)
            del self.frequency[word]
            return True


class AutoCompleteEngine:
    def __init__(self):
        self.t = Trie()

    def insert(self, word):
        return self.t.insert(word)

    def select(self, word):
        with self.t.lock:
            if word not in self.t.frequency:
                return "Word does not exist"
            self.t.frequency[word] += 1
            current = self.t.root
            if word in current.index_mapping:
                for char in word:
                    index = current.index_mapping[word]
                    current.top_k.heap[index] = (word, self.t.frequency[word])
                    while True:
                        left = 2 * index + 1
                        right = 2 * index + 2
                        smallest = index
                        if (
                            left < len(current.top_k.heap)
                            and current.top_k.heap[smallest][1]
                            > current.top_k.heap[left][1]
                        ):
                            smallest = left
                        if (
                            right < len(current.top_k.heap)
                            and current.top_k.heap[smallest][1]
                            > current.top_k.heap[right][1]
                        ):
                            smallest = right
                        if smallest == index:
                            break
                        current.top_k.heap[smallest], current.top_k.heap[index] = (
                            current.top_k.heap[index],
                            current.top_k.heap[smallest],
                        )
                        current.index_mapping[current.top_k.heap[smallest][0]] = (
                            smallest
                        )
                        current.index_mapping[current.top_k.heap[index][0]] = index
                        index = smallest
                    current = current.children[char]
                return "Word Selected"
            lowest_frequency = current.top_k.peek()[1]
            if lowest_frequency < self.t.frequency[word]:
                for char in word:
                    _ = current.top_k.extract()
                    _ = current.top_k.insert((word, self.t.frequency[word]))
                    current.index_mapping = dict()
                    for i, (w, _) in enumerate(current.top_k.heap):
                        current.index_mapping[w] = i
                    current = current.children[char]
                return "Word Selected"
        return "Word Selected"

    def delete(self, word):
        return self.t.delete(word)

    def search(self, prefix, k=None):
        current = self.t.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]
        if not k:
            return sorted(
                (word for (word, _) in current.top_k.heap),
                key=lambda x: -self.t.frequency[x],
            )
        return sorted(
            (word for (word, _) in current.top_k.heap),
            key=lambda x: -self.t.frequency[x],
        )[: min(k, len(current.top_k.heap))]


engine = AutoCompleteEngine()

# Insert words
print(engine.insert("cat"))  # Word Inserted
print(engine.insert("car"))  # Word Inserted
print(engine.insert("cart"))  # Word Inserted
print(engine.insert("dog"))  # Word Inserted
print(engine.insert("catalog"))  # Word Inserted
print(engine.insert("cater"))  # Word Inserted
print(engine.insert("do"))  # Word Inserted
print(engine.insert("dove"))  # Word Inserted
print(engine.insert("carton"))  # Word Inserted
print(engine.insert("carpet"))  # Word Inserted
print(engine.insert("car"))  # Word already exists

# Select (increase frequency) and test ranking
print(engine.select("car"))  # Word Selected
print(engine.select("car"))  # Word Selected
print(engine.select("cart"))  # Word Selected
print(engine.select("cart"))  # Word Selected
print(engine.select("catalog"))  # Word Selected
print(engine.select("catalog"))  # Word Selected
print(engine.select("catalog"))  # Word Selected
print(engine.select("cat"))  # Word Selected

# Delete a word and check
print(engine.delete("cater"))  # True
print(engine.delete("cater"))  # Word does not exist

# Try to select a word that doesn't exist
print(engine.select("cater"))  # Word does not exist

# Try to delete a word that doesn't exist
print(engine.delete("caterpillar"))  # Word does not exist

# Insert after delete and check
print(engine.insert("cater"))  # Word Inserted

# Insert more than 10 words to test heap size limit
print(engine.insert("cab"))  # Word Inserted
print(engine.insert("cape"))  # Word Inserted
print(engine.insert("cap"))  # Word Inserted
print(engine.insert("can"))  # Word Inserted
print(engine.insert("cane"))  # Word Inserted

# Search for top-k for prefix 'ca'
print(
    engine.search("ca")
)  # ['catalog', 'cart', 'car', 'cat', 'carton', 'carpet', 'cater', 'cab', 'cape', 'cap']

# Search for a prefix with no matches
print(engine.search("z"))  # []

# Search for a prefix with only one match
print(engine.search("cata"))  # ['catalog']

# Search with k parameter
print(engine.search("ca", k=3))  # ['catalog', 'cart', 'car']

# Manual inspection of top_k heap at root and a prefix node
print("Root top_k:", engine.t.root.top_k.heap)
current = engine.t.root
for char in "ca":
    current = current.children[char]
print("Prefix 'ca' top_k:", current.top_k.heap)
