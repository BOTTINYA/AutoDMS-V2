#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import pandas as pd

df = pd.read_csv('Data_Raw.csv')


    
#Regroupement de certaines causes dans la cause 'A Creuser'
df.loc[df['Cause_Pareto'] == 'Schéma', 'Cause_Pareto'] = 'A Creuser'
df.loc[df['Cause_Pareto'] == 'Expe usine', 'Cause_Pareto'] = 'A Creuser'

print('DataFrame Shape before deduplication = ',df.shape)

#Suppression des doublons
df = df.drop_duplicates(subset=['PREPARATION_DATE','PDT_COD','PLT_COD'], keep = 'first')             #On vire tous les doublons en regardant les colonnes 'date, SAP_code et DC' et on conserve uniquement la première occurence
df = df.dropna() 

df.to_csv('Data_Roughly_Cleaned.csv', index=False)

print('DataFrame Shape after deduplication = ', df.shape)

