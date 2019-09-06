#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from time import time
from google.cloud import bigquery

client = bigquery.Client()                     #préparation du client pour interroger BigQuery et garder les data dans un pd.DataFrame

sql5 = """
WITH
  DMS AS (
  SELECT
    ROW_NUMBER() OVER(PARTITION BY date_pr__pa, Code_SAP ORDER BY FLAG_CF ASC) AS ROW,
    FLAG_CF,
    CAST(date_pr__pa AS DATE) AS DATE_PREPA,
    Code_SAP,
    Import_type,
    Usine,
    Base,
    Index_Pareto,
    Cause_Pareto
  FROM
    `electric-armor-213817.Archives_DMS.DMS_2019_07_30`
  GROUP BY
    FLAG_CF,
    date_pr__pa,
    Code_SAP,
    Usine,
    Import_type,
    Base,
    Index_Pareto,
    Cause_Pareto )
  #----------------------------------------------------------------------------
SELECT
  FLAG_CF,
  PREPARATION_DATE,
  PDT_COD,
  PDT_DSC,
IF
  (Forecast_table.Transformable = 'OUI',
    1,
    0) AS TRANSFORMABLE,
  IF(DATE_DIFF( PREPARATION_DATE,CAST(BDD_PDT.Product_launch_date AS DATE), MONTH) < 2 ,1,0) AS INNO,
  IF(Reft = '01 Afh', 1,0) AS IMPLUSE,
  BDD_PDT.Umbrella_Brand,
  DMS.Import_type,
  DMS.Usine,
  PLT_COD,
  PLT_DSC,
  SUM(Forecast_table.Forecast_including_adjustments) OVER(PARTITION BY Forecast_table.date, SAP_code ) AS PREVISION_NATIONAL,
  COMMANDE_NATIONAL,
  ALLOUE_NATIONAL,
  LIVRE_NATIONAL,
  (ALLOUE_NATIONAL - LIVRE_NATIONAL) AS ECART_ALLOC_NATIONAL,
  RUPTURE_NATIONAL,
  RUPTURE_STKA_NATIONAL,
IF
  (SUM(Forecast_table.Forecast_including_adjustments) OVER(PARTITION BY Forecast_table.date, SAP_code ) = 0,
    1,
    0) AS NO_FORECAST_NAT,
  COMMANDE_NATIONAL - SUM(Forecast_table.Forecast_including_adjustments) OVER(PARTITION BY Forecast_table.date, SAP_code ) AS ECART_PREVISION_NAT,
IF
  (SUM(Forecast_table.Forecast_including_adjustments) OVER(PARTITION BY Forecast_table.date, SAP_code ) = 0,
    90000,
    (SUM(Forecast_table.Forecast_including_adjustments) OVER(PARTITION BY Forecast_table.date, SAP_code ) - COMMANDE_NATIONAL)*100 / SUM(Forecast_table.Forecast_including_adjustments) OVER(PARTITION BY Forecast_table.date, SAP_code )) AS ECART_PREVISION_NAT_PERCENT,
  Forecast_table.Forecast_including_adjustments AS PREVISION,
  COMMANDE,
  ALLOUE,
  LIVRE,
  (ALLOUE - LIVRE) AS ECART_ALLOC,
  RUPTURE,
  RUPTURE_STKA,
IF
  (Forecast_table.Forecast_including_adjustments = 0,
    1,
    0) AS NO_FORECAST,
  COMMANDE - Forecast_table.Forecast_including_adjustments AS ECART_PREVISON,
IF
  (Forecast_table.Forecast_including_adjustments = 0,
    10000,
    (Forecast_table.Forecast_including_adjustments - COMMANDE)*100 / Forecast_table.Forecast_including_adjustments) AS ECART_PREVISION_PERCENT,
  CSL_ALLOC,
  CSL,
  CSL_ALLOC - CSL AS PERTE_CSL_vs_ALLOC,
  CSL_ALLOC_NATIONAL,
  CSL_NATIONAL,
  CSL_ALLOC_NATIONAL - CSL_NATIONAL AS PERTE_CSL_vs_ALLOC_NATIONAL,
  DMS.Cause_Pareto
FROM
  `electric-armor-213817.Archives_MicroStrategy.CSL_20181201_to_20190630_clean` AS MSTR_Archive_table,
  `electric-armor-213817.Data_Forecasts.Data_Forecasts_CAR` AS Forecast_table,
  `electric-armor-213817.Fichiers_produits.REFERENTIEL_PRODUITS_V2` AS BDD_PDT,
  DMS
WHERE
  MSTR_Archive_table.PREPARATION_DATE = Forecast_table.date
  AND MSTR_Archive_table.PLT_DSC = Forecast_table.DC
  AND MSTR_Archive_table.PDT_COD = Forecast_table.SAP_code
  AND MSTR_Archive_table.PDT_COD = BDD_PDT.Codification
  AND MSTR_Archive_table.PREPARATION_DATE = DMS.DATE_PREPA
  AND MSTR_Archive_table.PDT_COD = DMS.Code_SAP 
  AND IF(DMS.FLAG_CF = 0, TRUE, MSTR_Archive_table.PLT_DSC = DMS.Base)     #Condition sur quelle base joindre dans le cas ou j'ai une CF ou non (car top 10 donné sans la base)

"""

start_time = time()

df = client.query(sql5).to_dataframe()

df.to_csv('Data_Raw.csv', index = False)



print('Querying and loading time = {:0.2f} s \n'.format(time() - start_time))

