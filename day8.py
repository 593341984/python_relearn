# -*- coding:utf-8 -*-
__author__ = "ljh"
__date__ = "2019-07-24"


import sys, os, zipfile
import time
import re

def unzip_single(src_file, dest_dir, password):
    if password:
        password = password.encode()

    zf = zipfile.ZipFile(src_file)


    try:
        zf.extractall(path=dest_dir, pwd=password)
    except RuntimeError as e:
        print(e)

    zf.close()


def channel():

    zf = zipfile.ZipFile('channel.zip')
    files = zf.namelist()

    def item(start, ret_l=[]):
        if start in files:
            with zf.open(start) as f:
                content = f.read().decode('utf8')
                comment = zf.getinfo(start).comment.decode('utf8')
                ret_l.append(comment)
                print(content.split(' ')[-1])
            return item('{}.txt'.format(content.split(' ')[-1]))
        else:
            return ret_l
    return item('90052.txt')


def f(n, m):
    return n if n == 1 else (f(n-1, m) + m -1) % n + 1


if __name__ == '__main__':
    # unzip_single('channel.zip', 'channel/', '')
    print(f(6,3))