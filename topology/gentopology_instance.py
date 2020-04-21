# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 14:56:02 2020

Examples of different cases are given.

This module should be fully compatible with:
    * Python >=v3.7
    * Spyder >=v4.0
    
@author: Da YIN
e-mail: forestrock@163.com

"""


import pandas as pd
import numpy as np


# =============================================================================
# General Format
# 
# 基于对上述特殊实施例的讨论，现在我们可以得出
# 由钻孔数据生成钻孔剖面拓扑图的一般方法。
# 
#     hi: hole_id
#     ds: domain_status
#     nl: node_list
#     nd: node_depth
#     cd: connected_domain
# =============================================================================

# =============================================================================
# 按照[弧段号，起点，终点，左域，右域]的数据结构存储二维拓扑图
# =============================================================================
def gen_topology(hi1, s1, ds1, nl1, nd1, hi2, s2, ds2, nl2, nd2, num_node,
                 interfaceID, num_curve, new_node_list, curve_list):
    cd1 = [i for i,x in enumerate(ds1) if x == 1]
    cd2 = [i for i,x in enumerate(ds2) if x == 1]
        
    u = 0; v = 0;
    for i in range(len(cd1)-1):
        
        # if tmp[i] == 0 : continue
        
        n1 = cd1[i+1]-cd1[i]
        n2 = cd2[i+1]-cd2[i]
        
        if (n1 == 1) and (n2 == 1):
            curve_list.append([num_curve, nl1[i+u], nl2[i+v], 
                          s1[cd1[i]], s1[cd1[i+1]]])
            num_curve += 1
            u += n1-1; v += n2-1; 
            
        elif (n1 > 1) and (n2 == 1):           
            (num_node, new_node_list, num_curve, curve_list) = new_node_hole1(
                hi1, s1, nl1, nd1, cd1, i, n1, hi2, u,
                num_node, new_node_list, num_curve, curve_list)
            
            curve_list.append([num_curve, num_node, nl2[i+v],
                               s1[cd1[i]], s1[cd1[i]+n1]])
            num_curve += 1 
            u += n1-1; v += n2-1;                       
       
        elif (n1 == 1) and (n2 > 1):
            (num_node, new_node_list, num_curve, curve_list) = new_node_hole2(
                hi2, s2, nl2, nd2, cd2, i, n2, hi1, v,
                num_node, new_node_list, num_curve, curve_list)
            
            curve_list.append([num_curve, nl1[i+u], num_node,
                               s1[cd1[i]], s1[cd1[i]+n1]])
            num_curve += 1  
            u += n1-1; v += n2-1; 
            
        else :            
            (num_node, new_node_list, num_curve, curve_list) = new_node_hole1(
                hi1, s1, nl1, nd1, cd1, i, n1, hi2, u,
                num_node, new_node_list, num_curve, curve_list)
                   
            curve_list.append([num_curve, num_node, num_node+1,
                               s1[cd1[i]], s1[cd1[i]+n1]])
            num_curve += 1
            
            (num_node, new_node_list, num_curve, curve_list) = new_node_hole2(
                hi2, s2, nl2, nd2, cd2, i, n2, hi1, v,
                num_node, new_node_list, num_curve, curve_list)  
            u += n1-1; v += n2-1; 

        
    return (num_node, num_curve, new_node_list, curve_list)


# =============================================================================
# 对于非连通域生成相应的拓扑控制点，自动生成相应的钻孔地质剖面拓扑
# =============================================================================
def new_node_hole1(hi1, s1, nl1, nd1, cd1, i, n1, hi2, u,
                   num_node, new_node_list, num_curve, curve_list):
    ''' 生成钻孔1的控制点及拓扑图 '''
    num_node += 1
    depth = nd1[i+u]
    for x in range(1,n1): depth += nd1[i+u+x]
    depth /= n1;
    new_node = [num_node,hi1,hi2,depth] 
    new_node_list.append(new_node) 
    
    for x in range(0,n1):
        curve_list.append([num_curve, nl1[i+u+x], num_node,
                      s1[cd1[i]+x],s1[cd1[i]+x+1]])
        num_curve += 1
        
    return (num_node, new_node_list, num_curve, curve_list)


def new_node_hole2(hi2, s2, nl2, nd2, cd2, i, n2, hi1, v,
                   num_node, new_node_list, num_curve, curve_list):
    ''' 生成钻孔2的控制点及拓扑图 '''
    num_node += 1
    depth = nd2[i+v]
    for x in range(1,n2): depth += nd2[i+v+x]
    depth /= n2;
    new_node = [num_node,hi2,hi1,depth] 
    new_node_list.append(new_node) 
    
    for x in range(0,n2):
        curve_list.append([num_curve, num_node, nl2[i+v+x], 
                      s2[cd2[i]+x],s2[cd2[i]+x+1]])
        num_curve += 1
        
    return (num_node, new_node_list, num_curve, curve_list)

 

if __name__ == "__main__":    
    from connecteddomain import LCS   
    
    # Enter an arbitrary string representing the 
    # geological stratification of the borehole.
    s1 = "[ABCDEAF]"   
    s2 = "[ACDAEDF]"

    hi1 = 0; hi2 = 1;
    nl1 = []
    for x in range(len(s1)-1): nl1.append(x)
    nd1 = []
    for x in range(len(s1)-1): nd1.append(0.0+1.5*x)
    
    nl2 = []
    for x in range(len(s2)-1): nl2.append(len(nl1)+x)
    nd2 = []
    for x in range(len(s2)-1): nd2.append(0.0+1.6*x)
    
    (lcs,ds1,ds2)=LCS(s1, s2)
    interfaceID = pd.Series([nl1,nl2])
    
    # 新节点编号紧接原节点编号
    num_node = max(interfaceID.max())
    num_curve = 0; new_node_list = []; curve_list = [];   
    
    (num_node, num_curve, new_node_list, curve_list) = gen_topology(
        hi1, s1, ds1, nl1, nd1, hi2, s2, ds2, nl2, nd2, num_node, 
        interfaceID, num_curve, new_node_list, curve_list)         
           
    # print(new_node_list)
    # print(curve_list)    
    
    
# =============================================================================
#     剖面可视化
# =============================================================================
    import matplotlib.pyplot as plt
    import networkx as nx 
    
    holes = np.array([[0,0,1],[100,80,1]])
    
    # 更新所有节点三维坐标（包括新增节点）
    depthID = pd.Series([nd1,nd2])
    nodes = []
    for i in range(len(holes)):
        for j in range(len(interfaceID.iloc[i])):
            n_id = interfaceID.iloc[i][j]
            x = holes[i][0]
            y = holes[i][1]
            z = holes[i][2] - depthID.iloc[i][j]
            nodes.append([n_id, x, y, z]) 
    
    for i in range(len(new_node_list)):
        n_id,j,k,z = new_node_list[i]
        x = (4 * holes[j][0]+holes[k][0])/5
        y = (4 * holes[j][1]+holes[k][1])/5
        z = (holes[j][2]+holes[k][2])/2 - z
        nodes.append([n_id, x, y, z])    
    
    # 列出指定钻孔区间剖面涉及到的所有节点
    int_list = []
    int_list += interfaceID.iloc[hi1]
    int_list += interfaceID.iloc[hi2]
    for i in range(len(new_node_list)):
        if [hi1,hi2] == new_node_list[i][1:3]:
            int_list.append(new_node_list[i][0])
        elif [hi2,hi1] == new_node_list[i][1:3]:
            int_list.append(new_node_list[i][0])
            
    # 为绘制钻孔剖面创建一个节点的二维坐标array
    h1_loc = holes[hi1]
    vertices = np.zeros([len(nodes),2])
    for i in range(len(int_list)):
        n_id = int_list[i]
        dist = np.sqrt(np.power(h1_loc[0]-nodes[n_id][1],2)
                    + np.power(h1_loc[1]-nodes[n_id][2],2))
        elev = nodes[n_id][3]
        vertices[n_id] = [dist,elev]
        
    pos = dict(zip(np.array(int_list),vertices))  

    # 列出指定钻孔区间剖面涉及到的所有拓扑线
    c_section = []
    G = nx.path_graph(0) 
    for i in range(len(curve_list)):
        n1_id, n2_id = curve_list[i][1:3]
        if n1_id in int_list and n2_id in int_list:
            c_section.append(curve_list[i])
            G.add_edge(n1_id,n2_id)

    plt.figure(figsize=(10,10))
    nx.draw(G,pos,with_labels=True) 
    plt.show() 
