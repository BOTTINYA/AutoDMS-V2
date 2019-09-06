#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import google.datalab.bigquery as bq
import pandas as pd
import numpy as np
from time import time
import itertools
from daily_data_preprocessing import preprocessed_data_for_prediction

import matplotlib.pyplot as plt
import collections


X_to_predict =  preprocessed_data_for_prediction [0]



# ---------------- Perform predictions ----------------------
print('Batch prediction of daily shortages...')

#---------------------------- Choose which model to load -------------------
#get the trained model
from joblib import load
model = load('trained_XGB_V2.joblib')



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



