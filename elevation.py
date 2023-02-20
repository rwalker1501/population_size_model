import pandas as pd
import numpy as np

def readelevation():
   df = pd.read_csv('population_data/elev.mean.csv')
   return df

def getelevationarray():
   df = readelevation()
   return df['elev_mean']

