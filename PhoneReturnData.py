# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 14:01:07 2017

@author: litr2
"""

#==============================================================================
# 计算手机返回的数据
#==============================================================================
import pandas as pd
import numpy as np
import datetime
import re

def delTime(x):
    if len(x['Return_RECEIVED_DT'])>10 :
        return x.replace(x['Return_RECEIVED_DT'],x[:(len(x)-9)])
     
# 得到范围数据
def getRangeData(start, end):
    lst = []
    for i in range(start,end):
        lst.append(i)
    return lst

#针对不同的年月统计数量
def getAllData(df, year_lst, month_lst):
    dt = {}
    for y in year_lst:
        for m in month_lst:
            # 筛选列中数据
            tmp =df[(df.year==y)&(df.month==m)]
            tsum = tmp.ReturnQty.sum()
            dt[str(y)+'-'+str(m)] = tsum
    return dt

def getAllData2(df, year_lst, month_lst):
    dt = {}
    for y in year_lst:
        for m in month_lst:
            # 筛选列中数据
            tmp =df[(df.year_ship==y)&(df.month_ship==m)]
            tsum = tmp.ReturnQty.sum()
            dt[str(y)+'-'+str(m)] = tsum
    return dt

#根据激活日期-返修日期计算返修数量(打标签)
#def returnNumLabel(year_lst_re,month_lst_re,year_lst_act,month_lst_act):
    
    


if __name__=='__main__':
    fPath = r'E:\Phone_Data\Return 1 --ML_LA_Return_date_with_Act.csv'
    df = pd.read_csv(fPath)
    #筛选出0N66的数据
    s_df = df[df.Return_apc_code=='0N66']
#    #重建索引
#    s_df.reindex(index=range(s_df.shape[0]))
    #加入新的index列
    #s_df['index'] = range(s_df.shape[0])
    
    #对日期时间列去除时间
#    s_df[['Return_RECEIVED_DT','Return_SHIP_DESPATCH_DT']].apply(delTime)
    
#    dstr = dstr.replace(dstr, dstr[:(len(dstr)-9)])

#插入复制列
    s_df.insert(1,'year',s_df['Return_RECEIVED_DT'])
    s_df.insert(2,'month',s_df['Return_RECEIVED_DT'])
    s_df.insert(3,'year_ship',s_df['Return_SHIP_DESPATCH_DT'])
    s_df.insert(4,'month_ship',s_df['Return_SHIP_DESPATCH_DT'])
    s_df.insert(5,'year_ac',s_df['Phone_Activation_date'])
    s_df.insert(6,'month_ac',s_df['Phone_Activation_date'])
    
    s_df.insert(7,'date_r',s_df['Return_RECEIVED_DT'])
    s_df.insert(8,'date_a',s_df['Phone_Activation_date'])
#截取字符串
    s_df['year'] = s_df['year'].map(lambda x:int(x[:4]))
    s_df['month'] = s_df['month'].map(lambda x:int(x[5:7]))
    s_df['year_ship'] = s_df['year_ship'].map(lambda x:int(x[:4]))
    s_df['month_ship'] = s_df['month_ship'].map(lambda x:int(x[5:7]))
    s_df['year_ac'] = s_df['year_ac'].map(lambda x:int(x[:4]))
    s_df['month_ac'] = s_df['month_ac'].map(lambda x:int(x[5:7]))
    
    #转换为统一日期格式：yyyy-mm-dd
    s_df['date_r'] = s_df['date_r'].map(lambda x:int(x if len(x)<=10 else x[:11]))
    s_df['date_a'] = s_df['date_a'].map(lambda x:int(x if len(x)<=10 else x[:11]))
    
    year_lst = getRangeData(2013,2018)
    month_lst = getRangeData(1,13)
    dic=getAllData(s_df,year_lst,month_lst)
    res = pd.DataFrame.from_dict(dic,orient='index')
    res.to_csv(r'E:\Phone_Data\Return_0N66_ActNumByMonthWihtShip.csv')
    
    
    