#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#This code performs the extraction of data from BigQuery, cleaning of data, preprocessing and resampling of data for building the Training set
#This code is to be launched everytime new archived data from the official DMS is to be added to the BigQuery tables


#perform data extraction from BigQuery

import data_extraction
import data_cleaning_for_training
import data_resampling

data_extraction
data_cleaning_for_training
data_resampling