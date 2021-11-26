# POC-bomber
POC bomber 是一款漏洞检测工具，旨在利用大量POC快速发现目标脆弱性，节省人工检测漏洞的时间   
                                  
本项目收集互联网已知危害性大且影响广泛漏洞的POC并集成在 POC bomber 武器库中，并利用大量POC对单个或多个目标进行模糊测试，以此快速获取目标服务器权限，适合红蓝对抗或hvv中红队快速找到突破口进入内网       
支持weblogic，struct2，tp5，redis未授权等漏洞的检测，支持多线程在检测结束生成报告

用法:

      python3 poc_bomber.py 

配置文件: /inc/config.py

目录结构:
       
      +--------- poc_bomber.py (启动 POC-bomber)
      | 
      +--------- inc(存放支撑 POC-bomber 框架运行的核心文件)
      |
      \--------- pocs(POC存放列表)----------- framework(存放框架漏洞POC)
                                      |
                                      |------ middleware(中间件漏洞POC)
                                      |
                                      |------ ports(常见端口漏洞,主机服务漏洞POC)
                                      |
                                       \----- webs(常见web页面漏洞POC)
      
      
      
     
项目持续更新中，欢迎各位师傅贡献POC共筑网络安全！  
有问题欢迎issues留言  
联系: 929305053@qq.com    
