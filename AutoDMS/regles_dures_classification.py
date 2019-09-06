#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# ------------------ Importation des bibliothèques utilisées ---------------
import pandas as pd



#------------------------ Retravail des prédictions -----------------------
class hard_coded_rules:
    
	def flag_rupture(row):
		#Fonction qui flag lorsqu'il n'y a pas de rupture
		val=0
		if row['RUPTURE'] > 0:
			val = 1
		else:
			val = 0
		return val

	def flag_livraison(row):
		#fonction qui va passer la classe à "Livré" si RUPTURE = 0
		classe=row['Class_Prediction']
		if row['RUPTURE'] == 0:
			classe = 'Livré'
		else:
			pass
		return classe
			

	def rejet_cause_prev(row):
		#fonction qui rejete de la cause prévisions une rupture qui présente Prev>Commande 
		#ou pour lequel l'écart de prévision national est nul
		#ou pour lequel le CSL_alloc_National est de 100%
		classe = row['Class_Prediction']
		proba = row['Class_Prediction_probability']
		if (((row['PREVISION'] > row['COMMANDE'])  | (row['CSL_ALLOC_NATIONAL'] == 100.0) | (row['ECART_PREVISION_NAT_PERCENT'] == 0.0)) & (classe == 'Previsions')):
			classe = "A Creuser"
			proba = 1
		else:
			pass
		return classe    #il faudrait aussi modifier la probabilité à 1 mais je ne sais pas encore comment le faire




