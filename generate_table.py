#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 18:03:52 2019

@author: niranjana
"""

import os

path_length = [5,10,20, 30, 40, 50, 100] #, 200, 300, 400, 500
cand_serv = [5, 10, 15, 20, 25, 30, 35, 40]#, 50

for i in path_length:
    for j in cand_serv:
        string_cmd = "python autograph_gen_new.py " + str(i) +" "+ str(j)
        print(string_cmd)
        out = os.system(string_cmd)
        print(out)
