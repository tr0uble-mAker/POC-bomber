# POC-bomber
本项目收集互联网已知危害性大且影响广泛漏洞的POC并集成在武器库中，对单个或大量目标进行模糊测试，适合红蓝对抗或hvv中红队快速找到突破口进入内网

用法:

      python3 poc_bomber.py 

配置文件:
      /inc/config.py

目录结构:
       
      +--------- poc_bomber.py (启动POC-bomber)
      | 
      +--------- inc(存放POC-bomber框架的配置文件)
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
