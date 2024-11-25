from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import cross_val_score, KFold, train_test_split, cross_val_predict, GridSearchCV
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsRegressor
import plotly.express as px
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")
import itertools
import os
import pickle
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt