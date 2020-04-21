# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 15:13:38 2020

Read borehole geological data from excel.
Generate computable data structures from the read excel data.

pandas的数据结构介绍-CSDN博客
https://blog.csdn.net/hbu_pig/article/details/80278438

Pandas DataFrame 总结 - 简书
https://www.jianshu.com/p/6e35d37e7709

This module should be fully compatible with:
    * Python >=v3.7
    * Spyder >=v4.0

@author: Da YIN
e-mail: forestrock@163.com
"""


import pandas as pd 


# =============================================================================
# 自动为钻孔命名和平面坐标创建对应的代号映射
# 钻探常分为前期勘探、后期补孔，不同时期钻孔的深度和土层分类的粒度会有较大差异
# 此处为了方便实现，只取LocationID为[2,33]的深孔数据进行处理
# =============================================================================
def HID(df):
    ID = []; X = []; Y = []; Z= []; 
    for i in range(df.shape[0]):
        if type(df[df.columns[0]][i]) is int:
            ID.append(df[df.columns[0]][i])
            X.append(df[df.columns[1]][i])
            Y.append(df[df.columns[2]][i])
            Z.append(df[df.columns[3]][i])
            
    data = {'ID':ID,'X':X,'Y':Y,'Z':Z}
    holeID = pd.DataFrame(data)
    
    return holeID


# =============================================================================
# 自动为土层命名创建对应的代号映射表（也可以考虑将常见土层的代号固定下来）
# =============================================================================
def SID(df):
    soil = []; tmp = "";
    for i in range(df.shape[0]):
        # 图集编号+土层命名
        tmp = df[df.columns[3]][i]+df[df.columns[4]][i]
        if not(tmp in soil):
            soil.append(tmp)
    soilID = pd.DataFrame({"soilname":soil})
    
    ID = []; tmp = ""; j = 0;
    for i in range(df.shape[0]):
        tmp = df[df.columns[3]][i]+df[df.columns[4]][i]
        j = soilID.soilname[soilID.soilname.values == tmp].index.tolist()[0]
        # 将数字代号转换为字符代号"A~Z"和"a~z"
        if j < 26 :
            ID.append(chr(65+j))
        else:
            ID.append(chr(97+j))

    df["soilID"] = ID
    
    return df

"""    
后续该处可以更新为映射，精简代码并节省内存、提升计算效率
lsit = [str1,str2,...]
tmp = pd.Series(list)
mapper = {v:k for k,v in enumerate(tmp.unique())}
as_int = tmp.map(mapper) # dtype:int64

ctmp = tmp.cat.categories
ctmp.cat.reorder_categories(mapper).cat.codes # dtype:int8
"""


# =============================================================================
# 按钻孔代号存储钻孔所涉及地质界面点的索引及标高
# =============================================================================
def TopologicalNode(df,holeID):
    tmp = ""; hole = []; interface = []; ID = []; 
    j = 0; k = 0; depth = []; dd = [];
    for i in range(df.shape[0]):
        if (df[df.columns[0]][i] in list(holeID.ID)):           
            if (df[df.columns[0]][i] != tmp):
                if (ID != []):
                    ID.append(j);j+=1;
                    interface.append(ID)
                    dd.append(df[df.columns[2]][k])
                    depth.append(dd)
                    
                tmp = df[df.columns[0]][i]
                hole.append(tmp)
                ID=[]; ID.append(j); j+=1;
                dd=[]; dd.append(df[df.columns[1]][i])
                
            else:
                ID.append(j);j+=1;
                dd.append(df[df.columns[1]][i])                
                k = i
                
    if (ID != []):
        ID.append(j);j+=1;
        dd.append(df[df.columns[2]][k])
        interface.append(ID); depth.append(dd);

    interfaceID = pd.Series(interface,index=hole)
    depthID = pd.Series(depth,index=hole)
    
    return (interfaceID,depthID)


# =============================================================================
# 按钻孔代号存储钻孔所涉及土层的索引及土层代号
# =============================================================================
def DID(df,holeID):
    tmp = ""; hole = []; ID = []; SD = [];
    for i in range(df.shape[0]):
        if (df[df.columns[0]][i] in list(holeID.ID)):
            
            if (df[df.columns[0]][i] != tmp):
                if (ID != []): SD.append(ID)
                tmp = df[df.columns[0]][i]
                hole.append(tmp)
                ID=[]; ID.append(df[df.columns[5]][i])            
            else:
                ID.append(df[df.columns[5]][i])
                
    if (ID!=[]):SD.append(ID)
    domainID = pd.Series(SD,index=hole)
    
    return domainID


# =============================================================================
# 从excel中读取钻孔数据
# =============================================================================
if __name__ == "__main__":
    df1 = pd.read_excel("GeologiclaData.xlsx", "Location")
    df2 = pd.read_excel("GeologiclaData.xlsx", "Data")     
    
    holeID = HID(df1)
    df2 = SID(df2)
    (interfaceID,depthID) = TopologicalNode(df2,holeID)
    domainID = DID(df2,holeID)  
    

