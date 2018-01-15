# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 14:01:56 2017

@author: litr2
"""

# =============================================================================
# 打算做一个特征筛选的函数或者库
# 可以实现的功能如下：
# 1.读取所有数据
# 2.对所有数据读取其所有特征
# 3.计算出所有特征的排列组合
# 4.对给定算法计算所有特征组合的得分并进行评价
# 5.输出当前数据最好的特征和对应预测值，以及对应的测试函数（可选）
# 6.待补
# =============================================================================

import pandas as pd
import numpy as np 
import os
from itertools import combinations
from sklearn.linear_model import BayesianRidge
import re
from sklearn.cross_validation import KFold#过时？
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import cross_val_score#评分
from sklearn.model_selection import cross_val_predict#预测
# 1.读取所有数据
# 1.1 获得所有文件名列表，返回文件名列表
def getFileList2(path):
    lst = os.listdir(path)
    return lst

# 1.2 通过文件列表和文件名获取对应df 返回df_list(返修数修改)
def getDfList(path, file_lst):
    df_lst = [] # 根据路径与文件名列表返回对应的df_list
    for f in file_lst:
        tmp = pd.read_csv(path+'\\'+f)
        tmp.drop(0,axis=0,inplace=True)
        df_lst.append(tmp)
    return df_lst

# 2.对所有数据读取其特征
# 2.1 获得一个df的特征列表的所有组合
def getAllFeatureDictWithSingleDf(df):
    f_lst = np.array(df.columns).tolist()
    del f_lst[0]
    # 计算所有特征的组合
    dic = {}
    for l in range(len(f_lst)):
        dic[l+1] = list(combinations(f_lst,l+1))
    return dic

# 2.1 获得一个df的特征列表的所有组合
def getAllFeatureListWithSingleDf(df):
    f_lst = np.array(df.columns).tolist()
    del f_lst[0]
    # 计算所有特征的组合
    f_a_lst = []
    for l in range(len(f_lst)):
        f_a_lst.append(list(combinations(f_lst,l+1)))
    return f_a_lst

# 去除字符串中的逗号并使str变为float类型
def dfDelComma6(df): 
    for col in df.select_dtypes([np.object]).columns[1:]:
        df[col] = df[col].str.replace(',','').astype('float64')

# 得到df训练测试集与预测参数
def getAllDataWithoutLast(df):
    df_train_test = df.copy().iloc[:-1]
    df_pre = df.iloc[-1]
    return df_train_test,df_pre

# 得到标签与数据集
def splitDf(df):
    y = df[df.columns[:1]]
    X = df[df.columns[1:]]
    return X,y  

# 将数据分为预测集训练集
def getTrainTestSet(df_train_test):
    y = df_train_test[df_train_test.columns[:1]]
    X = df_train_test[df_train_test.columns[1:]]
    X_train,X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=0)
    return X_train,X_test, y_train, y_test

# 删除PC NAN 值与根据对应的col_lst筛选出数据(输入为df_pre的series，和col_lst的tuple)
def formatPredcitedData(df_pre,col_lst):
#    X_pre = df_pre.drop('PC ')
    # series 多列索引需要list
    tmp_l = list(col_lst)
    X_pre = df_pre[tmp_l]
    X_pre = X_pre.values.reshape(1,X_pre.shape[0])
    return X_pre

# column_names获得与处理
def handleColNames(df):
    column_names_all = np.array(df.columns).tolist()
    column_names =column_names_all[1:]
    return column_names,column_names_all

# 把PC 列与特征列合并
def concatLabel(df_train_test,df_label):
    df_train_test = pd.concat([df_label,df_train_test],axis=1,join_axes=[df_train_test.index])
    return df_train_test

# 2.2 对特征组合列表进行运算，给出对应分值，并选出最好的
def getBestResultsWithSingleDf(df,all_feature_lst,sklearn_algorithm=None):
    if sklearn_algorithm == None:
        reg = BayesianRidge() # 默认使用贝叶斯岭回归
    else:
        reg = sklearn_algorithm
    # 1 对dic中的每一个特征组合做运算（交叉验证）
    # 1 对list中的每一个特征组合做运算（交叉验证）
    # 1 可以使用grid search 和pipline
        # 1.1 取除最后一行以外的所有数据 
    #     数据表原始格式应为最后一行除‘PC’数据以外其他均有数据的格式
    # 1.2 分成训练集测试集样本
    # 1.3 交叉验证
    print('您没有给定函数，默认选择的sklearn的贝叶斯岭回归')
    # 2 对模型进行评估（R2,MSE）
    rmse_score_lst = [] #split的测试集得分list
    pre_lst = [] # 预测值list
    acc_score_lst = [] #精准率的list
    r2_lst = [] #r2的list
    feature_lst = []
    all_lst = []
    df_label = df[['PC ']]
    for lists in lst:
        for l in lists:
            tmp = list(l)
            df_train_test,df_pre = getAllDataWithoutLast(df[tmp])
            df_train_test = concatLabel(df_train_test,df_label)
            X_train,X_test, y_train, y_test = getTrainTestSet(df_train_test)
            X_pre = formatPredcitedData(df_pre,l)
            reg.fit(X_train,y_train.values.ravel())
            r2 = reg.score(X_test,y_test)
            true_pre = reg.predict(X_pre)
            r2_lst.append(r2)
            pre_lst.append(true_pre)
            feature_lst.append(l)
            all_lst.append((r2,true_pre,(l)))
    return all_lst,r2_lst,pre_lst,feature_lst            

#转为DataFrame并按照r2排序
def sortByR2AndSave(all_lst,savePath,saveName):
    results = pd.DataFrame(all_lst,columns=['r2','predict_value','features'])
    results = results.sort_values(by='r2',ascending=False,inplace=True)
    results.to_csv(savePath +'\\'+ saveName +'.csv')


if __name__ == '__main__':
#    以下为测试使用
    #读取数据
    path = r'E:\TestData\2017Q4CHINA.csv'
    df = pd.read_csv(path)
    #df中年份作为索引列
#    df.set_index(df.columns[:1], inplace=True)
    df.set_index('Quarter', inplace=True)
    
    #df中字符串处理
    dfDelComma6(df)
    #df分成预测数据与训练数据
    df_train_test,df_pre = splitDf(df)
    #
    for lists in f_a_lst:
        for l in lists:
            l = list(l)
    
     for lists in f_a_lst:
        for l in lists:
            tmp = list(l)
            df_train_test,df_pre = getAllDataWithoutLast(df[tmp])
            df_train_test = concatLabel(df_train_test,df_label)
            X_train,X_test, y_train, y_test = getTrainTestSet(df_train_test)
            X_pre = formatPredcitedData(df_pre,l)
            reg.fit(X_train,y_train)
            r2 = reg.score(X_test,y_test)
            true_pre = reg.predict(X_pre)
            r2_lst.append(r2)
            pre_lst.append(true_pre)
            feature_lst.append(l)
            all_lst.append((r2,true_pre,(l)))        
# =============================================================================
