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
from connecteddomain import LCS
import gentopology_instance as gi


# =============================================================================
# 依次两两比较相邻钻孔，由LCS判别土层代号字符串的公共子序列（即连通域）
# =============================================================================
def neighbourhood(nbh, domainID, interfaceID, depthID):
    num_node = max(interfaceID.max());
    num_curve = 0; new_node_list = []; curve_list = [];
    for i in range(len(nbh)):
        tmp = [str(x) for x in domainID.iloc[i]]
        s1 = "["+''.join(tmp)+"]"
        for j in range(len(nbh[i])):
            n = nbh[i][j][0]
            # 单向比较
            if n > i:
                tmp = [str(x) for x in domainID.iloc[n]]
                s2 = "["+''.join(tmp)+"]"     
                
                nl1 = interfaceID.iloc[i]
                nd1 = depthID.iloc[i]              
                
                nl2 = interfaceID.iloc[n]
                nd2 = depthID.iloc[n]
                
                (lcs,ds1,ds2)=LCS(s1, s2)
                              
                (num_node, num_curve, new_node_list, curve_list) = gi.gen_topology(
                    i, s1, ds1, nl1, nd1, n, s2, ds2, nl2, nd2, num_node,
                    interfaceID, num_curve, new_node_list, curve_list)     
   
    return (new_node_list, curve_list)
        


if __name__ == "__main__":
    
    import readdata as rd
    from voronoi import drilling_floor_plan
    
    df1 = pd.read_excel("GeologiclaData.xlsx", "Location")
    df2 = pd.read_excel("GeologiclaData.xlsx", "Data")     
    
    holeID = rd.HID(df1)
    df2 = rd.SID(df2)
    (interfaceID,depthID) = rd.TopologicalNode(df2,holeID)
    domainID = rd.DID(df2,holeID)  
    
    points = holeID.values[:,1:3]
    nbh = drilling_floor_plan(points)
       
    (new_node_list, curve_list) = neighbourhood(
        nbh, domainID, interfaceID, depthID)
    
