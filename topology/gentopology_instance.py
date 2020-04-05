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
# Case_1 
# 
# 最简单的情形，上下域为空集Ø，中间土层为单连通域A，记为[A]。
# Case_1是最常见也最为简单的层状地质构造。
# 
#     ds: domain_status 表示是否为邻接钻孔剖面上的单连通域
#     nl: node_list 表示钻孔土质分界面上的节点集合
#     cd: connected_domain 连通域在ds向量上的索引集合
# =============================================================================
# s1 = "[A]"
# ds1 = np.array([1,1,1])
# nl1 = [10,11]
# cd1 = [i for i,x in enumerate(ds1) if x == 1]

# s2 = "[A]"
# ds2 = np.array([1,1,1])
# nl2 = [20,21]
# cd2 = [i for i,x in enumerate(ds2) if x == 1]

# curve_c1 = []; num_curve = 0;
# for i in range(len(cd1)-1):
#     curve_c1.append([num_curve, nl1[i], nl2[i], 
#                   s1[cd1[i]], s2[cd1[i+1]]])
#     num_curve += 1

# print(curve_c1)


# =============================================================================
# Case_2
# 
# 较复杂的情形，钻孔1中存在非连通域B，其钻孔地质表达为[AB]，
# 钻孔2不存在非连通域，其表达为[A]。
# 我们需要为钻孔1的非连通域B新建一个拓扑控制点P，并将其
# 存储为[新建节点号，归属钻孔号，节点虚拟深度]。
# 
#     hi: hole_id 钻孔编号
#     ds: domain_status
#     nl: node_list
#     nd: node_depth 以钻孔孔口为基准的节点深度集合
#     cd: connected_domain
# =============================================================================
# hi1 = 1
# s1 = "[AB]"
# ds1 = np.array([1,1,0,1])
# nl1 = [10, 11, 12]
# nd1 = [0.0, 3.2, 5.6]
# cd1 = [i for i,x in enumerate(ds1) if x == 1]

# hi2 = 2
# s2 = "[A]"
# ds2 = np.array([1,1,1])
# nl2 = [20, 21]
# nd2 = [0.0, 3.4]
# cd2 = [i for i,x in enumerate(ds2) if x == 1]

# interfaceID = pd.Series([nl1,nl2])

# curve_c2 = []; num_curve = 0;
# # 新节点编号紧接原节点编号
# num_node = max(interfaceID.max());
# for i in range(len(cd1)-1):
#     if (cd1[i+1]-cd1[i] == 1) and (cd2[i+1]-cd2[i] == 1):
#         curve_c2.append([num_curve, nl1[i], nl2[i], 
#                       s1[cd1[i]], s1[cd1[i+1]]])
#         num_curve += 1
        
#     elif (cd1[i+1]-cd1[i] > 1) and (cd2[i+1]-cd2[i] == 1):
#         num_node += 1
#         depth = (nd1[i] + nd1[i+1]) /2;
#         # 新节点[节点号，钻孔号，假定深度]
#         new_node = [num_node,hi1,depth]             
        
#         curve_c2.append([num_curve, nl1[i], new_node[0], 
#                       s1[cd1[i]], s1[cd1[i]+1]])
#         num_curve += 1
        
#         curve_c2.append([num_curve, nl1[i+1], new_node[0], 
#               s1[cd1[i]+1], s1[cd1[i]+2]])
#         num_curve += 1
        
#         curve_c2.append([num_curve, new_node[0], nl2[i], 
#               s1[cd1[i]], s1[cd1[i]+2]])
#         num_curve += 1
    
#     elif (cd1[i+1]-cd1[i] == 1) and (cd2[i+1]-cd2[i] > 1):
#         pass
        
#     else :
#         pass

# print(new_node)
# print(curve_c2)


# =============================================================================
# Case_3
# 
# 与例2相反，钻孔1不存在非连通域，其表达为[A]
# 钻孔2中存在非连通域B，其钻孔地质表达为[AB]。
# 
#     hi: hole_id
#     ds: domain_status
#     nl: node_list
#     nd: node_depth
#     cd: connected_domain
# =============================================================================
# hi1 = 1
# s1 = "[A]"
# ds1 = np.array([1,1,1])
# nl1 = [10, 11]
# nd1 = [0.0, 3.2]
# cd1 = [i for i,x in enumerate(ds1) if x == 1]

# hi2 = 2
# s2 = "[AB]"
# ds2 = np.array([1,1,0,1])
# nl2 = [20, 21, 22]
# nd2 = [0.0, 3.4, 4.0]
# cd2 = [i for i,x in enumerate(ds2) if x == 1]

# interfaceID = pd.Series([nl1,nl2])

# curve_c3 = []; num_curve = 0;
# # 新节点编号紧接原节点编号
# num_node = max(interfaceID.max());
# for i in range(len(cd1)-1):
#     if (cd1[i+1]-cd1[i] == 1) and (cd2[i+1]-cd2[i] == 1):
#         curve_c3.append([num_curve, nl1[i], nl2[i], 
#                       s1[cd1[i]], s1[cd1[i+1]]])
#         num_curve += 1
        
#     elif (cd1[i+1]-cd1[i] > 1) and (cd2[i+1]-cd2[i] == 1):
#         pass
    
#     elif (cd1[i+1]-cd1[i] == 1) and (cd2[i+1]-cd2[i] > 1):
#         num_node += 1
#         depth = (nd2[i] + nd2[i+1]) /2;
#         # 新节点[节点号，钻孔号，假定深度]
#         new_node = [num_node,hi2,depth]  
        
#         curve_c3.append([num_curve, nl1[i], new_node[0], 
#                       s1[cd1[i]], s1[cd1[i]+1]])
#         num_curve += 1
        
#         curve_c3.append([num_curve, new_node[0], nl2[i], 
#                       s1[cd1[i]], s2[cd2[i]+1]])
#         num_curve += 1
        
#         curve_c3.append([num_curve, new_node[0], nl2[i+1], 
#                       s2[cd2[i]+1], s2[cd2[i]+2]])
#         num_curve += 1
        
#     else :
#         pass        

# print(new_node)
# print(curve_c3)


# =============================================================================
# Case_4
# 
# 更复杂的，钻孔1存在非连通域B，其表达为[AB]
# 钻孔2中存在非连通域C，其钻孔地质表达为[AC]。
# 
#     hi: hole_id
#     ds: domain_status
#     nl: node_list
#     nd: node_depth
#     cd: connected_domain
# =============================================================================
# hi1 = 1
# s1 = "[AB]"
# ds1 = np.array([1,1,0,1])
# nl1 = [10, 11, 12]
# nd1 = [0.0, 3.2, 6.4]
# cd1 = [i for i,x in enumerate(ds1) if x == 1]

# hi2 = 2
# s2 = "[AC]"
# ds2 = np.array([1,1,0,1])
# nl2 = [20, 21, 22]
# nd2 = [0.0, 3.4, 4.0]
# cd2 = [i for i,x in enumerate(ds2) if x == 1]

# interfaceID = pd.Series([nl1,nl2])

# curve_c4 = []; num_curve = 0;
# # 新节点编号紧接原节点编号
# num_node = max(interfaceID.max())
# new_node_list = []
# for i in range(len(cd1)-1):
#     if (cd1[i+1]-cd1[i] == 1) and (cd2[i+1]-cd2[i] == 1):
#         curve_c4.append([num_curve, nl1[i], nl2[i], 
#                       s1[cd1[i]], s1[cd1[i+1]]])
#         num_curve += 1
        
#     elif (cd1[i+1]-cd1[i] > 1) and (cd2[i+1]-cd2[i] == 1):
#         pass
    
#     elif (cd1[i+1]-cd1[i] == 1) and (cd2[i+1]-cd2[i] > 1):
#         pass
        
#     else :
#         num_node += 1
#         depth = (nd1[i] + nd1[i+1]) /2;
#         new_node1 = [num_node,hi1,depth] 
#         new_node_list.append(new_node1)
        
#         num_node += 1
#         depth = (nd2[i] + nd2[i+1]) /2;
#         new_node2 = [num_node,hi2,depth]  
#         new_node_list.append(new_node2)
        
#         curve_c4.append([num_curve, nl1[i], new_node1[0],
#                           s1[cd1[i]],s1[cd1[i]+1]])
#         num_curve += 1
        
#         curve_c4.append([num_curve, nl1[i+1], new_node1[0],
#                           s1[cd1[i]+1],s1[cd1[i]+2]])
#         num_curve += 1
        
#         curve_c4.append([num_curve, new_node1[0], new_node2[0],
#                           s1[cd1[i]], s1[cd2[i]+2]])
#         num_curve += 1
        
#         curve_c4.append([num_curve, new_node2[0], nl2[i], 
#                       s2[cd2[i]], s2[cd2[i]+1]])
#         num_curve += 1
        
#         curve_c4.append([num_curve, new_node2[0], nl2[i+1], 
#                       s2[cd2[i]+1], s2[cd2[i]+2]])
#         num_curve += 1
        
# print(new_node_list)
# print(curve_c4)


# =============================================================================
# Case_5
# 
# 对Case_2扩充，当钻孔1存在连续的非连通域B和C，其表达为[ABC]
# 钻孔2中不存在非连通域，其钻孔地质表达为[A]。
# 
#     hi: hole_id
#     ds: domain_status
#     nl: node_list
#     nd: node_depth
#     cd: connected_domain
# =============================================================================
# hi1 = 1
# s1 = "[ABC]"
# ds1 = np.array([1,1,0,0,1])
# nl1 = [10, 11, 12, 13]
# nd1 = [0.0, 3.2, 6.4, 7.0]
# cd1 = [i for i,x in enumerate(ds1) if x == 1]

# hi2 = 2
# s2 = "[A]"
# ds2 = np.array([1,1,1])
# nl2 = [20, 21]
# nd2 = [0.0, 3.4]
# cd2 = [i for i,x in enumerate(ds2) if x == 1]

# interfaceID = pd.Series([nl1,nl2])

# curve_c5 = []; num_curve = 0;
# # 新节点编号紧接原节点编号
# num_node = max(interfaceID.max())
# new_node_list = []
# for i in range(len(cd1)-1):
    
#     # n1 为连续邻接的非连通域的个数+1
#     n1 = cd1[i+1]-cd1[i]
    
#     if (n1 == 1) and (cd2[i+1]-cd2[i] == 1):
#         curve_c5.append([num_curve, nl1[i], nl2[i], 
#                       s1[cd1[i]], s1[cd1[i+1]]])
#         num_curve += 1
        
#     elif (n1 > 1) and (cd2[i+1]-cd2[i] == 1):
#         num_node += 1
#         depth = nd1[i]
#         for x in range(1,n1): depth += nd1[i+x]
#         depth /= n1;
#         new_node1 = [num_node,hi1,depth] 
#         new_node_list.append(new_node1)
        
#         curve_c5.append([num_curve, nl1[i], new_node1[0],
#                           s1[cd1[i]],s1[cd1[i]+1]])
#         num_curve += 1
        
        
#         for x in range(1,n1):
#             curve_c5.append([num_curve, nl1[i+x], new_node1[0],
#                           s1[cd1[i]+x],s1[cd1[i]+x+1]])
#             num_curve += 1
        
#         curve_c5.append([num_curve, new_node1[0], nl2[i],
#                           s1[cd1[i]], s1[cd2[i]+n1]])
#         num_curve += 1
   
#     elif (n1 == 1) and (cd2[i+1]-cd2[i] > 1):
#         pass
        
#     else :
#         pass        
        
# print(new_node_list)
# print(curve_c5)


# =============================================================================
# Case_6
# 
# 当连通域判别存在二义性时，例如钻孔1表达为[ABC]，钻孔2为[BAC]时，
# 我们可以记其连通域为{AC}, ds1=[11011], ds2=[10111];
# 也可以记为{BC}, ds1=[10111], ds2=[11011];
# 
#     hi: hole_id
#     ds: domain_status
#     nl: node_list
#     nd: node_depth
#     cd: connected_domain
# =============================================================================









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
