# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 15:36:50 2017

@author: litr2
"""

import numpy as np
import pandas as pd

#==============================================================================
# 以下为测试
#==============================================================================

#    m1 = df1.as_matrix()
#    m2 = df2.as_matrix()
#    
#    res = m1*m2.T
#    
#    row = res.shape[0]
#    col = res.shape[1]
#    
#    l3 = []
#    k = 0
#    minValue = col if row>col else row
#    while(k <minValue):
#        sum = 0
#        for i in range(minValue):  
#        #    for j in range(i, row):
#            for j in range(minValue):
#                if (i+j == k):
#                    sum += res[i,j]
#                    
#        l3.append(sum)
#        k = k +1        
#        print(l3)

#使用数组
#np1 = np.array(df1)
#np2 = np.array(df2)
#
#np2 = np2.reshape(1,len(np2))    
#
#res = np1.dot(np2)

def getResult(df1,df2,k):
    df1 = pd.DataFrame(l1)
    df2 = pd.DataFrame(l2)
    
    m1 = df1.as_matrix()
    m2 = df2.as_matrix()
    
    res = m1*m2.T
    
    row = res.shape[0]
    col = res.shape[1]
    
    judge = row+col-1
    l3 = []
    if(k > judge):
        print('输入的参数k太大请输入 %d 以内的数字' %judge)
        return l3    
    count = 0
#    minValue = col if row>col else row
    while(count < k):
        sum = 0
        for i in range(row):  
            for j in range(col):
                if (i+j == count):
                    sum += res[i,j]
                    
        l3.append(sum)
        count = count +1        
        print(l3)
    return pd.DataFrame(l3,columns=['Predict_Results'])

def getResult2(df1,df2,k):
    df1 = pd.DataFrame(l1)
    df2 = pd.DataFrame(l2)
    
    m1 = df1.as_matrix()
    m2 = df2.as_matrix()
    
    res = m1*m2.T
    
    row = res.shape[0]
    col = res.shape[1]
    
    judge = row+col-1
    l3 = []
    if(k > judge):
        print('输入的参数k太大请输入 %d 以内的数字' %judge)
        return l3    
    count = 1
#    minValue = col if row>col else row
    while(count <= k):
        sum = 0

        for i in range(count if count<=row else row):  
            for j in range(count if count<= col else col):
                if (i+j == count-1):
#                    print(res[i,j])
                    sum += res[i,j]
                    
        l3.append(sum)
        count = count +1        
        print(l3)
    return pd.DataFrame(l3,columns=['Predict_Results'])

def getIndex(df):
    df['indexCol'] = range(df.size)
    colList = list(df)
    colList.insert(0,colList.pop(colList.index('indexCol')))
    df.ix[:, colList]
#    return df

def getIndex2(df):
    index = pd.Series(range(df.size))
    df.insert(0,'index', index)
    

if __name__ == '__main__':
    
    l1 = [1,2,3,4]
    l2 = [1,2,3,4,5,6,7]
    
    df1 = pd.DataFrame(l1)
    df2 = pd.DataFrame(l2)
    
    df_res = getResult2(df1,df2,10)
    
    df_res1 = getResult(df1,df2,10)
#    getIndex2(df_res)
    

            
    
    