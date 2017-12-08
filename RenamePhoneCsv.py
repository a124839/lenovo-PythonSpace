# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 15:20:00 2017

@author: litr2
"""

#==============================================================================
#用来对phone文件进行二次处理
#包括添加header等 
#==============================================================================
import pandas as pd
import numpy as np

import os  

def act_header(df):
    df.columns = ['month','total_activation']

def ship_header(df):
    df.columns = ['month','total_shipment']

def return_header(df):
    try:
        df.columns = ['month','return_qty']
    except:
        print(type(df))

def getFileList2(path):
    lst = os.listdir(path)
    return lst

#通过文件列表获取对应df 返回list(返修数修改)
def getDfList(path, file_lst):
    df_lst = [] 
    for f in file_lst:
#        tmp = pd.read_csv(path+'\\'+f)
#        tmp.drop(0,inplace=True)
        tmp = pd.read_csv(path+'\\'+f)
        tmp.drop(0,axis=0,inplace=True)
        df_lst.append(tmp)
    return df_lst

def getDfList2(path, file_lst):
    df_lst = [] 
    for f in file_lst:

        tmp = pd.read_csv(path+'\\'+f)
#        tmp.drop(0,axis=0,inplace=True)
        df_lst.append(tmp)
    return df_lst

#对每个df进行列重命名
def header_all_return(df_lst):
    for d in range(len(df_lst)):
#        act_header(d)
#        ship_header(d)
        return_header(df_lst[d])
    
def header_all_act(df_lst):
    for d in range(len(df_lst)):
        act_header(df_lst[d])
#        ship_header(d)
#        return_header(df_lst[d])
#
#保存新的文件夹
def saveNew(df_lst, savePath, saveNameSub, file_lst):
    for d in range(len(df_lst)):
        df_lst[d].to_csv(path_or_buf=savePath+'\\'+file_lst[d][:5]+saveNameSub+'.csv',index=None)

if __name__ == '__main__':
    filePath = r'E:\Phone_Data\AllTypesReturnFrom'
    file_lst = getFileList2(filePath)
    df_lst = getDfList(filePath,file_lst)
#    header_all(df_lst)
    header_all_act(df_lst)
    savePath = r'E:\Phone_Data\AllTypesAct'
    nameSub = '_actNum'
    saveNew(df_lst,savePath,nameSub,file_lst)
    
