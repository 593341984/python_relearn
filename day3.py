# -*- coding:utf-8 -*-
__author__ = "ljh"
__date__ = "2019-07-10"


foo = [{"name": "zs", "age": 19}, {"name": "ll", "age": 54},
       {"name": "wa", "age": 17}, {"name": "df", "age": 23}]

print(sorted(foo, key=lambda x: x.get('age')))
