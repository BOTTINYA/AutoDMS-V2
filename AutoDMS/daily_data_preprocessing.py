#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
from time import time
import itertools
from google.cloud import bigquery
client = bigquery.Client()                     #préparation du client pour interroger BigQuery et garder les data dans un pd.DataFrame

import collections
    
class preprocessed_data_for_prediction:
	# ------------------- Récupération des données qui ont servi à l'entrainement du modèle ----------------
	data = pd.read_csv('../AutoDMS-V2/Data/Data_Resampled.csv')

	training_feature_names = list(data)[:-1]            #le nom des colonnes des features d'entrainement
	training_target_name = list(data)[-1]                #le nom de la colonne des classes cibles

	#Put te Class_Name at the end of the DataFrame columns
	training_columns = list(np.sort(training_feature_names))      #on arrange les colonnes issues du set d'entrainement 

	#--------------- Extract prediction data --------------------------

	print('Querying BigQuery for daily shortage prediction analysis...')

	sql_pred = """
	SELECT DISTINCT * FROM `electric-armor-213817.Donnees_journalieres.Mise_en_Forme_Extract_journalier_MSTR_CSL`
	WHERE PREPARATION_DATE < CURRENT_DATE
	"""

	start_time = time()

	data_to_predict = client.query(sql_pred).to_dataframe()         #Interrogation de BigQuery 

	print('Querying and loading time = {:0.2f} s '.format(time() - start_time))
	print('Request finished\n')


	#--------------- Prediction data preprocessing -----------------------------------------
	#On conserve le DataFrame appelé 'data_to_predict' auquel on viendra ajouté ensuite les prédictions de l'algo
	#on crée un DataFrame intermédiaire appelé 'df_for_prediction' qui récupère les données journalières pour transformer les données catégoriques et ne va prendre que les colonnes du dataset d'entrainement



	#One Hot Encode des données catégoriques (Usine, DC) pour 
	DC_pred = pd.get_dummies(data_to_predict.PLT_DSC)
	PLANT_pred = pd.get_dummies(data_to_predict.Usine)
	#MARQUE = pd.get_dummies(data.Umbrella_Brand)

	df_for_prediction = pd.concat([PLANT_pred,DC_pred,data_to_predict], axis=1)

	df_for_prediction = df_for_prediction[training_columns]
	df_for_prediction = df_for_prediction.dropna()



	# ---------------- Comparaison entre le dataframe d'entrainement et dataframe de prédiction pour vérification de cohérence --------------------

	print('Training dataframe has ',data.shape[1]-1, ' features plus one target column')
	print('Prediction dataframe has ',df_for_prediction.shape[1], ' features')

	if data.shape[1]-1 != df_for_prediction.shape[1]:
		raise ValueError("Number of features between training set and prediction set is different")


	#On veut prédire la classe de toutes les ruptures, on conserve donc les données dans une liste que l'on fera passer dasn l'algo
	X_to_predict = df_for_prediction.iloc[:, :].values



	data = X_to_predict
	feature_names = training_columns


	print('Data Preprocessing finished')