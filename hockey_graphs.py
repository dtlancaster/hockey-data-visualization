# -*- coding: utf-8 -*-
"""
Created on Wed May  5 12:52:55 2021

@author: Dylan Lancaster
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

forward_df = pd.read_csv('forward_data.csv')
forward_df = pd.DataFrame(forward_df)
defense_df = pd.read_csv('defense_data.csv')
defense_df = pd.DataFrame(defense_df)
goalie_df = pd.read_csv('goaltender_data.csv')
goalie_df = pd.DataFrame(goalie_df)

"""
Function creating a line plot showing the correlation between average time on ice
and the absolute value of a forward's plus-minus stat.
"""

def forward_toi_points(df):
    df['TOI'] = pd.to_datetime(df['TOI'], format="%M:%S")
    #df['+/-'] = df['+/-'].abs()
    df = df.groupby(df['TOI'].dt.strftime('%M:%S'))['P'].mean()
    df = df.reset_index()
    print(df)
    df.plot(kind='line', x='TOI', y='P', linewidth=1, color='red', legend=False)
    plt.title('Correlation between TOI and Points Earned by Forward Players')
    plt.xlabel('Average Time on Ice (min/sec)')
    plt.ylabel('Average Number of Points')
    plt.show()

"""
Function creating a scatter plot showing the correlation between total number of hits
and total number of penalty minutes committed by a defensive player, featuring a line of best fit.
"""

def defense_hits_pim(df):
    df = df.groupby('Hits')['PIM'].mean()
    df = df.reset_index()
    print(df)
    df.plot(kind='scatter', x='Hits', y='PIM', linewidth=1, color='mediumblue', legend=False)
    plt.title('Correlation between Hits and PIM Earned by Defensemen')
    plt.xlabel('Number of Legal Hits')
    plt.ylabel('Average Penalty Minutes')
    plt.plot(np.unique(df['Hits']), np.poly1d(np.polyfit(df['Hits'], df['PIM'], 1))(np.unique(df['Hits'])))
    plt.show()

"""
Function creating a scatter plot showing the correlation between a goaltender's age 
and his save percentage, featuring a line of best fit.
"""

def goalie_age_svpctg(df):
    df = df.groupby('Age')['SV%'].mean()
    df = df.reset_index()
    print(df)
    df.plot(kind='scatter', x='Age', y='SV%', linewidth=1, color='green', legend=False)
    plt.title('Correlation between Age and SV% of Goaltenders')
    plt.xlabel('Age in Years')
    plt.ylabel('Average Save Percentage')
    plt.plot(np.unique(df['Age']), np.poly1d(np.polyfit(df['Age'], df['SV%'], 1))(np.unique(df['Age'])))
    plt.show()

forward_toi_points(forward_df)
defense_hits_pim(defense_df)
goalie_age_svpctg(goalie_df)