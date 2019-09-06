#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from time import time

from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, label_binarize
from sklearn.decomposition import PCA, KernelPCA

import matplotlib.pyplot as plt
import collections
import scikitplot as skplt
import seaborn as sns

from google.cloud import bigquery

