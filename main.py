import threading


class Node:
    def __init__(self, user):
        self.user = user
        self.next = None


class Queue:
    def __init__(self):
        self.lock = threading.Lock()
        self.head = None
        self.tail = None

    def enqueue(self, user):
        node = Node(user)
        with self.lock:
            if self.head is None:
                self.head = node
                self.tail = node
                return
            self.tail.next = node
            self.tail = node
            return

    def dequeue(self):
        with self.lock:
            if self.head is None:
                return None
            temp = self.head
            self.head = self.head.next
            temp.next = None
            if self.head is None:
                self.tail = None
            return temp.user


class Graph:
    def __init__(self):
        self.users = dict()
        self.lock = threading.Lock()

    def add_user(self, user):
        with self.lock:
            if user in self.users:
                return "User exists"
            self.users[user] = set()
            return "User Added"

    def remove_user(self, user):
        with self.lock:
            if user not in self.users:
                return "User does not exist"
            for friend in self.users[user]:
                self.users[friend].remove(user)
            del self.users[user]
            return "User Removed"

    def add_friend(self, user, friend):
        with self.lock:
            if user not in self.users or friend not in self.users:
                return "User does not exist"
            if friend in self.users[user]:
                return "Already Friends"
            self.users[user].add(friend)
            self.users[friend].add(user)
            return "Added Friend"

    def remove_friends(self, user, friend):
        with self.lock:
            if user not in self.users or friend not in self.users:
                return "User does not exist"
            if friend not in self.users[user]:
                return "Not Friends"
            self.users[user].remove(friend)
            self.users[friend].remove(user)
            return "Removed Friend"

    def mutual_friends(self, user, friend):
        with self.lock:
            if user not in self.users or friend not in self.users:
                return "User does not exist"
            user_friends = len(self.users[user])
            friend_friends = len(self.users[friend])
            mutuals = []
            if user_friends <= friend_friends:
                for f in self.users[user]:
                    if f in self.users[friend]:
                        mutuals.append(f)
            else:
                for f in self.users[friend]:
                    if f in self.users[user]:
                        mutuals.append(f)
            return mutuals

    def shortest_path(self, user_a, user_b):
        with self.lock:
            if user_a not in self.users or user_b not in self.users:
                return "User does not exist"
            q = Queue()
            q.enqueue((user_a, [user_a]))
            seen = set()
            seen.add(user_a)
            while q.head is not None:
                user = q.dequeue()
                if user[0] == user_b:
                    return " -> ".join(user[1])
                for friend in self.users[user[0]]:
                    if friend not in seen:
                        seen.add(friend)
                        q.enqueue((friend, user[1] + [friend]))

    def friend_recommendations(self, user, k=None):
        with self.lock:
            if user not in self.users:
                return "User does not exist"
            friends_of_friends = dict()
            for friend in self.users[user]:
                for f in self.users[friend]:
                    if f not in self.users[user] and f != user:
                        friends_of_friends[f] = friends_of_friends.get(f, 0) + 1
            recommended_friends = sorted(
                friends_of_friends.items(), key=lambda x: -x[1]
            )
            if k is None:
                return recommended_friends
            return recommended_friends[: min(k, len(recommended_friends))]

    def connected_component(self):
        with self.lock:
            if not self.users:
                return None
            seen = set()
            connected_components = []
            for user in self.users:
                if user not in seen:
                    stack = [user]
                    seen.add(user)
                    component = []
                    component.append(user)
                    while stack:
                        u = stack.pop()
                        for friend in self.users[u]:
                            if friend not in seen:
                                seen.add(friend)
                                stack.append(friend)
                                component.append(friend)
                    connected_components.append(component)
            return connected_components


g = Graph()

# ---- Add users ----
users = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
for u in users:
    print(g.add_user(u))

# ---- Add friendships ----
edges = [
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("B", "D"),
    ("C", "D"),
    ("D", "E"),
    ("E", "F"),
    ("F", "G"),
    ("D", "F"),
    ("H", "I"),
    ("I", "J"),
    ("K", "L"),
]

for u, v in edges:
    print(g.add_friend(u, v))

print("\n--- MUTUAL FRIENDS ---")
print("Mutual A & B:", g.mutual_friends("A", "B"))
print("Mutual B & D:", g.mutual_friends("B", "D"))
print("Mutual D & F:", g.mutual_friends("D", "F"))

print("\n--- SHORTEST PATHS ---")
print("A -> G:", g.shortest_path("A", "G"))
print("C -> F:", g.shortest_path("C", "F"))
print("A -> J:", g.shortest_path("A", "J"))

print("\n--- FRIEND RECOMMENDATIONS ---")
print("Recommendations for A:", g.friend_recommendations("A"))
print("Top 2 for A:", g.friend_recommendations("A", k=2))
print("Recommendations for D:", g.friend_recommendations("D"))

print("\n--- CONNECTED COMPONENTS ---")
print(g.connected_component())

print("\n--- REMOVE EDGE & RETEST ---")
print(g.remove_friends("D", "F"))
print("A -> G after removal:", g.shortest_path("A", "G"))

print("\n--- REMOVE USER & RETEST ---")
print(g.remove_user("E"))
print("Connected components after removing E:")
print(g.connected_component())
