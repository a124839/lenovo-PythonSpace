# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# imports up here can be used to 
import pandas as pd
import re
import numpy as np
#画图使用
import matplotlib.plotly as plt


# 分词
def getDataAfterSplit(data):
    data1 = data.split(" ")
    return data1

# 去除标点符号与英文
def delSignaForCN(data):
    dataNoSig = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+|[A-Za-z0-9]+"," ",data)
    return dataNoSig
    
#去除所有符号    
def delSignaForENG(data):
     afterData = re.sub("[\s+\.+\!\/_,$%^*(+\"\'\)\-\;]+|[+——！，。？、~@#￥%……&*（）]+", " ",data)  
     return afterData

#-----去除list中的\n
def delSpaceN(lst):
    for l in range(len(lst)):
        lst[l] = lst[l].strip('\n')

#-----去除list中空格
def delSpace(lst):
    for l in range(len(lst)):
        lst[l] = lst[l].strip() 


#2,3.1---使用其他停用词词表
def getOtherStopWords(filePath):
    f = open(filePath)
    sw = f.read().split("\n")
    return sw 
    
#--使用其他停用词词表去除停用词，sw为stirng类型
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
            
#---词频统计2，并按照从大到小排序
def sort_count2(data):
    count_dict={}
    for str in data:
        if str in count_dict.keys():
            count_dict[str] = count_dict[str]+1
        else:
            count_dict[str] = 1
    count_list = sorted(count_dict.items(), key=lambda x:x[1], reverse=True)
    return count_list    
    
#-- 去除空对象
def delNull2(lst):
    lst2 = []
    for o in range(len(lst)):
#        if lst[o] == None | lst[o] == '':
        if lst[o] == '':
            o = o+1
        elif lst[o] == ' ':
            o = o+1
        else:
            lst2.append(lst[o])
    return lst2
   
def plotFig(df):
    labels = df[0]
    values = df[1]
    trace = go.Pie(labels=labels, values=values)
    py.iplot([trace], filename='basic_pie_chart')
    
# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame
def azureml_main(dataframe1 = None, dataframe2 = None):

    # Execution logic goes here
    print('Input pandas.DataFrame #1:\r\n\r\n{0}'.format(dataframe1))
    #1. 得到df数据，df1为需要统计的文档，df2为停用词表
    df_data = dataframe1
    df_sw = dataframe2
    #2. 统计文档df1转换为stirng
    string_data = df_data.to_string(header=None, index=None)
    #3. 统计的文档所有词转为小写
    string_data_l = string_data.lower()
    #4. 停用词表df2转为string
    string_sw = df_sw.to_string(header=None, index=None)
#    list_sw = string_sw.split('\n')
    #5. 去除与单词无关的其他符号
    afterData = delSignaForENG(string_data_l)
    #6.使用ntlk切分英文单词（主要希望通过nltk去掉标点）
    #afterData_split = nltk.tokenize.word_tokenize(afterData)
    #6.1 直接split分词
    afterData_split = afterData.split(" ")
    #6.2 去除空值
    ad_split = delNull2(afterData_split)
    #7. 去除停用词
    after_data = delStopWords2(ad_split, string_sw)
    #8.对处理后的数据进行统计并按照从高到低排序
    res = sort_count2(after_data)
    #9. 得到的list转为pd输出
    df_afterData = pd.DataFrame(res)
    # If a zip file is connected to the third input port is connected,
    # it is unzipped under ".\Script Bundle". This directory is added
    # to sys.path. Therefore, if your zip file contains a Python file
    # mymodule.py you can import it using:
    # import mymodule
    
    # Return value must be of a sequence of pandas.DataFrame
    return df_afterData
if __name__ == '__main__':
    sFile = r'E:\TestData\CXSurvey.csv'
    sswFile = r'E:\TestData\newSWENG.csv'
    df_data = pd.read_csv(sFile, sep='"', header=None)
    df_sw = pd.read_csv(sswFile, header=None)
    res = azureml_main(df_data, df_sw)