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
import pandas as pd
import jieba 

#1.读取文件
def getTxt(filePath):
    f = open(filePath,encoding='UTF-8')
    data = f.read()
    data = data.lower()#转小写
    return data

#得到中文
def getChinese(data):
    dataChinese = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+|[A-Za-z0-9]+"," ",data)    
    return dataChinese

#2.分词
#2.1英文‘分词’
def getDataAfterSplit(data):
    data1 = data.split(" ")
    return data1
#2.2中文分词
def splitChineseData(data):
    seg_list = jieba.lcut(data)
    return seg_list 
#3.去除标点符号



def delSigna(data):
     afterData = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", " ",data)  
     return afterData
#针对特定数据 特别的去除一些符号
def spReg(data):
    afterdata = re.sub("[\-\)\;\<\[\]\|\:\>\`\=\,\s+]", "", data)
    return afterdata
 
#2,3---标点符号也分出来
def getDataUsingNltk(data):
    data2 = nltk.tokenize.word_tokenize(data)
    return data2

#2,3.1---使用其他停用词词表
def getOtherStopWords(filePath):
    f = open(filePath, encoding='UTF-8')
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

#将结果转化为csv文件(word, frequency)
def file2Csv(data, savePath, saveName):
    csvData = pd.DataFrame(data,columns=['word','frequency'])
    csvData.to_csv(savePath+'\\'+saveName)

if __name__ == '__main__':
#    源文件路径
    sFile = r'E:\TestData\CX Survey.txt'
#    停用词路径
    stopWordFile = r'E:\TestData\stop_words_eng.txt'
#    标点符号列表

    lst = [',','.','"','!']
    #读取数据
    sourceData = getTxt(sFile)
    #得到分词数据
    splitData = getDataUsingNltk(sourceData)
    #得到停止词库
    sw = getOtherStopWords(stopWordFile)
    #对分词的数据剔除停用词
    withoutSWData = delStopWords2(splitData, sw)
    #去除自定义标点符号
    afterData = delSingal(withoutSWData, lst)
    #统计词频
    resList = sort_count2(afterData)
    
#    中文词频统计
    sFile2 = r'E:\TestData\CX Survey10.17.17.txt'
    #中文停用词路径
    stopWordFile_cn = r'E:\TestData\stop_words_zh.txt'
    #得到原始数据
    sourceData2 = getTxt(sFile2)
    #得到中文数据
    splitData_cn = getChinese(sourceData2)
    #去除标点符号
    afterData_cn = delSigna(splitData_cn)
    afterData_cn = spReg(afterData_cn)
    #中文分词
    scd = splitChineseData(afterData_cn)
    #去除停用词
        #读取中文停用词
    sw_cn = getOtherStopWords(stopWordFile_cn)
    withoutSWData_cn = delStopWords2(scd, sw_cn)   
    #词频统计
    resList_cn = sort_count2(withoutSWData_cn)
    #列表转换为csv
    file2Csv(resList_cn, r'E:\TestData', 'CN_wordCount.csv')
    
    print(resList)
