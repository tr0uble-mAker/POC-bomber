from inc import init
from inc import common
from inc import output, dnslog
import queue, time, threading
import concurrent.futures
from func_timeout import func_set_timeout

class ThreadPool():
    '''线城池模块'''
    def __init__(self):
        self.max_thread = common.get_value('max_threads')
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_thread)
        self.task_queue = queue.Queue()
        self.futures = {}

    def add_task(self, func, target):
        new_task = (func, target)
        self.task_queue.put(new_task)

    def start_threadpool(self):
        while self.task_queue.qsize() != 0:
            current_target, current_script = self.task_queue.get()
            future = self.thread_pool.submit(self.run_signel_poc, current_target, current_script)
            self.futures[future] = (current_target, current_script)
            if common.get_value("delay"):
                self.do_result(future.result())
                time.sleep(common.get_value("delay"))
        if not common.get_value("delay"):
            for future in concurrent.futures.as_completed(self.futures):
                self.do_result(future.result())
        self.thread_pool.shutdown()

    @func_set_timeout(common.get_value('timeout'))
    def set_fuc_timeout(self, func, arg):
        '''设置函数超时'''
        result = func(arg)
        return result

    def run_signel_poc(self, current_target, current_script):
        try:
            result = self.set_fuc_timeout(common.get_value("pocinfo_dict")[current_script].verify, current_target)
            result["url"] = current_target
            result["script"] = current_script
            return result
        except:
            # 超时
            result = {
                "url": current_target,
                "script": current_script,
                "timeout": True,
            }
            return result

    def do_result(self, result):
        if result.get("dnslog_domain"):
            dnslog.dnslog_add_scan(result)
        else:
            output.put_output_queue(result)



