# LRU Cache Implementation in Python

This project provides a thread-safe Least Recently Used (LRU) cache implementation using a doubly linked list and a hash map (dictionary) in Python.

## Features
- O(1) time complexity for set, get, and delete operations
- Automatic eviction of the least recently used item when the cache is full
- Thread-safe using `threading.RLock`
- Includes a test suite at the bottom of `main.py` to demonstrate cache behavior
- Internal state printing for debugging and understanding cache order

## How It Works
- The cache uses a doubly linked list to maintain the order of usage (most recently used at the head, least at the tail).
- A dictionary maps keys to their corresponding nodes for O(1) access.
- When the cache reaches its capacity, the least recently used item is evicted.
- All operations are thread-safe.

## Usage
1. Clone or download this repository.
2. Run the main file:
   ```bash
   python main.py
   ```
3. Observe the printed output and cache state transitions after each operation.

## Customization
- You can change the cache capacity by modifying the argument to `Cache()` in `main.py`.
- Add or modify test cases at the bottom of `main.py` to further explore cache behavior.

## License
This project is provided for educational purposes and has no specific license.
# LRU-Cache-Implementation-in-Python
