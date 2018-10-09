# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 00:00:17 2018

@author: Jochen Binder
"""

# Load packages
import os as os
import pandas as pd
import numpy as np
import Raking as Rake

# Set working directory for the session
os.chdir('C:/Users/Jochen Binder/Desktop/Data_Weighting')
# Read in the df from filepath
#df = pd.read_table('K1.csv', sep='\t', decimal='.', encoding='utf8', na_values=[' '])
#df = pd.read_table('K1.csv', sep=';', decimal=',', encoding='latin1', na_values=[' '])
df = pd.read_table('rnk09353472l9c2_181008_065357.txt', sep=',', decimal='.', encoding='latin1', na_values=[' '])
#df = pd.read_table('Test.csv', sep=';', decimal='.', encoding='utf-8', na_values=['#NULL!'])
#df['total'] = 1

df['total'] = df['QWGT0']
#df['total'] = 1

#df = pd.read_table('rnk09353472l9c2_181007_210333.txt', sep=',', decimal='.', encoding='latin1', na_values=[' '])
#df['total'] = 1


# =============================================================================

df_total = df[((df.status == 'C') | (df.status == 'T')| (df.status == 'Q')) & df.QFSAMP == 1].copy()
df_complete = df[(df.status == 'C')].copy()

#df_total['total'] = len(df_complete)/len(df_total)
df_total['total'] = df_complete.total.sum()/df_total.total.sum()

# =============================================================================

i = 'QAGEGEN'

# Mortgage
aggm = df_total[df_total['Q3']!=4].groupby([i])['total'].sum()
t = len(df_complete[df_complete['QVERTICAL']==2])/aggm.sum().copy()
#t = df_complete[df_complete['QVERTICAL']==2]['total'].sum()/aggm.sum().copy()
aggm = aggm*t

data = df_complete[df_complete['QVERTICAL']==2].copy()
data['total'] = 1

ipfn_k = Rake.ipfn(data, [aggm],
               [[i]], 'total')

df_m = ipfn_k.iteration()
df_m = ipfn_k.weighting()

df_m.weight.sum()
df_m.weight.unique()
df_m.groupby([i])['weight'].sum()

# Car Insurance
aggm = df_total[df_total['Q4']==1].groupby([i])['total'].sum()
t = len(df_complete[df_complete['QVERTICAL']==1])/aggm.sum().copy()
aggm = aggm*t

data = df_complete[df_complete['QVERTICAL']==1].copy()
data['total'] = 1

ipfn_k = Rake.ipfn(data, [aggm],
               [[i]], 'total')

df_c = ipfn_k.iteration()
df_c = ipfn_k.weighting()

df_c.weight.sum()
df_c.weight.unique()
df_c.groupby([i])['weight'].sum()

# Personal Loan
aggm = df_total[df_total['Q5']!=4].groupby([i])['total'].sum()
t = len(df_complete[df_complete['QVERTICAL']==3])/aggm.sum().copy()
aggm = aggm*t

data = df_complete[df_complete['QVERTICAL']==3].copy()
data['total'] = 1

ipfn_k = Rake.ipfn(data, [aggm],
               [[i]], 'total')

df_l = ipfn_k.iteration()
df_l = ipfn_k.weighting()

df_l.weight.sum()
df_l.weight.unique()
df_l.groupby([i])['weight'].sum()

frames = [df_m, df_c, df_l]
df_weighted = pd.concat(frames)

# =============================================================================

#df_weighted.to_csv('weighted_df.csv')
df_weighted.to_csv('weighted_df_commadec.csv', sep=";", decimal=".")
#df_weighted.to_csv('weighted_df.csv')