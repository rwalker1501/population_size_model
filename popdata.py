import os
import numpy as np
import json
from classes_module import Target, PopulationData

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

def savepopcomputations(base_path,populations,data_name='pops'):
    pop_data_path = os.path.join(base_path, "population_data")
    binary_path = os.path.join(pop_data_path, data_name + '.npz')
    print("saving to",binary_path,"...")
    np.savez_compressed(binary_path,populations=populations)
    print("saved",binary_path)

def loadpopcomputations(base_path,data_name='pops'):
    pop_data_path = os.path.join(base_path, "population_data")
    binary_path = os.path.join(pop_data_path, data_name + '.npz')
    with np.load(binary_path) as data:
       populations = data['populations']
    return populations

