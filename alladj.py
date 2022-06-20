
# program to generate adjacency file

import sys
import os
import numpy as np
from adjlib import *

from classes_module import Target, PopulationData
import json
from adjlib import *

def load_population_data_source(base_path, population_data_name):
    
    pop_data_path = os.path.join(base_path, "population_data")

    binary_path = os.path.join(pop_data_path, population_data_name + '.npz')
    info_file_path = os.path.join(pop_data_path, population_data_name + '_info.txt')

    label='txt'
    if population_data_name == "timmermann":
        label='ncf'

    data=np.load(binary_path)
    lats_txt=data['lats_' + label]
    lons_txt=data['lons_' + label]
    ts_txt=data['ts_' + label]
    dens_txt=data['dens_' + label]
    
    print(info_file_path)
    population_data_info = json.load(open(info_file_path));
    new_population_data = PopulationData(population_data_name, lats_txt, lons_txt, ts_txt, dens_txt, population_data_info)
    return new_population_data


base_path=''
population_data_name='Eriksson'
population_data=load_population_data_source(base_path, population_data_name)
lon=population_data.lon_array
lat=population_data.lat_array
adjfile = "population_data/all-adj.txt"

edges = makeadj(lon,lat)
saveadj(edges,adjfile)
