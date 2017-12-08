# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 10:36:03 2017

@author: litr2
"""
#==============================================================================
# 处理数据na值
#==============================================================================
import numpy as np
import pandas as pd

inputFile = r''
data_Files = pd.read_csv(inputFile)
data_Files = data_Files.dropna(axis=1)
