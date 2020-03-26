# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 14:24:55 2020

Generate the neighborhood diagram of the borehole.

This module should be fully compatible with:
    * Python >=v3.7
    * Spyder >=v4.0
    
@author: Da YIN
e-mail: forestrock@163.com
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi


# =============================================================================
# Reconstruct infinite voronoi regions in a 2D diagram to finite
# regions.
# 
# Parameters
# ----------
# vor : Voronoi
#     Input diagram
# radius : float, optional
#     Distance to 'points at infinity'.
# 
# Returns
# -------
# regions : list of tuples
#     Indices of vertices in each revised Voronoi regions.
# vertices : list of tuples
#     Coordinates for revised Voronoi vertices. Same as coordinates
#     of input vertices, with 'points at infinity' appended to the
#     end.
# =============================================================================
def voronoi_finite_polygons_2d(vor, radius=None):
    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()
    center = vor.points.mean(axis=0)
    
    if radius is None:
        radius = vor.points.ptp().max()

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge
            t = vor.points[p2] - vor.points[p1] # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]
        # finish
        new_regions.append(new_region.tolist())
        
    return new_regions, np.asarray(new_vertices)


# =============================================================================
# 对处于XY平面的钻孔点进行voronoi剖分，形成泰森多边形格网。进而确定钻孔点的邻点
# points : numpy.ndarray
#     Input drilling coordinates X,Y
# =============================================================================
def drilling_floor_plan(points=None):   
    if points is None:
        # make up data points
        np.random.seed(1551)
        points = np.random.rand(15, 2)
    # compute Voronoi tesselation
    vor = Voronoi(points)
    
    # plot
    regions, vertices = voronoi_finite_polygons_2d(vor)
#    print("--"); print(regions); print("--"); print(vertices);
    
    # colorize
    for region in regions:
        polygon = vertices[region]
        plt.fill(*zip(*polygon), alpha=0.6)
    
#    plt.plot(points[:,0], points[:,1], 'ko')
    for i in range(points.shape[0]):
        plt.plot(points[i,0], points[i,1], 'ko')
        plt.annotate(r'$%s$'%i,xy=(points[i,0],points[i,1]),xytext=(+3,-15),
                     textcoords='offset points',fontsize=16)
    
    plt.xlim(vor.min_bound[0] - 0.1, vor.max_bound[0] + 0.1)
    plt.ylim(vor.min_bound[1] - 0.1, vor.max_bound[1] + 0.1)
    plt.show()
    
    # 读取钻孔点邻点的集合(p,v,v)，p为邻域，v为泰森多边形公共边的顶点
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))
    i=7; print("编号为%s的钻孔点的邻域集为\n"%i,all_ridges[i])

    return all_ridges


# =============================================================================
# 调用ReadData.py中的HID函数，获取钻孔点集合holeID，
# 调用drilling_floor_plan()，得到钻孔点的邻域集neighbourhood
# =============================================================================
if __name__ == "__main__":  
    import pandas as pd
    from ReadData import HID
    
#     df1 = pd.read_excel("GeologiclaData.xlsx", "Location")
# #    df2 = pd.read_excel("GeologiclaData.xlsx", "Data")
#     holeID = HID(df1)
    
#     points = holeID.values[:,1:3]
    nbh = drilling_floor_plan()
    
    
    
