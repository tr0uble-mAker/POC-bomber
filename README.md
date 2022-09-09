# 🔥 POC-bomber
🦄 **POC bomber 是一款漏洞检测/利用工具，旨在利用大量高危害漏洞的POC/EXP快速获取目标服务器权限**
                                  
本项目收集互联网各种危害性大的 RCE · 任意文件上传 · 反序列化 · sql注入 等高危害且能够获取到服务器核心权限的漏洞POC/EXP，并集成在 POC bomber 武器库中，利用大量高危害POC对单个或多个目标进行模糊测试，以此在大量资产中快速获取发现脆弱性目标，获取目标服务器权限。适用场景包括但不仅限于以下:
1. 红蓝对抗或hvv中帮助红队在大量资产中快速找到突破口进入内网
2. 内网安全测试，横向移动
3. 利用新型0day对企业资产进行批量评估

## 📝 简介
POC bomber 的poc支持weblogic，tomcat，apache，jboss，nginx，struct2，thinkphp2x3x5x，spring，redis，jenkins，php语言漏洞，shiro，泛微OA，致远OA，通达OA等易受攻击组件的漏洞检测，支持调用dnslog平台检测无回显的rce(包括log4j2的检测)，支持单个目标检测和批量检测，程序采用高并发线程池，支持自定义导入poc/exp，并能够生成漏洞报告  
POC bomber默认使用验证模式进行poc的验证，如返回结果中attack的值为True时，可以加参数(--attack)进入攻击模式直接调用exp进行攻击(需要指定poc文件名)，达到一键getshell

## 😄 红队专版-RedTeam 3.0
追求更快的速度？更稳定的框架？更低的资源占用？更高的检测效率？更多的poc/exp集成利用？  
尽请期待 POC-bomber RedTeam 3.0，目前仅限内部测试中，请持续关注项目更新。



## 💻 Screenshots    
#### 🏆 验证模式
        python3 pocbomber.py -u http://xxx.xxx
![image](https://user-images.githubusercontent.com/71172892/168099161-f46a54f7-562b-4ba5-a751-1d65492b17d9.png)
![image](https://user-images.githubusercontent.com/71172892/147481630-f8b94566-572f-4d89-a874-dc01f5041377.png)
![verify模试演示](https://user-images.githubusercontent.com/71172892/148684886-98b0f1ff-76f5-48d3-8d2d-932635392a33.gif)


#### ⚡️ 攻击模式
        python3 pocbomber.py -u http://xxx.xxx --poc="thinkphp2_rce.py" --attack
![image](https://user-images.githubusercontent.com/71172892/147629887-def9d18e-f6aa-466a-ab2c-2538752b82aa.png)
![image](https://user-images.githubusercontent.com/71172892/148206720-86f77246-301c-481f-a16c-b36047f72d7c.png)
![attack模式演示](https://user-images.githubusercontent.com/71172892/148684097-67b59320-6758-458d-ac6b-ae219c327924.gif)



## 🔧 安装
      git clone https://github.com/tr0uble-mAker/POC-bomber.git            
      cd POC-bomber
      pip install -r requirements.txt
## 🚀 用法      
        查看用法:     python3 pocbomber.py
        
        模式:
                获取poc/exp信息:   python3 pocbomber.py --show
                单目标检测:        python3 pocbomber.py -u http://xxx.xxx.xx
                批量检测:          python3 pocbomber.py -f url.txt -o report.txt 
                指定poc检测:       python3 pocbomber.py -f url.txt --poc="thinkphp2_rce.py"
                exp攻击模式:       python3 pocbomber.py -u 目标url --poc="指定poc文件" --attack
        参数:
                -u  --url      目标url
                -f  --file     指定目标url文件   
                -o  --output   指定生成报告的文件(默认不生成报告)
                -p  --poc      指定单个或多个poc进行检测, 直接传入poc文件名, 多个poc用(,)分开
                -t  --thread   指定线程池最大并发数量(默认30)
                --show         展示poc/exp详细信息
                --attack       使用poc文件中的exp进行攻击
                --dnslog       使用dnslog平台检测无回显漏洞(默认不启用dnslog,可在配置文件中启用)
                
## 🔆 配置文件    
      /inc/config.py   
      
          


## ⚠️ 常见问题
1. 程序不安装requirements.txt就可以直接运行，只依赖requests第三方库，其他库安装不上不影响程序运行，但有些poc会不能检测
2. log4j2命令执行漏洞的检测：需要添加 --dnslog  参数 
3. 无回显漏洞检测默认使用 dnslog.cn 平台且默认关闭, 要开启需前往配置文件将 dnslog_flag 开关置为True  
4. 需要指定一个poc才能调用--attack攻击模式


## 📁 目录结构:
       
      +--------- poc_bomber.py (启动 POC-bomber)
      | 
      +--------- inc(存放支撑 POC-bomber 框架运行的核心文件)
      |
      \--------- pocs(POC存放列表)----------- framework(存放框架漏洞POC)
                                      |
                                      |------ middleware(存放中间件漏洞POC)
                                      |
                                      |------ ports(存放常见端口漏洞,主机服务漏洞POC)
                                      |
                                       \----- webs(存放常见web页面漏洞POC)
      
      


## 📖 POC编写规则     
POC bomber支持自定义编写poc          
poc统一要求python3编写，具有verify和attack(非必须)两个函数分别进行验证和攻击,                     
#### 👻 漏洞验证函数(verify)编写应该满足以下条件:                   
1. 函数名为 verify ， 参数接收目标url的参数           
2. 函数的返回结果以字典的形式返回并且具有name和vulnerable两个键值，name说明漏洞名称，vulnerable通过True和False的状态表明漏洞是否存在
3. 如果存在漏洞要将返回字典中vulnerable的值置为True, 并添加目标url, 漏洞利用相关网页等信息
4. 用try方法尝试验证，使用request等发送数据包时要设置超时时间, 避免poc会卡死                              
  
        def verify(url):                        
            relsult = {                                            
                'name': 'Thinkphp5 5.0.22/5.1.29 Remote Code Execution Vulnerability',                          
                'vulnerable': False，
                'attack'： False，        # 如果有exp支持attack模式将attack的值置为True
            }              
            try:                    
                ......        
                (用任意方法检测漏洞)             
                ......
                if 存在漏洞:
                    relsult['vulnerable'] = True     # 将relsult的vulnerable的值置为True
                    relsult['url'] = url             # 返回验证的url
                    relust['xxxxx'] = 'xxxxx'        # 可以添加该漏洞相关来源等信息   
                    ......           
                    return relsult     # 将vulnerable值为True的relsult返回                   
                else:  # 不存在漏洞           
                    return relsult    # 若不存在漏洞将vulnerable值为False的relsult返回

            execpt:
                return relsult

如果有exp可以编写 attack 函数作为exp攻击函数，
#### 🎃 漏洞攻击函数(attack)编写应该满足以下条件：
1. 函数名为 attack ， 参数接收目标url的参数  
2. 并在try中编写exp代码进行攻击, 可以与用户交互输入       
3. 编写完成后将该漏洞的verify函数返回字典中attack值置为True 
4. 攻击成功后返回True，其他原因失败的话返回False即可        
      
        def attack(url):    
          try:            
              ........................................            
                攻击代码(执行命令或反弹shell上传木马等)             
              ........................................
              return True
          except:               
              return False    
                      
                      
编写完成后的poc直接放入 /pocs 目录下任意位置即可被递归调用!    


项目持续更新中，欢迎各位师傅贡献poc共筑网络安全！  
有问题欢迎issues留言: https://github.com/tr0uble-mAker/POC-bomber/issues    
联系: 929305053@qq.com    
## 免责声明
本工具仅面向合法授权的企业安全建设行为，如您需要测试本工具的可用性，请自行搭建靶机环境。
在使用本工具进行检测时，您应确保该行为符合当地的法律法规，并且已经取得了足够的授权。请勿对非授权目标进行扫描。
如您在使用本工具的过程中存在任何非法行为，您需自行承担相应后果，我们将不承担任何法律及连带责任。
