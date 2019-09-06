#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# ------------------ Importation des bibliothèques utilisées ---------------
import pandas as pd
import numpy as np
from time import time

import sklearn.metrics
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.metrics import classification_report

from google.cloud import bigquery

import xgboost as xgb

import collections
import joblib




#retrieve data from the Data directory
#To train our model, we want to use the Resampled Data for better performances
data = pd.read_csv('../Data/Data_Resampled.csv')

#Put the Class_Name at the end of the DataFrame columns
columns = list(data.columns)
columns.pop(columns.index('Cause_Pareto'))
columns.append('Cause_Pareto')
data = data[columns]




#-----------------------------------Data separation for validation and testing ----------------------------------------------------------
#séparation feature et target_class
X = data.iloc[:, :-1].values    #Inputs
y = data.iloc[:,-1].values      #Output

class_names  = list(set(y))                  #on récupère les noms des classes pour l'analyse SHAP
class_names.sort()                           #on range ces classes par ordre alphabétique

feature_names = list(data)[:-1]              #on récupère les noms des colonnes pour l'analyse SHAP


#test train split
test_fraction = 0.01
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=test_fraction, random_state=42)




#-----------------------------------tuning of XGB ----------------------------------------------
from time import time

start_time = time()

bst = xgb.XGBClassifier(scale_pos_weight=1,
                      learning_rate=0.1,  
                      colsample_bytree = 0.4,
                      subsample = 1,
                      n_estimators=150, 
                      min_child_weight = 3,
                      reg_alpha = 0.3,
                      max_depth=12, 
                      n_jobs=-1,
                      nthreads = 4,
                      gamma=10)


bst.fit(X_train, y_train)

fitting_time = time()-start_time

print('Total fitting time = {:0.2f}s.'.format(fitting_time))

model = bst


#------------------------------------Perform predictions and test model-----------------------------------------------------------
y_predict = model.predict(X_test)
y_predict_proba = model.predict_proba(X_test)


#------------------ Sauvegarde du modèle dans dossier courrant ----------------
from joblib import dump

#Sauvegarde en local
dump(model, 'trained_model.joblib') 