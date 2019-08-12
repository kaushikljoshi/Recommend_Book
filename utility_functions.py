# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 20:46:42 2019

@author: kaushik Joshi
"""

from os import path
import math


def check_file(filename):
    if (path.isfile(filename)):
        return True
    else:
        return False
    
def get_distance(vec1,vec2,n):
    #Miknowski formula, n=1 is Manahattan distance, n=2 is Euclidean distance
    distance = 0.0
    for i1 in range(0,len(vec1)):
        distance = distance + pow(abs(vec1[i1]-vec2[i1]),n)
    return pow(distance,1.0/n)            

def get_cosine_similarity(dict1,dict2):
    sum1 = 0.0
    sum2 = 0.0
    sum3 = 0.0
    for key in dict1:
        if key in dict2:
            sum1 = sum1 + dict1[key]*dict1[key]
            sum2 = sum2 + dict2[key]*dict2[key]
            sum3 = sum3 + dict1[key]*dict2[key]
  
    if (sum1 == 0.0 or sum2 == 0.0):
        result = 0.0
    else:
        result = sum3 /(math.sqrt(sum1)*math.sqrt(sum2))
    
    return result

def get_Pearson(dict1,dict2):
    vec1 = []
    vec2 = []
    for key in dict1:
        if key in dict2:
            vec1.append(dict1[key])
            vec2.append(dict2[key])
    
    if (len(vec1) == 0):
        return 0.0
    
    avg1 = sum(vec1)/len(vec1)
    avg2 = sum(vec2)/len(vec2)
    
    sum1 = 0.0
    sum2 = 0.0
    sum3 = 0.0
    
    for i1 in range(0,len(vec1)):
        sum1 = sum1 + (vec1[i1] - avg1)*(vec2[i1] - avg2)
        sum2 = sum2 + pow((vec1[i1]-avg1),2)
        sum3 = sum3 + pow((vec2[i1]-avg2),2)
    
    if (sum3 == 0 or sum2 == 0):
        return 0.0
    else:
        return sum1/(math.sqrt(sum2)*math.sqrt(sum3))
    

#def get_nearest_neighbor(name,data_list):
    
def parse_string(i_line,o_list):
    data = i_line.split(';')                
    size = len(data)
            
    if (size == 3 and data[0].strip('"').isnumeric() ):
        o_list.append(data[0].strip('"'))    
        temp_s = data[size-1].strip().strip('"')
        if (temp_s == 'NULL'):
            o_list.append(data[1].strip('"'))
            for i2 in range(2,size-1):
                o_list[1] = o_list[1]+data[i2]
        elif (temp_s.isnumeric()):
            o_list.append(data[1].strip('"'))
            for i2 in range(2,size-1):
                o_list[1] = o_list[1]+data[i2]
            o_list.append(temp_s)
        else:
            o_list.append(data[1].strip('"'))
            for i2 in range(2,size+1):
                o_list[1] = o_list[1]+data[i2]
    