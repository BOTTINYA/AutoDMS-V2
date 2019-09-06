#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import google.datalab.bigquery as bq
import pandas as pd
import numpy as np
from time import time
import itertools

import daily_data_preprocessing
from regles_dures_classification import hard_coded_rules

import matplotlib.pyplot as plt
import collections


temp =  daily_data_preprocessing.preprocessed_data_for_prediction()

X_to_predict =  temp.data
feature_names = temp.feature_names
data_to_predict = temp.data_to_predict


# ---------------- Perform predictions ----------------------
print('Batch prediction of daily shortages...')

#---------------------------- Choose which model to load -------------------
#get the trained model
from joblib import load
model = load('trained_model.joblib')



#Perform predictions and get probabilities
y_to_predict = model.predict(X_to_predict)
y_to_predict_proba = model.predict_proba(X_to_predict)

y_to_predict_proba = np.amax(y_to_predict_proba, axis=1)

Y_to_predict_df = pd.DataFrame( {"Class_Prediction":y_to_predict})
Y_to_predict_proba_df = pd.DataFrame( {"Class_Prediction_probability":y_to_predict_proba})

#Build the predicted Pandas DataFrame
Final_predicted_df = pd.concat([data_to_predict,Y_to_predict_df,Y_to_predict_proba_df], axis=1)

Final_predicted_df = Final_predicted_df.dropna()

print('Batch prediction finished')



#---------------------- retravail de la classification avec les règles en dur -------------------------


#Application de ces règles au dataframe
Final_predicted_df['FLAG_RUPTURE'] = Final_predicted_df.apply(hard_coded_rules.flag_rupture, axis=1)
Final_predicted_df['Class_Prediction'] = Final_predicted_df.apply(hard_coded_rules.rejet_cause_prev, axis=1)
Final_predicted_df['Class_Prediction'] = Final_predicted_df.apply(hard_coded_rules.flag_livraison, axis=1)


#--------------------- BigQuery Exportation ----------------------------
print('Export to BigQuery table...')
start_time = time()

#Export vers BigQuery
bigquery_dataset_name = 'electric-armor-213817.Donnees_journalieres'
bigquery_table_name = 'Classification_journaliere'

# Define BigQuery dataset and table
dataset = bq.Dataset(bigquery_dataset_name)
table = bq.Table(bigquery_dataset_name + '.' + bigquery_table_name)


# Create or overwrite the existing table if it exists
table_schema = bq.Schema.from_data(Final_predicted_df)
table.create(schema = table_schema, overwrite = True)

# Write the DataFrame to a BigQuery table
table.insert(Final_predicted_df)
print('BigQuery export finished. \nExporting process took {:0.2f}min'.format((time()-start_time)/60))