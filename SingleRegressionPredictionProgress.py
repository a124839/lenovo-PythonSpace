# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 14:29:33 2017

@author: litr2
"""

# =============================================================================
# 单次执行回归过程
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

# 去除字符串中的逗号并使str变为float类型 
def dfDelComma(df): 
    for col in df.select_dtypes([np.object]).columns[1:]:
        df[col] = df[col].str.replace(',','').astype('float64')

# 季度作为索引
def setIndex(df):
    df.set_index('Quarter', inplace=True)

# 得到df训练测试集与预测参数
def getAllDataWithoutLast(df):
    df_train_test = df.copy().iloc[:-1]
    df_pre = df.iloc[-1] #最后一行为需要预测的值的参数
    return df_train_test,df_pre

# 得到标签与数据集
def splitDf(df):
    y = df[df.columns[:1]]
    X = df[df.columns[1:]]
    return X,y    
  
# 将数据分为预测集训练集
def getTrainTestSet(df_train_test):
    y = df_train_test[df.columns[:1]]
    X = df_train_test[df.columns[1:]]
    X_train,X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=0)
    return X_train,X_test, y_train, y_test

# 删除PC NAN 值
def formatPredcitedData(df_pre):
    X_pre = df_pre.drop('PC ')
    X_pre.values.reshape(1,X_pre.shape[0])
    return X_pre
    
# 训练模型
def modelTrainFit(X_train,X_test, y_train, y_test,X_pre,model=None):
    if model == None:
        model = BayesianRidge()
    model.fit(X_train,y_train)
    pre_cv = model.predict(X_test)
    score = model.score(X_test,y_test)
    true_pre = model.predict(X_pre)
    lst = []
    lst.append((pre_cv,score,true_pre))
    return lst
    
if __name__ == '__main__':
    path = r''
    df = pd.read_csv(path)
    
    