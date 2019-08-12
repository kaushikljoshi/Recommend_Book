# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 22:34:57 2019

@author: kaushik Joshi
"""

import statistics

def get_modified_standard_score(data_list):
    npoints = len(data_list)
    median = get_median(data_list)
    asd    = get_asd(npoints,data_list)
    
    for i1 in range(0,npoints):
        data_list[i1] = (data_list[i1]-median)/asd
    

def get_median(data_list):
    return statistics.median(data_list)

def get_asd(npoints, data_list):
    median = get_median(data_list)
    temp_sum = 0.0
    for i1 in range(0,npoints):
        temp_sum = temp_sum + abs(data_list[i1]-median)
    
    return temp_sum/npoints
    
    