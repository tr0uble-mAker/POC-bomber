import threading
import requests
import time
from queue import Queue
from inc.init import *

# 线程模块
class MyThread(threading.Thread):       # 重写Thread，加入返回值
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)  # 在执行函数的同时，把结果赋值给result,
        # 然后通过get_result函数获取返回的结果

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            return None


class Threads():            # 本项目引用到的线程模块
    def __init__(self, max_threads, thread_timeout):
        self.queue = Queue()
        self.max_threads = max_threads  # 最大线程
        self.current_threads = []
        self.report = []                # 报告
        self.timeout = thread_timeout   # 线程超时时间
        self.cheak_thread = []          # 用于检查超时线程

    def add_task(self, target):
        t = re.findall(r'[^(]*', target)[0]
        p = re.findall(r'\("(.*)"\)', target)[0]
        task = MyThread(eval(t), args=(p, ))
        self.queue.put(task)

    def start_thread(self):
        output = threading.Thread(target=self.output)
        timeout = threading.Thread(target=self.thread_timeout)
        timeout.start()
        output.start()
        while not self.queue.empty():
            while threading.activeCount() <= self.max_threads + 1:
                if self.queue.empty():
                    break
                thread = self.queue.get()
                self.queue.task_done()
                thread.setDaemon(True)
                thread.start()
                self.current_threads.append(thread)
        output.join()


    def output(self):
        while (len(self.current_threads) != 0) or (self.queue.empty() is not True):
            for current_thread in self.current_threads:
                relsult = current_thread.get_result()
                if relsult is not None:
                    print('\n[+] 正在检测: ' + str(relsult['name']))
                    self.current_threads.remove(current_thread)
                    if relsult['vulnerable']:
                        self.report.append(relsult)
                        print('\n[@] 检测到漏洞:', relsult['name'])


    def thread_timeout(self):       # 检查线程超时
        while (len(self.current_threads) != 0) or (self.queue.empty() is not True):
            time.sleep(self.timeout)
            for t in self.current_threads:
                if t in self.cheak_thread:
                    self.current_threads.remove(t)
                    print('\n[-] 线程超时,已放弃该线程', t.getName())
            self.cheak_thread = self.current_threads

    def get_report(self):       # 获取存在漏洞的结果报告
        return self.report

