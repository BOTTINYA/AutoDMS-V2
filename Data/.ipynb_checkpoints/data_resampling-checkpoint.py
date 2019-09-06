#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import collections
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

df = pd.read_csv('Data_Roughly_Cleaned.csv')

#------------------- One Hot Encode of categorical data----------------------
data = df.drop(['PREPARATION_DATE', 'PLT_COD', 'PDT_COD', 'PDT_DSC'], axis = 1)

DC = pd.get_dummies(data.PLT_DSC)
PLANT = pd.get_dummies(data.Usine)
#MARQUE = pd.get_dummies(data.Umbrella_Brand)

data = pd.concat([PLANT,DC,data], axis=1)
data = data.drop(['PLT_DSC','Usine','Umbrella_Brand'], axis=1) 


#---------------------- Supression des lignes avec des NULLs--------------------
data.dropna()


#Conversion du DataFrame en ndarray pour passage dans algo
X = data.iloc[:, :-1].values    #Features
y = data.iloc[:,-1].values      #Labels 

feature_names = list(data)[:-1]
class_names = np.unique(y)

#----------------------Re-sampling ---------------------------------
populaire = [list(elem) for elem in collections.Counter(y).most_common()]
max_occurence = int(populaire[0][1])
populaire = pd.DataFrame(columns = ['Class_Name', 'Original_Number'], data = populaire)

max_percent = 0.5

dict_over = {
             'Transport': int(max_occurence*(max_percent-0.02)), 
 #            'Client': int(max_occurence*(max_percent)), 
             'Déploiement/Quarantaine': int(max_occurence*(max_percent-0.25)), 
             'Probleme Copacking': int(max_occurence*(max_percent-0.3)),
             'Production': int(max_occurence*(max_percent+0.2)),
             'Qualité': int(max_occurence*(max_percent+0.05)),
#             'Schéma': int(max_occurence*(max_percent-0.25)),
#             'Expe usine': int(max_occurence*(max_percent-0.3))
            }       #Je crée un dictionnaire ou je lui dit combien de sample je veux par classe 

dict_under = {
#             'A Creuser': int(max_occurence*0.8),
#             'Previsions': int(max_occurence*0.65)
             }

smote = SMOTE(sampling_strategy=dict_over,  k_neighbors=3)
under_sampler = RandomUnderSampler(sampling_strategy = dict_under )

X_SMOTE , y_SMOTE = smote.fit_sample(X,y)
X_SMOTE , y_SMOTE = under_sampler.fit_sample(X_SMOTE , y_SMOTE)

# ----------------- Reconstruction du DataFrame ---------------------
features_df = pd.DataFrame(data = X_SMOTE, columns = feature_names)
target_df = pd.DataFrame(data = y_SMOTE, columns = ['Cause_Pareto'])
data = pd.concat([features_df,target_df], axis=1)

print('DataFrame shape after One Hot Encoding of categorical features and Resampling with SMOTE : ', data.shape)

data.to_csv('Data_Resampled.csv', index=False)