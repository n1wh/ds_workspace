# This script contains default libs which will be uploaded on any ipython/jupyter startup

### create a hard symlink from this file into ~/.ipython/profile_default/startup/
#$: ln jupyter_startup_libs.py ~/.ipython/profile_default/startup/jupyter_startup_libs.py

# built-in
import os
import sys
import datetime as dt
import time
import copy
import pickle
import requests

# 3rd party
import pandas as pd
pd.options.display.max_columns = 100
pd.options.display.max_rows = 500

import numpy as np
import scipy as sc
#from scipy.stats import probplot

# visualization
#%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()
sns.set_style("darkgrid")
sns.set_context("paper")
sns.palplot(color)
#sns.set(rc={'figure.figsize': (9, 6)})

"""
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
init_notebook_mode(connected=True)
import cufflinks as cf
cf.go_offline(connected=True)
cf.set_config_file(theme='pearl')
"""


# plot config
from pylab import rcParams

SMALL_SIZE = 10
MEDIUM_SIZE = 14
BIGGER_SIZE = 18

rcParams['figure.figsize'] = 10, 6
rcParams['figure.titlesize'] = BIGGER_SIZE
rcParams['font.size'] = MEDIUM_SIZE

rcParams['axes.titlesize'] = BIGGER_SIZE
rcParams['axes.labelsize'] = MEDIUM_SIZE
rcParams['axes.labelcolor'] = 'grey'

rcParams['text.color'] = 'grey'
rcParams['legend.fontsize'] = MEDIUM_SIZE

rcParams['xtick.color'] = 'grey'
rcParams['xtick.labelsize'] = MEDIUM_SIZE
rcParams['ytick.color'] = 'grey'
rcParams['ytick.labelsize'] = MEDIUM_SIZE

# constants
SEED = 11
np.random.seed(SEED)


