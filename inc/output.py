#!/usr/bin/env python
# coding=utf-8
import random

# 输出模块
def output(report, output_path=''):
    print('\n[+] 所有检测完毕即将生成报告......')
    print('----\n')
    if len(report) == 0:
        print('\n[-] 未检测出漏洞所以程序未生成任何报告')
        print('\n----')
        return
    for relsult in report:
        first = True
        for r in relsult:
            if first:
                #print('[!]', r.capitalize(), ':', relsult[r])
                value = '[!]{0}: {1}'.format(str(r.capitalize()), str(relsult[r]))
                print(str(value))
                if output_path != '':
                    write_report(output_path, value)
                first = False
            else:
                #print('     ', r.capitalize(), ':', relsult[r])
                value = '     {0}: {1}'.format(str(r.capitalize()), str(relsult[r]))
                print(value)
                if output_path != '':
                    write_report(output_path, value)
        print('\n', end='')
    print('\n----')
    print('\n[+] 报告已生成至\'{0}\''.format(output_path))

def write_report(output_path, value):
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
if __name__ == '__main__':
    logo()