from inc.init import *
import re, time, random, queue, requests
import concurrent.futures

# 线程池模块
class ThreadPool():
    def __init__(self, max_thread):
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_thread)
        self.task_queue = queue.Queue()
        self.futures = {}

    def add_task(self, poc, target):
        new_task = (poc, target)
        self.task_queue.put(new_task)

    def start_threadpool(self):
        while self.task_queue.qsize() != 0:
            current_task = self.task_queue.get()
            current_poc = current_task[0]
            current_target = current_task[1]
            future = self.thread_pool.submit(current_poc, current_target)
            self.futures[future] = current_target
        self.futures = concurrent.futures.as_completed(self.futures)
        return self.futures


