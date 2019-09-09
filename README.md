# AutoDMS-V2

**Ce dépot contient le code source pour la nouvelle version du AutoDMS qui combine règles dures pour une première passe de classification des ruptures, puis du ML pour une deuxième passe sur les ruptures non classées.**


Le dépot AutoDMS-V2 est composé de plusieurs dossiers.

   - '/Data' contient: 
        - Le code qui extrait les données d'entrainement depuis la table BigQuery (data_extraction.py) et exporte ces données dans un .csv (Data_Raw.csv)
        - Le code qui fait le cleaning rapide des données brutes (data_cleaning_for_training.py) et exporte les données dans un .csv (Data_Roughly_Cleaned.csv)
        - Le code qui fait le resampling de nos données à cause du fort déséquilibre du problème (data_resampling.py) et exporte les données dans un .csv (Data_Resampled.csv). Dans ce code on retrouve les réglages pour resampling du problème
        - 'Data Analysis Archive DMS.ipynb' qui est un notebook qui nous sert à la visualisation des données pour analyse préalable à chaque fois que l'historique des ruptures est complété
          
   - '/AutoDMS' contient :
       - 'model_training.py' qui est le code qui réalise l'entrainement du model et la sauvegarde du modèle entrainé sous le nom 'trained.model.joblib'
       - 'regles_dures_classification.py' qui est l'implémentation des règles en dur de classification des ruptures en accord avec les équipes supply
       - 'daily_data_preprocessing.py' qui est le code de cleaning et mise en forme des données du jour par rapport au data set d'entrainement
       - 'main.py' qui est le code qui lance le process pour les prédictions du jour avec récupération des données du jour dans BQ, predictions à partir du modèle entrainé, puis export vers la table BigQuery 
       - 'model_testing_and_validation_XGB_DataV2.ipynb' qui est le code de test du modèle pour vérification des performances et interpretation avec analyse SHAP
       
       