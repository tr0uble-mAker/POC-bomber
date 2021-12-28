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


def get_one_poc_modole(poc_filename_search):                   # 此函数调用一条poc文件, 传入poc文件名列表, 返回  (对象,绝对路径)
    current_path = os.path.abspath('.')
    pocs_base_path = os.path.join(current_path, 'pocs')
    poc_path_list = get_dir_files(pocs_base_path)
    for poc_path in poc_path_list:
        poc_rppath = poc_path.replace(current_path, '')
        if 'Windows' in platform.system():
            poc_filename = poc_rppath.split('\\')[-1]
        else:
            poc_filename = poc_rppath.split('/')[-1]
        if poc_filename_search == poc_filename:
            try:
                poc_modole_path = path_to_modolepath(poc_rppath)
                return (importlib.import_module(poc_modole_path), poc_path)
            except:
                return False
    return False






