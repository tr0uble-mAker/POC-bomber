import socket
import re
from threading import Thread
from queue import Queue
from time import sleep, time
from urllib.parse import urlparse

def is_ip(url):
    if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", url):
        return True
    else:
        return False

def is_open(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(1)
        s.connect((host, int(port)))
        s.shutdown(2)
        return True
    except:
        return False

def redis_6379(url, port=6379):
    relsult = {
        'name': 'Redis 4.x/5.x 未授权访问漏洞',
        'vulnerable': False
    }
    oH = urlparse(url)
    a = oH.netloc.split(':')
    # port = 6379        # redis默认端口是6379
    host = a[0]
    if is_open(host, port) is False:  # 端口未开放直接退出
        return relsult
    if url:
        payload = b'*1\r\n$4\r\ninfo\r\n'  # 发送的数据
        s = socket.socket()
        socket.setdefaulttimeout(3)  # 设置超时时间
        try:
            s.connect((host, int(port)))
            s.send(payload)  # 发送info命令
            response = s.recv(1024).decode()
            s.close()

            if response and 'redis_version' in response:
                relsult['vulnerable'] = True
                relsult['url'] = url
                relsult['port'] = port
                relsult['about'] = 'https://github.com/vulhub/redis-rogue-getshell'
                return relsult
        except (socket.error, socket.timeout):
            return relsult

    return relsult



def create_queue(file_name):
    """
    创建数据队列
    argument: file_name -> 输入文件名
    return: data,total 数据队列,数据总数
    """
    total = 0
    data = Queue()
    for line in open(file_name):
        url = line.strip()
        if url:
            # 跳过空白的行
            data.put(url)
            total += 1

    data.put(None)  # 结束标记
    return data, total


def start_jobs(data, num):
    """
    启动所有工作线程
    argument: data -> 数据队列 num -> 线程数
    """
    is_alive = [True]

    def job():
        """工作线程"""
        while is_alive[0]:
            try:
                url = data.get()
                if url == None:
                    # 遇到结束标记
                    break
                code, result = redis_6379(url)  # 验证漏洞
                if code:
                    print(result)  # 存在漏洞
            except:
                is_alive[0] = False
        data.put(None)  # 结束标记

    jobs = [Thread(target=job) for i in range(num)]  # 创建多个线程
    for j in jobs:
        j.setDaemon(True)
        j.start()  # 启动线程

    for j in jobs:
        j.join()  # 等待线程退出


def main():
    file_name = input('输入文件路径:')  # 输入文件
    num = int(input('输入执行的线程:'))  # 线程数
    data, total = create_queue(file_name)  # 创建数据队列
    print('total: %s' % total)
    begin = time()
    start_jobs(data, num)  # 启动工作线程
    end = time()
    print('spent %ss' % str(end - begin))


if __name__ == '__main__':
    host = input('host:')
    port = input('port:')
    print(redis_6379(host, int(port)))
