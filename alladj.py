
# program to generate adjacency file

import sys
import os
import numpy as np
import pandas as pd
from adjlib import *

from classes_module import Target, PopulationData
import json
from adjlib import *
from popdata import *

base_path=''
population_data_name='Eriksson'
population_data=load_population_data_source(base_path, population_data_name)
#lon=population_data.lon_array
#lat=population_data.lat_array

lonworld=population_data.lon_array
latworld=population_data.lat_array
lldf = pd.DataFrame({'lon':lonworld,'lat':latworld})
filterdf = lldf[(lldf['lat']>31) & (lldf['lat']<62) & ((lldf['lon']>353) | (lldf['lon']< 60))]
lon = list(filterdf['lon'])
lat = list(filterdf['lat'])
print(len(lon),len(lat))

# adjfile = "population_data/all-adj.txt"
adjfile = "population_data/all-adj-small300.txt"

edges = makeadj(lon,lat,300)
saveadj(edges,adjfile)
