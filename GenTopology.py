# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:40:52 2020

Generate geological profile topology of adjacent boreholes.

This module should be fully compatible with:
    * Python >=v3.7
    * Spyder >=v4.0
    
@author: Da YIN
e-mail: forestrock@163.com
"""


import pandas as pd
import numpy as np
from ConnectedDomain import LCS


# =============================================================================
# 依次两两比较相邻钻孔，由LCS判别土层代号字符串的公共子序列（即连通域）
# =============================================================================
def neighbourhood(nhb,domainID):
    for i in range(len(nbh)):
        tmp = [str(x) for x in domainID.iloc[i]]
        s1 = "["+''.join(tmp)+"]"
        for j in range(len(nbh[i])):
            n = nbh[i][j][0]
            # 单向比较
            if n > i:
                tmp = [str(x) for x in domainID.iloc[n]]
                s2 = "["+''.join(tmp)+"]"             
                (lcs,id1,id2)=LCS(s1, s2)
                 
            
            pass     
        
        pass
        

# =============================================================================
# 对于非连通域生成相应的拓扑控制点，自动生成相应的钻孔地质剖面拓扑
# =============================================================================
def gen_new_topo_node(h1,h2,id1,id2,interfaceID):
    num_node = max(interfaceID.max())
    n = 0
    
    pointer1 = 0
    for i in range(pointer1,len(id1)):
        
        node1 = interfaceID.iloc[h1][i]       
        
        if id1[i] == 0:
            n+=1
            
           
    pointer2 = 0  
    for j in range(pointer2,len(id2)):
        node2 = interfaceID.iloc[h2][j]
        
        pass    
    
    pass




# =============================================================================
# 按照[弧段号，起点，终点，左域，右域]的数据结构存储二维拓扑图
# =============================================================================

    








