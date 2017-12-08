# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 14:41:40 2017

@author: litr2
"""

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
    dataChinese = re.sub("[\s+\.+\!\/_,$%^*(+\"\'\)\-+\:\;\>\<\`]+|[+——！，。？?、~@#￥%……&*（）]+|[A-Za-z0-9]+"," ",data)    
    return dataChinese

#---中文分词
def splitChineseData(data):
    seg_list = jieba.lcut(data)
    return seg_list 

#3.去除标点符号
def delSigna(data):
     afterData = re.sub("[\s+\.\!\/_,$%^*(+\"\'\)\-]+|[+——！，。？、~@#￥%……&*（）]+|[0-9]", " ",data)  
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

#-----去除list中的\n
def delSpaceN(lst):
    lst2 = []
    for l in range(len(lst)):
        lst[l] = lst[l].strip('\n')

#-----去除list中空格
def delSpace(lst):
    for l in range(len(lst)):
        lst[l] = lst[l].strip() 

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
    

#将结果转化为csv文件(word, frequency)
def file2Csv(data, savePath, saveName):
    csvData = pd.DataFrame(data,columns=['word','frequency'])
    csvData.to_csv(savePath+'\\'+saveName)

if __name__ == '__main__':
    
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

#==============================================================================
# add to azrue 
#==============================================================================
    df_data = pd.read_table(dataframe1)
    df_sw = pd.read_table(dataframe2)
    
#    2.pd转换为stirng
    string_data = df_data.to_string(header=None, index=None)
    #转为小写
    string_data_l = string_data.lower()
    
    string_sw = df_sw.to_string(header=None, index=None)
    list_sw = string_sw.split('\n')
#    2.1 去除其他符号
    afterData = delSigna(string_data_l)
#    3.使用ntlk切分英文单词（主要希望通过nltk去掉标点）
    afterData_split = nltk.tokenize.word_tokenize(afterData)
#    4.去除停用词
    afterData = delStopWords2(afterData_split, string_sw)
#    4.得到的list转为pd输出
    df_afterData = pd.DataFrame(afterData)
