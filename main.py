import threading
import time
import random


class Node:
    def __init__(self, job):
        self.job = job
        self.next = None


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.lock = threading.RLock()
        self.condition = threading.Condition(self.lock)

    def enqueue(self, job):
        node = Node(job)
        with self.condition:
            if self.head is None:
                self.head = node
                self.tail = node
            else:
                self.tail.next = node
                self.tail = node
            self.condition.notify()

    def dequeue(self, shutdown):
        with self.condition:
            while self.head is None:
                if shutdown.is_set():
                    return None
                self.condition.wait()
            temp = self.head
            self.head = self.head.next
            if self.head is None:
                self.tail = None
        return temp.job


class ThreadPool:
    def __init__(self, num_workers):
        self.num_workers = num_workers
        self.q = Queue()
        self.shutdown_event = threading.Event()
        self.workers = []
        for _ in range(self.num_workers):
            t = threading.Thread(target=self.worker)
            t.start()
            self.workers.append(t)

    def submit(self, job):
        if not self.shutdown_event.is_set():
            self.q.enqueue(job)

    def worker(self):
        while not self.shutdown_event.is_set():
            job = self.q.dequeue(self.shutdown_event)
            if callable(job):
                job()

    def shutdown(self, wait=True):
        self.shutdown_event.set()
        with self.q.condition:
            self.q.condition.notify_all()
        if wait:
            for t in self.workers:
                t.join()


def job():
    sleep_time = random.randint(3, 7)
    print(f"{threading.current_thread().name} Running job for {sleep_time} seconds")
    time.sleep(sleep_time)
    print("Job Done")


pool = ThreadPool(3)


try:
    while True:
        user_inp = input()
        if user_inp:
            pool.submit(job)
except KeyboardInterrupt:
    pool.shutdown()
