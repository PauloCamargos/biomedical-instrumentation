#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 22:16:47 2018

@author: camargos
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import Imputer # for missing data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder # for encoding
from sklearn.model_selection import train_test_split # for training and test
from sklearn.preprocessing import StandardScaler # for feature scaling

dataset = pd.read_csv("../Data.csv")

# Creating the matrix of features (independent)
x = dataset.iloc[:,:-1].values  # gets all the columns excpt last, return values
# dependent
y = dataset.iloc[:,-1].values

# SPLITING THE DATA BET. TRAINING AND TEST SET
# 2 on test, 8 on training
x_train, x_test, y_train_, y_test = train_test_split(x,y, test_size=0.2,
                                                       random_state = 0)

# FEATURE SCALING
"""sc_x = StandardScaler()
x_train = sc_x.fit_transform(x_train)
x_test = sc_x.transform(x_test)"""

