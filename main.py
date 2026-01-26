import threading
import time
import random


class MinHeap:
    def __init__(self):
        self.heap = []
        self.lock = threading.RLock()
        self.condition = threading.Condition(self.lock)

    def insert(self, job, schedule_time=0):
        job_obj = (job, time.time() + schedule_time)
        with self.condition:
            if not self.heap:
                self.heap.append(job_obj)
                self.condition.notify()
                return
            self.heap.append(job_obj)
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
            self.condition.notify()

    def extract(self):
        with self.condition:
            if len(self.heap) == 1:
                job_obj = self.heap.pop()
                return job_obj
            self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
            job_obj = self.heap.pop()
            index = 0
            while index < len(self.heap):
                left = 2 * index + 1
                right = 2 * index + 2
                smallest_index = index

                if (
                    left < len(self.heap)
                    and self.heap[left][1] < self.heap[smallest_index][1]
                ):
                    smallest_index = left
                if (
                    right < len(self.heap)
                    and self.heap[right][1] < self.heap[smallest_index][1]
                ):
                    smallest_index = right
                if smallest_index == index:
                    break
                else:
                    self.heap[index], self.heap[smallest_index] = (
                        self.heap[smallest_index],
                        self.heap[index],
                    )
                    index = smallest_index
        return job_obj

    def peek(self):
        with self.condition:
            if not self.heap:
                return None
            return self.heap[0]


h = MinHeap()


def job():
    print("\nRunning job...")
    sleep_time = random.randint(4, 10)
    print(f"Thinking of a number for {sleep_time} seconds.")
    time.sleep(sleep_time)
    print(f"The number is {random.randint(0, 9)}")


def producers(h):
    while not shutdown_event.is_set():
        user_inp = input()
        if shutdown_event.is_set():
            break
        if user_inp.isdigit():
            h.insert(job, float(user_inp))
        elif user_inp.isalpha():
            h.insert(job)


def consumers(h):
    while not shutdown_event.is_set():
        with h.condition:
            while not h.heap and not shutdown_event.is_set():
                h.condition.wait()
            if shutdown_event.is_set():
                break
            job_obj = h.peek()
            time_now = time.time()
            if job_obj[1] > time_now:
                h.condition.wait(timeout=job_obj[1] - time_now)
                continue
            do_job = h.extract()
            if callable(do_job[0]):
                do_job[0]()


shutdown_event = threading.Event()

t1 = threading.Thread(target=producers, args=(h,), daemon=True)
t2 = threading.Thread(target=consumers, args=(h,), daemon=True)
t1.start()
t2.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    shutdown_event.set()
    with h.condition:
        h.condition.notify_all()
    t2.join()
    print("\nShutting down. If blocked, press Enter to exit.")
