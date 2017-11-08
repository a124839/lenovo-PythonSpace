# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:52:25 2017

@author: litr2
"""

#==============================================================================
#分词与处理停用词 
#==============================================================================

from nltk.corpus import stopwords
import nltk
import re
import collections
 

#1.读取文件
def getTxt(filePath):
    f = open(filePath)
    data = f.read()
    data = data.lower()#转小写
    return data

#2.分词
def getDataAfterSplit(data):
    data1 = data.split(" ")
    return data1

#3.去除标点符号
def delSigna(data):
    dataNoSig = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+|[A-Za-z0-9]+","",data)
    #去掉中英文符号
    return data

#2,3---标点符号也分出来
def getDataUsingNltk(data):
    data2 = nltk.tokenize.word_tokenize(data)
    return data2

#2,3.1---使用其他停用词词表
def getOtherStopWords(filePath):
    f = open(filePath)
    sw = f.read().split("\n")
    return sw

#4.去掉停用词
def delStopWords(data):
    wordEngStop = nltk.corpus.stopwords.words('english')
    lst = []
    for d in data:
        if not d in wordEngStop:
            lst.append(d)
    return lst    
#--使用其他停用词词表去除停用词
def delStopWords2(data,sw):   
    lst2 = []
    for d in data:
        if not d in sw:
            lst2.append(d)
    return lst2 

#--去除标点符号
def delSingal(data, lst):
    lstRes = []
    for d in data :
        if not d in lst:
            lstRes.append(d)
    return lstRes
            
#5，词频统计
def sort_count(data):
    res = collections.OrderedDict(sorted(data.items(), key = lambda t:-t[1]))
    return res

#---词频统计2
def sort_count2(data):
    count_dict={}
    for str in data:
        if str in count_dict.keys():
            count_dict[str] = count_dict[str]+1
        else:
            count_dict[str] = 1
    count_list = sorted(count_dict.items(), key=lambda x:x[1], reverse=True)
    return count_list    
    
def wordcount(str):
    # 文章字符串前期处理
    strl_ist = str.replace('\n', '').lower().split(' ')
    count_dict = {}
    # 如果字典里有该单词则加1，否则添加入字典
    for str in strl_ist:
        if str in count_dict.keys():
            count_dict[str] = count_dict[str] + 1
        else:
            count_dict[str] = 1
    #按照词频从高到低排列
    count_list=sorted(count_dict.iteritems(),key=lambda x:x[1],reverse=True)
    return count_list

if __name__ == '__main__':
#    源文件路径
    sFile = r'E:\TestData\test.txt'
#    停用词路径
    stopWordFile = r'E:\TestData\stop_words_eng.txt'
#    标点符号列表
    lst = [',','.','"','!']
    sourceData = getTxt(sFile)
    splitData = getDataUsingNltk(sourceData)
    sw = getOtherStopWords(stopWordFile)
    withoutSWData = delStopWords2(splitData, sw)
    afterData = delSingal(withoutSWData, lst)
    resList = sort_count2(afterData)
    print(resList)
