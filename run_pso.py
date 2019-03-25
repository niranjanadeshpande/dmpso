#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:43:19 2019

@author: niranjana
"""

import os

path_length = [5, 10, 20]#, [5, 10,20, 30, 40, 50]#, 100, 200, 300, 400, 500]
cand_serv = [5, 10, 20, 30, 40]#[5, 10, 15, 20, 25, 30, 35, 40, 50]

for i in path_length:
    for j in cand_serv:
            string_cmd = "python dmpso.py " + str(i) +" "+ str(j)+"  >> PSO_output_timings.txt 2>&1"
            print(string_cmd)
            temp_var = os.system(string_cmd)
            print(temp_var)