#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 09:26:01 2023

@author: nnedi
"""

import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt

from a21_data_analytics import *
from a22_descriptive_stats import *

    

def filter_df(df, bool_series):
    '''which expects a parameter df, which is a pandas.DataFrame and bool_series, which is a 
    pandas. Series with the same index as df, that contains boolean values (True or False)'''
    
    #returns the dataseries
    return df[bool_series]



def histogram_function():
    ''' plots a histogram of the TO and AST columns '''
      
    #makes a new dataset the same as the original dataset
    df1 = df
    
    #filters out everybody's regular season stats
    df1 = filter_df(df1, df1['SZN'] == 'Post')
    
    #drops all of the columns except for turnovers and assists
    df1.drop(columns = ['PTS', 'REB', 'FG%', '3PT%', 'FT%', 'MIN', 'AST/TO'], axis=1, inplace=True)
    
    #calling plt.subplots, initializing it with the amount of rows and columns from df1
    fig, axes = plt.subplots(1, 2)
    
    #creates the first histogram with the data from the column 'TO'
    df1.hist('TO', ax=axes[0])
    
    #creates the second histogram with the data from the column 'AST'
    df1.hist('AST', ax=axes[1])
    
    #sets the title of the first histogram
    axes[0].set_title('Hist. of Postseason TO')
    
    #labels the x-axis for the first histogram
    axes[0].set_xlabel('TO')
    
    #labels the y-axis for the first histogram
    axes[0].set_ylabel('Frequency')
    
    #labels the title for the second histogram
    axes[1].set_title('Hist.  of Postseason AST')
    
    #labels the x for the second histogram
    axes[1].set_xlabel('AST')
    
    #labels the y for the second histogram
    axes[1].set_ylabel('Frequency')
    
    #shows the histograms
    plt.show()



def reg_vs_post():
    '''puts regular season stats and postszn stats in two dataframes & does descriptive stats'''
    
    #labeling what part of the season the stats are from
    print('Regular Season Averages')
    
    #filters out postseason stats and puts it into a new dataframe
    df_reg = filter_df(df, df['SZN'] != 'Post')
    
    #computes descriptive statistics on the dataframe
    print(df_reg.describe())
    
    #prints two gaps
    print()
    print()
    
    #labeling what part of the season the stats are from
    print('Posteason Averages')
    
    #filters out  regular season stats and puts it into a new dataframe
    df_post = filter_df(df, df['SZN'] == 'Post')
    
    #computes descriptive statistics on the dataframe
    print(df_post.describe())



def playoff_scoring():
    '''gets the scoring mean of the player's PPG in the playoffs, not counting Harden''' 

    #filters out James Harden from the dataframe and puts everything else into a new dataframe
    new_df = filter_df(df, df['Name'] != 'James Harden')
    
    #filters out everybody's regular season stats
    new_df = filter_df(new_df, new_df['SZN'] == 'Post')
    
    #prints the mean pts of the players in the postseason, not counting Harden
    print(new_df['PTS'].mean())

    #filters out evverybody but James Harden from the dataframe it into a new dataframe
    new_df2 = filter_df(df, df['Name'] == 'James Harden')
     
    #filters out Harden's regular season stats
    new_df2 = filter_df(new_df2, new_df2['SZN'] == 'Post')
     
    #prints the average points Harden scores in the postseason
    print(new_df2['PTS'].mean())  



def harden_kawhi_post():
    '''plots harden and kawhi average pts, to, ast, reb, min, ast/to% in the playoffs'''
    
    #makes a new dataframe and sets it the same as the df with all of the stats
    df_new = df
    
    #drops the columns that hold percentages
    df_new.drop(columns=['FT%', 'FG%', '3PT%'], axis=1,inplace=True)
    
    #plots harden's postseason averages against kawhi's
    df_new[df_new['SZN'] == 'Post'].iloc[[0, 3]].plot.bar()
    
    

def harden_russ_post():
    '''plots harden and russ average FG%, 3PT%, FT% in the playoffs'''
    
    #makes a new dataframe and sets it the same as the df with all of the stats
    df_new = df
    
    #drops the columns that hold percentages
    df_new.drop(columns=['PTS', 'TO', 'AST', 'REB', 'MIN', 'AST/TO'], axis=1,inplace=True)
    
    #plots harden's postseason averages against kawhi's
    df_new[df_new['SZN'] == 'Post'].iloc[[0, 5]].plot.bar()
    
    

def ast_tov_ratio():
    '''calculates each player's assist to turnover ratio and adds it into the dataframe in a new column'''
    
    # #creates a new DataSeries with the same index as df
    # df_new = pd.DataFrame()
    
    # #makes the new dataframe the same as the original one
    # df_new = df
        
    # #calculates each players ast-to-tov ratio and adds in into the dataframe
    # df_new['AST/TO'] = df_new['AST'] / df_new['TO']
    
    # #prints the new dataframe
    # print(df_new)
    
        
    #calculates each players ast-to-tov ratio and adds in into the dataframe
    df['AST/TO'] = df['AST'] / df['TO']
    
    #prints the dataframe
    print(df)
    
    

def ast_tov_boxplot():   
    '''creates a labeled boxplot of the ast/tov column'''
    
    #labels the title
    plt.title('Box Plot for AST/TO')
    
    #labels the y label
    plt.ylabel('2AST/TO Ratio')
    
    #creates the boxplot
    df['AST/TO'].plot(kind='box')
    
    
    
def multi_variable_regression(df, independent1, independent2, dependent):
    '''performs an OLS regression of the column identified by dependent as a function of 
    the columns identified by independent'''

    #assigns the x variables
    X = df[[independent1, independent2]]
        
    #assigns the y variable
    Y= df[dependent]

    #run the OLS regression model
    model = sm.OLS(Y, X).fit()
        
    #prints the model's data table
    print(model.summary())



if __name__ == '__main__':
    
    #attaches the file's name to a variable
    filename = 'averages.csv'

    # reads the data
    df = pd.read_csv(filename)
    #sets up the index
    df.index = df[['Name', 'SZN']]
    
    #playoff_stats()
    
    ast_tov_ratio()
    
    print()
    
    multi_variable_regression(df, '3PT%', 'FG%', 'PTS')
    
    print()
    
    reg_vs_post()
    
    print()
    
    playoff_scoring()
    
    print()
    
    histogram_function()
    
    ast_tov_boxplot()