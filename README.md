# POC-bomber
POC bomber 是一款漏洞检测工具，旨在利用大量高危害漏洞的POC快速获取目标服务器权限 
                                  
本项目收集互联网各种危害性大的 RCE · 任意文件上传 · sql注入 等高危害且能够获取到服务器核心权限的漏洞POC，并集成在 POC bomber 武器库中，利用大量高危害POC对单个或多个目标进行模糊测试，以此快速获取目标服务器权限，适合在红蓝对抗或hvv中帮助红队快速找到突破口进入内网

支持weblogic，jboss，struct2，tp5，redis未授权访问，各大常见OA等易受攻击组件的漏洞检测，支持调用dnslog或ceye平台检测无回显的rce，支持单个目标检测和批量检测，支持多线程和自定义poc，并能够在当前目录生成漏洞报告
## 安装
      git clone https://github.com/tr0uble-mAker/POC-bomber.git            
      cd POC-bomber
## 用法      
      python3 poc_bomber.py 

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
![image](https://user-images.githubusercontent.com/71172892/143585798-9d7e505d-42f0-4b8f-ae0c-fd400466f2b5.png)
![image](https://user-images.githubusercontent.com/71172892/143586027-5e54e484-edc7-4551-a536-4f005efa5048.png)      


## POC编写规则     
POC bomber支持自定义编写poc          
POC bomber的poc编写简便灵活，没有严格的格式要求只要用python3以任意方法编写出可以验证漏洞的函数即可                        
漏洞验证函数应该满足以下条件:                   
1. 函数的返回结果以字典的形式返回并且具有name和vulnerable两个键值，name说明漏洞名称，vulnerable通过True和False的状态表明漏洞是否存在           
2. 示例函数如下(以 thinkphp5.0.22/5.1.29 的命令执行漏洞为例)                                  
  
        def  thinkphp5022_5129_rce(url):          
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
                  relust['xxxxx'] = 'xxxxx'     # 可以添加该漏洞相关来源等信息            
                  ......           
                  return relsult     # 将vulnerable值为True的relsult返回                   
              else:  # 不存在漏洞           
                  return relsult    # 若不存在漏洞将vulnerable值为False的relsult返回

            execpt:
              return relsult

编写完成后的poc可以直接放在在相关漏洞检测模块的目录下，并在当前目录下的main函数中导入           
例如将编写好的文件CVE_2021_22205.py("CVE-2021-22205 GitLab 未授权RCE" 的POC)应该放在目录/pocs下的web漏洞检测模块(/pocs/web)中即 /pocs/web/CVE_2021_22205.py ，并在 /pocs/web/main.py 的文件中导入CVE_2021_22205.py的漏洞验证函数      


项目持续更新中，欢迎各位师傅贡献poc共筑网络安全！  
有问题欢迎issues留言: https://github.com/tr0uble-mAker/POC-bomber/issues    
联系: 929305053@qq.com    
