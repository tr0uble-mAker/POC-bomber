#!/usr/bin/env python
# coding=utf-8
import random, time, os

def output(futures, ouput_path=''):
    succeed_report = []
    for future in futures:
        relsult = future.result()
        if relsult['vulnerable']:
            print('[SUCCESS] 检测到: {0}  目标: {1} !'.format(relsult['name'], relsult['url']))
            succeed_report.append(relsult)
        else:
            print('[INFO] 正在检测: {0}'.format(relsult['name']))
    print('[INFO] 所有检测任务完成, 即将生成报告......')
    if len(succeed_report) != 0:
        print('----')
        for relsult in succeed_report:
            first = True
            for r in relsult:
                if first:
                    value = '[!]{0}: {1}'.format(str(r.capitalize()), str(relsult[r]))
                    print(str(value))
                    first = False
                    if ouput_path != '':
                        data_save(ouput_path, value)
                else:
                    value = '     {0}: {1}'.format(str(r.capitalize()), str(relsult[r]))
                    print(value)
                    if ouput_path != '':
                        data_save(ouput_path, value)
        print('----')
        if ouput_path != '':
            print('[INFO] 已将报告写入至 {0} !'.format(os.path.join(os.path.abspath('.'), ouput_path)))
        else:
            print('[WARNING] 程序没有生成任何报告类文件以记录此次任务的数据')
    else:
        print('[CRITICAL] 所有测试已结束但是程序未生成任何报告')




def data_save(output_path, value):
    report_file = open(output_path, 'a+')
    report_file.write(value)
    report_file.write('\n')
    report_file.close()



def logo():
    logo0 = r'''
    
    
 ____   ___   ____   ____                  _               
|  _ \ / _ \ / ___| | __ )  ___  _ __ ___ | |__   ___ _ __ 
| |_) | | | | |     |  _ \ / _ \| '_ ` _ \| '_ \ / _ \ '__|
|  __/| |_| | |___  | |_) | (_) | | | | | | |_) |  __/ |   
|_|    \___/ \____| |____/ \___/|_| |_| |_|_.__/ \___|_|   

    
    
                                                Version 1.00
                                                            Author  tr0uble_mAker
                                                            Whoami  https://github.com/tr0uble-mAker
    '''
    logo1 = r'''

    
        

        
         ##    ping @@@@    ##   
           ##@@@@@@ @@@@@@##
            @@@@@@@ @@@@@@@          
           @@@@@@@@ @@@@@@@@   
    ## ## #@@@@@@@@ @@@@@@@@## ## ##You have an error in your SQL syntax.......   
           @eval($_ POST);@@
           @@@@@@@@ @@@@@@@@             
         ##@@@@@@@@ @@@@@@@@##
        ##                   ##    
                @root@@        
                 @@@@@ 
                 
                                                                                        
                                        POC bomber                          Version 1.00
                                                                            Author tr0uble_mAker
                                                                            Whoami https://github.com/tr0uble-mAker
                                                               
                                                               
                        /*!   你的系统似乎出了些问题, leT%27s ChEcK iT !!!  */                                                                                    
            '''
    logo2 = r'''





                                             ##    @@@@  @@@@    ##   
                                               ##@@@@@@  @@@@@@##
                                                @@@@@@@  @@@@@@@          
                                               @@@@@@@@  @@@@@@@@   
                                          ### #@@@@@@@@  @@@@@@@@# ###   
                                               @@@@@@@@  @@@@@@@@
                                               @@@@@@@@  @@@@@@@@             
                                             ##@@@@@@@@  @@@@@@@@##
                                            ##                    ##    
                                                     @@@@@@@        
                                                      @@@@@ 
                                                      
                                                      
                                                    POC bomber
                                               Author tr0uble_mAker
                                        Whoami https://github.com/tr0uble-mAker
                                                                                                       
                '''

    print(random.choice([logo0, logo1, logo2]))


def usage():
    print('''
        用法:
                单目标检测: python3 pocbomber.py -u http://xxx.xxx.xx -o report.txt
                批量检测:   python3 pocbomber.py -f url.txt 
        参数:
                -u  --url      目标url
                -f  --file     指定目标url文件   
                -o  --output   指定生成报告的文件
    
    ''')
if __name__ == '__main__':
    logo()