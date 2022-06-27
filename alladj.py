
# program to generate adjacency file

import sys
import os
import numpy as np
from adjlib import *

from classes_module import Target, PopulationData
import json
from adjlib import *
from popdata import *

base_path=''
population_data_name='Eriksson'
population_data=load_population_data_source(base_path, population_data_name)
lon=population_data.lon_array
lat=population_data.lat_array
# adjfile = "population_data/all-adj.txt"
adjfile = "population_data/all-adj1.txt"

edges = makeadj(lon,lat)
saveadj(edges,adjfile)
