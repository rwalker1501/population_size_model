import sys
import os
import numpy as np
import json
from adjlib import *
from nvalslib import *
from poplib2 import popbyadj, popbyproduct,popbygravity
from classes_module import Target, PopulationData
from worldplotter import *

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
  


base_path='smb://127.0.0.1/Google Drive/My Drive/Documents 2022/Human exceptionalism/Population size/John Vergara Model/POPESTNew/'
base_path=''
population_data_name='Eriksson'
population_data=load_population_data_source(base_path, population_data_name)

lonfile = "DATA/long.txt"
latfile = "DATA/lat.txt"
adjfile = "population_data/all-adj.txt"
centerlon = 355.877
centerlat = 43.377
adjthresh = 150
kya = 36
productthresh = 20000000
if (len(sys.argv)>1):
  centerlon = float(sys.argv[1])
if (len(sys.argv)>2):
  centerlat = float(sys.argv[2])
if (len(sys.argv)>3):
  kya = int(sys.argv[3])
if (len(sys.argv)>4):
  adjthresh = int(sys.argv[4])
if (len(sys.argv)>5):
  productthresh = int(sys.argv[5])
gravitythresh = productthresh/(100*100) # derived gravity threshold from product threshold
if (len(sys.argv)>6):
  gravitythresh = int(sys.argv[6])

print("Parameters")
print(" Target", centerlon, centerlat)
print(" 1000s years ago (kYA)", kya)
print(" ---")
print(" Adjacency threshold (km)", adjthresh)
print(" Product threshold (population^2)", productthresh)
print(" Gravity threshold (population^2/km^2)", gravitythresh)
print()
 
# =============================================================================
# with open(lonfile) as f:
#     lon = [float(x) for x in f.read().splitlines()]
# 
# with open(latfile) as f:
#     lat = [float(x) for x in f.read().splitlines()]
# =============================================================================


lon=population_data.lon_array
lat=population_data.lat_array
densities=population_data.density_array
nearest = nearestnode(centerlon,centerlat,lon,lat)
print(nearest, ":", lon[nearest],lat[nearest], "is the nearest node to target", centerlon, centerlat)

#preedges = makeadj(lon,lat,adjthresh,centerlon,centerlat)
preedges = loadadjfromfile(adjfile)

clustersize1,popsize1,cells1 = popbyadj(lon,lat,nearest,kya,preedges,densities)
print("Adjacency Results")
print(" cluster size is", clustersize1)
print(" population size is", popsize1)

clustersize2,popsize2,cells2 = popbyproduct(lon,lat,nearest,kya,preedges,productthresh,densities)
print("Product Filter Results")
print(" cluster size is", clustersize2)
print(" population size is", popsize2)

clustersize3,popsize3,cells3 = popbygravity(lon,lat,nearest,kya,preedges,gravitythresh,densities)
print("Gravity Filter Results")
print(" cluster size is", clustersize3)
print(" population size is", popsize3)

plotworld(cells1,cells2,cells3,lon,lat,"PLOTS/worldmap.png","world map")

