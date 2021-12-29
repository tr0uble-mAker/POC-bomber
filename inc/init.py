#!/usr/bin/env python
# coding=utf-8
import os, sys, importlib
import platform
from inc import output
# 调用此模块用来加载全部poc

def get_dir_files(base_path):           # 递归调用pocs目录下文件返回每条poc的绝对路径
    file_list = []
    if os.path.isdir(base_path):
        for each_file_or_dir in os.listdir(base_path):
            current_path = os.path.join(base_path, each_file_or_dir)
            if os.path.isfile(current_path) and each_file_or_dir.split('.')[-1] != 'py':        # 只加载py形式的poc文件
                continue
            each_path = get_dir_files(current_path)
            for file in each_path:
                file_list.append(file)

    else:
        file_list.append(base_path)
    return file_list


def path_to_modolepath(path):                   # 传入相对路径返回模块导入路径
    if 'Windows' in platform.system():
        path = path.lstrip('\\')
        modole_path = path.replace('\\', '.')
    else:
        path = path.lstrip('/')
        modole_path = path.replace('/', '.')
    modole_path = modole_path.replace('.py', '')
    return modole_path


def get_filename_by_path(path):         # 根据路径获取文件名
    if 'Windows' in platform.system():
        filename = path.split('\\')[-1]
    else:
        filename = path.split('/')[-1]
    return filename


def get_poc_modole_list():              # 调用此函数获取 /pocs 下的全部 poc
    poc_module_list = []
    current_path = os.path.abspath('.')
    pocs_base_path = os.path.join(current_path, 'pocs')
    poc_path_list = get_dir_files(pocs_base_path)
    for poc_path in poc_path_list:
        poc_path = poc_path.replace(current_path, '')
        poc_modole_path = path_to_modolepath(poc_path)
        try:
            poc_module_list.append(importlib.import_module(poc_modole_path))
        except:
            pass
    return poc_module_list


def get_poc_modole_list_by_search(search_keys_list):     # 此函数通过搜索poc文件名调用相应的poc, 传入poc文件名列表, 返回由poc对象的列表
    search_flag = True
    poc_modole_list = []
    current_path = os.path.abspath('.')
    pocs_base_path = os.path.join(current_path, 'pocs')
    poc_path_list = get_dir_files(pocs_base_path)
    for search_key in search_keys_list:
        for poc_path in poc_path_list:
            poc_rppath = poc_path.replace(current_path, '')
            poc_filename = get_filename_by_path(poc_rppath)
            if search_key == poc_filename and search_flag:
                try:
                    output.status_print('成功检测到poc文件: {0}'.format(poc_filename), 0)
                    poc_modole_path = path_to_modolepath(poc_rppath)
                    poc_modole_list.append(importlib.import_module(poc_modole_path))
                    search_flag = False
                    break
                except:
                    search_flag = True
                    break
        if search_flag:
            output.status_print('未检测到poc文件: {0}'.format(search_key), 2)
        search_flag = True
    return poc_modole_list






