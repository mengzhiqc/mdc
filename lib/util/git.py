#encoding=utf-8
'''
处理dev环境各种git操作
可以考虑替换为一个现成的更成熟的实现
@author: lenye01
'''

import os
import md5




def execute(command):
    '''
    shell命令执行 调用popen命令
    '''
    if str(command) != '':
        handle = os.popen(command)
        return handle.readlines()
    



