# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 10:51:37 2017

@author: litr2
"""

#==============================================================================
#新统计数量（通过格式化日期的形式） 
#==============================================================================
import pandas as pd 
import numpy as np
import types
import math
#获得类型列表
def getTypeList(df):
    lst=[]
    for o in df.Return_apc_code:
        if o not in lst:
            lst.append(o)
    return lst        

#根据类型列表返回对应df list
def getDfByTypesWithList(df_prototype, typeList):
    lst = []
    for t in typeList:
        lst.append(df_prototype[df_prototype['Return_apc_code']==t])
    return lst    

#根据类型列表返回对回应dict
def getDfByTypesWithDict(df_prototype, typeList):
    dic = {}
    for t in typeList:
        dic[t] = df_prototype[df_prototype['Return_apc_code']==t]
    return dic  

#添加新列并格式化日期（不转为datetime）
def preFormateDate(dfList=None,df_t=None):
    if dfList == None:
        preFormateDateSub(df_t)
    else:
        for l in dfList:
            preFormateDateSub(l)

#格式化日期子函数
def preFormateDateSub2(df_t):
    df_t.insert(0,'date_a',df_t['Phone_Activation_date'])
    df_t.insert(1,'date_r',df_t['Return_RECEIVED_DT'])
    df_t = df_t.dropna(subset=['Phone_Activation_date'])
    df_t = df_t.dropna(subset=['Return_RECEIVED_DT'])
    if isinstance(df_t['Phone_Activation_date'][0] ,str):
        df_t['date_a'] = df_t['date_a'].map(lambda x:(x if len(x)<=10 else x[:11]))
    else:
        df_t['date_a'] = df_t['date_a'].map(lambda x:str(x))
        df_t['date_a'] = df_t['date_a'].map(lambda x:(x if len(x)<=10 else x[:11]))
    if isinstance(df_t['Return_RECEIVED_DT'][0] ,str):
        df_t['date_r'] = df_t['date_r'].map(lambda x:(x if len(x)<=10 else x[:11]))
    else:
        df_t['date_r'] = df_t['date_r'].map(lambda x:str(x))
        df_t['date_r'] = df_t['date_r'].map(lambda x:(x if len(x)<=10 else x[:11]))

def preFormateDateSub(df_t):
    df_t.insert(0,'date_a',df_t['Phone_Activation_date'])
    df_t.insert(1,'date_r',df_t['Return_RECEIVED_DT'])
    df_t = df_t.dropna(subset=['Phone_Activation_date'])
    df_t = df_t.dropna(subset=['Return_RECEIVED_DT'])    
    df_t['date_a'] = df_t['date_a'].map(lambda x:str(x))
    df_t['date_a'] = df_t['date_a'].map(lambda x:(x if len(x)<=10 else x[:11]))   
    df_t['date_r'] = df_t['date_r'].map(lambda x:str(x))
    df_t['date_r'] = df_t['date_r'].map(lambda x:(x if len(x)<=10 else x[:11]))
        
#根据日期算出间隔月数(参数除去df外，给定最小值，最大值,不给定则用默认值)
def calculateGapMonthSub(df,minValue=None,maxValue=None):
    #算出间隔多少天
    df['gap'] = pd.to_datetime(df.date_r)-pd.to_datetime(df.date_a)
    #算出间隔多少月
    df['gap_month'] = df.gap.map(lambda x:x/np.timedelta64(3600*24*30,'s'))
    #根据gap_month统计结果
    minV = df.gap_month.min()
    maxV = df.gap_month.max()
    dic={}
    lst=[]
    #需要优化，，很慢大约10-30分钟
    if (minValue==None) | (maxValue==None):
        for i in range(0,20):
            tmp_df = df[(df.gap_month<i+1)&(df.gap_month>=i-1)]
            count = 1
            tmp_s = tmp_df.Return_mclaim_ref
            for o in tmp_s:
                if o not in lst:
                    lst.append(o)
                else:
                    count= count+1
            dic[i] = count
    else:
        for i in range(minV,maxV):
            dic[i] = df[(df.gap_month<i+1)&(df.gap_month>=i-1)].Return_mclaim_ref.sum()
    return dic 
#计算月的总和
def calculateGapMonth(lst, typeList):
    dic = {}
    for t in range(len(typeList)):
        dic[typeList[t]] = calculateGapMonthSub(lst[t])
    return dic
       
#保存不同类型数据
def saveCsvByType(dic, filePath, nameSub):    
    for k,v in dic.items():
        tmp = pd.DataFrame.from_dict(v,orient='index')
        tmp.to_csv(path_or_buf=filePath+'\\'+k+nameSub+'.csv')    
    
    
if __name__=='__main__':
    #0.重新获取数据csv（格式化日期形式）
    fPath = r'E:\Phone_Data\Return 1 --ML_LA_Return_date_with_Act.csv'
    #1.读取数据
    df = pd.read_csv(fPath)
    #2.获得型号列表list
    typeList = getTypeList(df)
    #3.获得不同型号的df返回的是dict
    dfList = getDfByTypesWithList(df,typeList)
    #4.格式化日期第一步
    preFormateDate(dfList)
    #5.计算总和
    dic_res = calculateGapMonth(dfList,typeList)
    #6.保存
    filePath = r'E:\Phone_Data\AllTypesReturnFrom'
    nameSub = '_return_from0'
    saveCsvByType(dic_res, filePath, nameSub)
