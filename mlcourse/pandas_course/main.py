#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 11:22:25 2018

@author: camargos
"""

import pandas as pd

# Creating a dataframe from file
df = pd.read_csv("data/weather_data.csv")

# Creating from dictionary
weather_data = {
    'day': ['1/1/2017','1/2/2017','1/3/2017','1/4/2017','1/5/2017','1/6/2017'],
    'temperature': [32,35,28,24,32,31],
    'windspeed': [6,7,2,7,4,2],
    'event': ['Rain', 'Sunny', 'Snow','Snow','Rain', 'Sunny']
}
df = pd.DataFrame(weather_data)

# Number of row andcol
row, col = df.shape

# printing the 2 firts row
df.head(2)
# printing the last 2
df.tail(2)

# slicding
df[2:5]

# printing the columns
df.columns

# printing the days data
df.day # or
df['day']
df[['event', 'day']]

df.temperature.max()
df.temperature.mean()
df.temperature.min()
df.temperature.std()

# print statistic info
df.describe()

# selecting with conditions
df[df.temperature>32]
df[df.temperature==df.temperature.max()]
df[['day', 'temperature']][df.temperature==df.temperature.max()]
# If the column name has spaces, use the other sintax

# setting the index
df.index # the acttual dataframe
df.set_index('day')     # returns anotther dataframe
df.set_index('day', inplace=True)     # modify the original

# searching for data as index
df.reset_index(inplace=True)
df.set_index('event',inplace=True)
df.loc['Rain']
df.reset_index(inplace=True)
df


###### ways to create dataframe

# READING FROM .csv
df = pd.read_csv("data/weather_data.csv")
# from xls
df = pd.read_excel("data/weather_data.xlsx")
# from dictionary
weather_data = {
    'day': ['1/1/2017','1/2/2017','1/3/2017','1/4/2017','1/5/2017','1/6/2017'],
    'temperature': [32,35,28,24,32,31],
    'windspeed': [6,7,2,7,4,2],
    'event': ['Rain', 'Sunny', 'Snow','Snow','Rain', 'Sunny']
}
df = pd.DataFrame(weather_data)
# using tuple
weather_data = [
    ('1/1/2017',32,6,'Rain'),
    ('1/2/2017',35,7,'Sunny'),
    ('1/3/2017',28,2,'Snow')
]
df = pd.DataFrame(data=weather_data, columns=['day','temperature','windspeed','event'])
df

# Reading and writng files csv
df = pd.read_csv("data/stock_data.csv")
# skiping row
df = pd.read_csv("data/stock_data.csv", skiprows=1)
#or
df = pd.read_csv("data/stock_data.csv", header=1) # header index starts at 0

# seting the header
df = pd.read_csv("data/stock_data.csv", header=0, names=['tiker','eps',
                                                            'revenue','price','people']) # header index starts at 0

# specify the n of row
df = pd.read_csv('data/stock_data.csv',nrows=3)
df

# changing to nan
df = pd.read_csv('data/stock_data.csv',na_values=['not available', 'n.a.'])
df
# with dict

df = pd.read_csv("stock_data.csv",  na_values={
        'eps': ['not available'],
        'revenue': [-1],
        'people': ['not available','n.a.']
    })
df

# WRITING TO CSV
df.to_csv('data/generated_csv.csv',index=False, columns=['tickers', 'eps'])
# without header
df.to_csv('data/generated_csv.csv',header=False)
