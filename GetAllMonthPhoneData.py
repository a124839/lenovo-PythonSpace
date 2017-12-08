# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 16:17:46 2017

@author: litr2
"""
import pandas as pd 
import numpy as np

#==============================================================================
#获得各类型各月的手机激活数据
#==============================================================================

#获得类型列表
def getTypeList(df):
    lst=[]
    for o in df.APC_CODE:
        if o not in lst:
            lst.append(o)
    return lst        

#根据类型列表返回对应df list
def getDfByTypesWithList(df_prototype, typeList):
    lst = []
    for t in typeList:
        lst.append(df_prototype[df_prototype['APC_CODE']==t])
    return lst    

#根据类型列表返回对回应dict
def getDfByTypesWithDict(df_prototype, typeList):
    dic = {}
    for t in typeList:
        dic[t] = df_prototype[df_prototype['APC_CODE']==t]
    return dic  

# 得到范围数据
def getRangeData(start, end):
    lst = []
    for i in range(start,end):
        lst.append(i)
    return lst

#针对不同的年月统计数量子函数
def getAllDataSub(df, year_lst, month_lst):
    dt = {}
    for y in year_lst:
        for m in month_lst:
            # 筛选列中数据
            tmp =df[(df.year_A==y)&(df.month_a==m)]
            tsum = tmp.activation.sum()
            dt[str(y)+'-'+str(m)] = tsum
    return dt

#针对不同的年月统计激活数量函数
def getAllData(df_lst, year_lst, month_lst, typeList):
    dic={}
    for d in range(len(df_lst)):
        dic[typeList[d]]= getAllDataSub(df_lst[d],year_lst,month_lst)
    return dic

#保存所文件到文件夹
def saveCsvByType(dic,path,nameSub):    
    for k,v in dic.items():
        tmp = pd.DataFrame.from_dict(v,orient='index')
        tmp.columns = ['total_activation']
        tmp.to_csv(path_or_buf=path+'\\'+k+nameSub+'.csv')

#添加新列并格式化日期（不转为datetime）
def preFormateDate(dfList=None,df_t=None):
    if dfList == None:
        preFormateDateSub(df_t)
    else:
        for l in dfList:
            preFormateDateSub(l)

#格式化日期子函数
def preFormateDateSub(df_t):
    df_t.insert(0,'date_a',df_t['Phone_Activation_date'])
    df_t.insert(1,'date_r',df_t['Return_RECEIVED_DT'])
    df_t = df_t.dropna(subset=['Phone_Activation_date'])
    df_t = df_t.dropna(subset=['Return_RECEIVED_DT'])    
    df_t['date_a'] = df_t['date_a'].map(lambda x:str(x))
    df_t['date_a'] = df_t['date_a'].map(lambda x:(x if len(x)<=10 else x[:11]))   
    df_t['date_r'] = df_t['date_r'].map(lambda x:str(x))
    df_t['date_r'] = df_t['date_r'].map(lambda x:(x if len(x)<=10 else x[:11]))
        

def filterCols(df, y, m):
    df_new = df[(df.year_A>y-1)&(df.year_A<y+1)&(df.month_a<m-1)&(df.month_a>m+1)]
    return df_new

if __name__ == '__main__':
    #文件路径
    fPath = r'E:\Phone_Data\Total LA Activation .csv'
    #读取原始数据文件
    df = pd.read_csv(fPath)
    #给定月份与年份list
    year_lst = getRangeData(2013,2018)
    month_lst = getRangeData(1,13)
    #得到所有的类型列表
    typeList = getTypeList(df)
    #根据类型列表返回不同型号的df list类型
    df_list = getDfByTypesWithList(df,typeList)
    #根据不同型号计算激活数量
    df_dic = getAllData(df_list, year_lst,month_lst,typeList)
    #保存文件到文件夹
    path = r'E:\Phone_Data\AllTypesAct' #保存文件的路径
    nameSub = '_actNum' #文件名后半部分
    saveCsvByType(df_dic, path, nameSub)

    
