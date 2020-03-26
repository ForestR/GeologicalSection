# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 21:41:13 2020

Longest Common Substring Algorithm

This module should be fully compatible with:
    * Python >=v3.7
    * Spyder >=v4.0
    
@author: Da YIN
e-mail: forestrock@163.com
"""


import numpy as np


# =============================================================================
# 使用二维数组C[m,n] 
# c[i,j]记录序列Xi和Yj的最长公共子序列的长度。 
# 当i=0或j=0时，空序列是Xi和Yj的最长公共子序列，故c[i,j]=0
# 
# 使用二维数据B[m,n]，其中，b[i,j]标记c[i,j]的值是由哪一个子问题的解达到的。
# 即c[i,j]是由c[i-1,j-1]+1或者c[i-1,j]或者c[i,j-1]的哪一个得到的。
# 取值范围为LeftTop ↖，Left ←，Top ↑ 三种情况
# =============================================================================
def LCS(s1, s2):
    size1 = len(s1) + 1
    size2 = len(s2) + 1
    # 程序多加一行，一列，方便后面代码编写
    id1 = np.zeros(size1-1)
    id2 = np.zeros(size2-1)
    chess = [[["", 0] for j in list(range(size2))] for i in list(range(size1))]
    for i in list(range(1, size1)):
        chess[i][0][0] = s1[i - 1]
    for j in list(range(1, size2)):
        chess[0][j][0] = s2[j - 1]
#    print("初始化数据：")
#    print(chess)
    for i in list(range(1, size1)):
        for j in list(range(1, size2)):
            if s1[i - 1] == s2[j - 1]:
                chess[i][j] = ['↖', chess[i - 1][j - 1][1] + 1]            
            elif chess[i][j - 1][1] > chess[i - 1][j][1]:
                chess[i][j] = ['←', chess[i][j - 1][1]]
            else:
                chess[i][j] = ['↑', chess[i - 1][j][1]]
#    print("计算结果：")
#    print(chess)
    i = size1 - 1
    j = size2 - 1
    s3 = []
    while i > 0 and j > 0:
        if chess[i][j][0] == '↖':
            s3.append(chess[i][0][0])
            i -= 1
            j -= 1
            id1[i] = 1.    
            id2[j] = 1.
        if chess[i][j][0] == '←':
            j -= 1
        if chess[i][j][0] == '↑':
            i -= 1
    s3.reverse()
#    print("最长公共子序列：%s" % ''.join(s3))
    return (s3,id1,id2)


# =============================================================================
# 输出最大公共字符串，以及 str1.LCS，str2.LCS 的位置list
# =============================================================================
if __name__ == "__main__":
    import time
    start = time.time() 
      
    str1 = "ABCDEFG"
    str2 = "ACDCEF"
    (lcs,id1,id2)=LCS(str1, str2)
    print(lcs,"\n",id1,"\n",id2)
    
    end = time.time()
    print(end-start)


