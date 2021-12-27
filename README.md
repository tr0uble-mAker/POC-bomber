# POC-bomber
POC bomber 是一款漏洞检测工具，旨在利用大量高危害漏洞的POC快速获取目标服务器权限 
                                  
本项目收集互联网各种危害性大的 RCE · 任意文件上传 · sql注入 等高危害且能够获取到服务器核心权限的漏洞POC，并集成在 POC bomber 武器库中，利用大量高危害POC对单个或多个目标进行模糊测试，以此快速获取目标服务器权限，适合在红蓝对抗或hvv中帮助红队快速找到突破口进入内网

支持weblogic，jboss，struct2，tp5，redis未授权访问，各大常见OA等易受攻击组件的漏洞检测，支持调用dnslog平台检测无回显的rce，支持单个目标检测和批量检测，POC bomber支持高并发线程池和自定义poc，并能够在当前目录生成漏洞报告，后续会增加exp攻击的功能
## 安装
      git clone https://github.com/tr0uble-mAker/POC-bomber.git            
      cd POC-bomber
## 用法      
        模式:
                单目标检测: python3 pocbomber.py -u http://xxx.xxx.xx
                批量检测:   python3 pocbomber.py -f url.txt -o report.txt 
        参数:
                -u  --url      目标url
                -f  --file     指定目标url文件   
                -o  --output   指定生成报告的文件(默认不生成报告)
                --dnslog       使用dnslog平台检测无回显漏洞(默认不启用dnslog,可在配置文件中启用)

## 配置文件    
      /inc/config.py         
无回显漏洞检测默认使用 dnslog.cn 平台且默认关闭, 要开启需前往配置文件将 dnslog_flag 开关置为True

## 目录结构:
       
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
      
      
## Screenshots    
![image](https://user-images.githubusercontent.com/71172892/147401553-420a9b43-c6ef-40ce-aa88-de47243a9996.png)
![image](https://user-images.githubusercontent.com/71172892/147481683-ff5c4fbf-efd6-4232-a30d-32bc6c30bc14.png)
![image](https://user-images.githubusercontent.com/71172892/147481630-f8b94566-572f-4d89-a874-dc01f5041377.png)   


## POC编写规则     
POC bomber支持自定义编写poc          
POC bomber的poc编写简便灵活，没有严格的格式要求只要用python3以任意方法编写出可以验证漏洞的函数即可                        
漏洞验证函数应该满足以下条件:                   
1. 函数的返回结果以字典的形式返回并且具有name和vulnerable两个键值，name说明漏洞名称，vulnerable通过True和False的状态表明漏洞是否存在           
2. 函数名为 verify                                 
  
        def verify(url):                        
            relsult = {                                            
                'name': 'Thinkphp5 5.0.22/5.1.29 Remote Code Execution Vulnerability',                          
                'vulnerable': False                          
            }              
            try:                    
                ......        
                (用任意方法检测漏洞)             
                ......
                if 存在漏洞:
                    relsult['vulnerable'] = True     # 将relsult的vulnerable的值置为True
                    relsult['url'] = url             # 返回验证的url
                    relust['xxxxx'] = 'xxxxx'        # 可以添加该漏洞相关来源等信息   
                    relsult['attack'] = True         # 如果有exp返回attack的值为True
                    ......           
                    return relsult     # 将vulnerable值为True的relsult返回                   
                else:  # 不存在漏洞           
                    return relsult    # 若不存在漏洞将vulnerable值为False的relsult返回

            execpt:
                return relsult

如果有exp可以编写 attack 函数, 该函数没有参数传入, 直接编写exp代码进行攻击, 编写完成后将该漏洞的verify函数返回字典中值attack置为True即可                        
  def attack():    
    try:            
          ......            
          攻击代码             
          ......    
    except:               
          return                    
编写完成后的poc直接放入 /pocs 目录下任意位置即可被递归调用!    


项目持续更新中，欢迎各位师傅贡献poc共筑网络安全！  
有问题欢迎issues留言: https://github.com/tr0uble-mAker/POC-bomber/issues    
联系: 929305053@qq.com    
