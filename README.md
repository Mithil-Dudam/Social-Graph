# Trie-based Autocomplete Engine with Per-Node Top-K Min-Heaps

## Overview

This project implements a scalable, thread-safe autocomplete engine using a Trie data structure. Each Trie node maintains a min-heap to efficiently track the top-k most frequent words for every prefix. The engine supports fast insert, select (frequency update), delete, and search (autocomplete) operations.

---

## Features

- **Efficient Insert:** Add new words to the Trie and update per-node top-k heaps.
- **Autocomplete Search:** Instantly retrieve the most frequent completions for any prefix.
- **Frequency Ranking:** Selecting a word increases its frequency, affecting its ranking in suggestions.
- **Delete:** Remove words from the Trie and update all relevant heaps.
- **Thread Safety:** All operations are protected by locks for concurrent use.
- **Configurable Top-K:** Each node maintains a heap of up to 10 most frequent words (can be adjusted).

---

## How It Works

- **Trie Structure:** Each node represents a prefix and has children for each possible next character.
- **Min-Heap at Each Node:** Stores up to k words with the highest frequencies for that prefix.
- **Index Mapping:** Allows fast updates and lookups in the heap.
- **Insert/Select:** Update the heap at every node along the word's path.
- **Delete:** Remove the word from all relevant heaps and the Trie.

---

## Usage

### Example

```python
engine = AutoCompleteEngine()

# Insert words
engine.insert("cat")
engine.insert("car")
engine.insert("cart")
engine.insert("catalog")

# Select (increase frequency)
engine.select("car")
engine.select("car")
engine.select("cart")

# Autocomplete search
print(engine.search("ca"))      # ['catalog', 'cart', 'car', 'cat']

# Delete a word
engine.delete("cat")

# Search with k parameter
print(engine.search("ca", k=2)) # ['catalog', 'cart']
```

---

## Test Cases

The project includes comprehensive test cases that cover:

- Insertion (including duplicates)
- Frequency updates and ranking
- Deletion (existing and non-existing words)
- Heap size limit (top-k)
- Edge cases (re-insertion after deletion, selecting/deleting non-existent words)
- Search/autocomplete for various prefixes
- Search with `k` parameter
- Manual inspection of per-node top-k heaps

---

## Time Complexity

- **Insert:** $O(n \log k)$
- **Select:** $O(n \log k)$
- **Delete:** $O(n \log k)$
- **Search:** $O(n + k \log k)$

Where $n$ is the length of the word/prefix and $k$ is the heap size (default 10).

---

## Notes

- For most real-world autocomplete use cases, $k$ is small (e.g., 10).
- The engine is thread-safe and suitable for concurrent environments.
- For very large $k$, consider memory and performance trade-offs.

---

## License

MIT License

---

## Author

Mithil
# Trie-based-Autocomplete-Engine-with-Per-Node-Top-K-Min-Heaps
