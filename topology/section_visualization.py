# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 10:30:27 2020

Visualization of arbitrary adjacent borehole 
profile topology based on networkx.

钻孔剖面可视化。

This module should be fully compatible with:
    * Python >=v3.7
    * Spyder >=v4.0

@author: Da YIN
e-mail: forestrock@163.com
"""


import matplotlib.pyplot as plt
import networkx as nx 
import numpy as np


# =============================================================================
# 更新所有节点三维坐标（包括新增节点）
# =============================================================================    
def update_nodes(holeID, interfaceID, depthID, new_node_list):
    nodes = []
    for i in range(len(holeID)):
      
        for j in range(len(interfaceID.iloc[i])):
            n_id = interfaceID.iloc[i][j]
            x,y = holeID.iloc[i][1:3]
            z = holeID.iloc[i][3] - depthID.iloc[i][j]
            nodes.append([n_id, x, y, z])     
            
    for i in range(len(new_node_list)):
        n_id,j,k,z = new_node_list[i]
        x = (4 * holeID.iloc[j][1]+holeID.iloc[k][1])/5
        y = (4 * holeID.iloc[j][2]+holeID.iloc[k][2])/5
        z = (holeID.iloc[j][3]+holeID.iloc[k][3])/2 - z
        nodes.append([n_id, x, y, z])
        
    return nodes


# =============================================================================
# 更新钻孔原有界面点的拓扑连线
# =============================================================================
def update_curves(curve_list, holeID, domainID, interfaceID):
    num_curve = len(curve_list)
    for i in range(len(holeID)):
        
        for j in range(len(domainID.iloc[i])):
            c_id = num_curve
            n1_id = interfaceID.iloc[i][j]
            n2_id = interfaceID.iloc[i][j+1]
            d1_code = domainID.iloc[i][j]
            d2_code = domainID.iloc[i][j]
            
            curve_list.append([c_id, n1_id, n2_id, d1_code, d2_code])
            num_curve += 1
            
    return curve_list
        
        
# =============================================================================
# 列出指定钻孔区间剖面涉及到的所有节点
# =============================================================================
def section_nodes_3d(h1_id, h2_id, interfaceID, new_node_list):
    int_list = []
    
    # 原有节点
    int_list += interfaceID.iloc[h1_id]
    int_list += interfaceID.iloc[h2_id]
    
    # 新增节点
    for i in range(len(new_node_list)):
        
        if [h1_id,h2_id] == new_node_list[i][1:3]:
            int_list.append(new_node_list[i][0])
            
        elif [h2_id,h1_id] == new_node_list[i][1:3]:
            int_list.append(new_node_list[i][0])
    
    return int_list


# =============================================================================
# 列出指定钻孔区间剖面涉及到的所有拓扑线
# =============================================================================
def section_curves(curve_list, int_list):
    # c_section = []
    G = nx.path_graph(0) 
    
    for i in range(len(curve_list)):
        n1_id, n2_id = curve_list[i][1:3]
        
        if n1_id in int_list and n2_id in int_list:
            # c_section.append(curve_list[i])
            G.add_edge(n1_id,n2_id)
            
    return G


# =============================================================================
# 为绘制钻孔剖面创建一个节点的二维坐标array
# =============================================================================
def section_nodes_2d(h1_id, holeID, nodes, int_list):
    h1_loc = holeID.iloc[h1_id]
    vertices = np.zeros([len(nodes),2])
    
    for i in range(len(int_list)):
        n_id = int_list[i]
        dist = np.sqrt(np.power(h1_loc[1]-nodes[n_id][1],2)
                   + np.power(h1_loc[2]-nodes[n_id][2],2))
        elev = nodes[n_id][3]
        
        vertices[n_id] = [dist,elev]
        
    return vertices


# =============================================================================
# 生成剖面上地层的多边形顶点集合regions
# =============================================================================
def section_regions(h1_id, h2_id, G, interfaceID):
    regions = []  
    regions = section_path(h1_id, G, interfaceID, regions)   
    regions = section_path(h2_id, G, interfaceID, regions)
    
    return regions
    

# =============================================================================
# 应用networkx找出图中环的最短路径
# =============================================================================
def section_path(h, G, interfaceID, regions):
    for i in range(len(interfaceID.iloc[h])-1):
        n1_id = interfaceID.iloc[h][i]
        n2_id = interfaceID.iloc[h][i+1]
        
        # 删去判断过的钻孔界面点
        G.remove_edge(n1_id,n2_id) 
        
        if nx.has_path(G,n1_id,n2_id):
            region = nx.shortest_path(G, source=n1_id, target=n2_id)
            regions.append(region)    
    
    return regions





if __name__ == "__main__":

    import pandas as pd
    import readdata as rd
    from voronoi import drilling_floor_plan
    from gentopology import neighbourhood
    
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
    
    
    # 指定用于生成剖面的邻接钻孔
    h1_id = 23; h2_id = 24; 
   
    
    nodes = update_nodes(holeID, interfaceID, depthID, new_node_list)
    
    curve_list = update_curves(curve_list, holeID, domainID, interfaceID)    
    int_list = section_nodes_3d(h1_id, h2_id, interfaceID, new_node_list)
    
    G = section_curves(curve_list, int_list)
      
    vertices = section_nodes_2d(h1_id, holeID, nodes, int_list)
    pos = dict(zip(np.array(nodes)[:,0],vertices))  
    
    
    plt.figure(figsize=(10,10))
    nx.draw(G,pos,with_labels=True) 
    plt.show()     
    
           
    plt.figure(figsize=(10,10))
    
    # nodes
    nx.draw_networkx_nodes(G,pos,int_list,node_size=50,node_color='r',with_labels=True)
    
    # # edges
    # nx.draw_networkx_edges(G,pos,width=6)
    
    # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    
    # colorize
    regions = section_regions(h1_id, h2_id, G, interfaceID)
    for region in regions:
        polygon = vertices[region]
        plt.fill(*zip(*polygon), alpha=0.6)   
    
    plt.show()
