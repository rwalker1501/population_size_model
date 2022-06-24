import sys
import pandas as pd
import os
import numpy as np
from classes_module import Target, PopulationData
import json
from adjlib import *
from nvalslib import *
from poplib2 import *
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

targetfile = "testdata.csv"
outfile = "results.csv" 
threshfile = "thresholds.csv"
threshindex = 0

if (len(sys.argv)>1):
   targetfile = sys.argv[1]
if (len(sys.argv)>2):
   outfile = sys.argv[2]
if (len(sys.argv)>3):
   threshfile = sys.argv[3]
if (len(sys.argv)>4):
   threshindex = int(sys.argv[4])

#base_path='smb://127.0.0.1/Google Drive/My Drive/Documents 2022/Human exceptionalism/Population size/John Vergara Model/POPESTNew/'
base_path=''
population_data_name='Eriksson'
population_data=load_population_data_source(base_path, population_data_name)

adjfile = "population_data/all-adj.txt"

print()
print("Threshold file:", threshfile)
params = pd.read_csv(threshfile)

adjthresh = params['adjacency'][threshindex]
productthresh = params['product'][threshindex]
gravitythresh = params['gravity'][threshindex]

print("Adjacency threshold (km)", adjthresh)
print("Product threshold (population^2)", productthresh)
print("Gravity threshold (population^2/km^2)", gravitythresh)
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
print("Target file:", targetfile)
targets = pd.read_csv(targetfile)

targets["Nearest hexagon"] = 0
targets["Nearest longitude"] = 0.0
targets["Nearest latitude"] = 0.0
targets["Adjacent cell count"] = 0
targets["Adjacent population"] = 0
targets["Product-based cell count"] = 0
targets["Product-based population"] = 0
targets["Gravity-based cell count"] = 0
targets["Gravity-based population"] = 0
    
for i in targets.index:    
    centerlon = targets['Longitude'][i]
    centerlat = targets['Latitude'][i]
    earliestage = targets['Earliest age in sample'][i]
    kya = earliestage/1000
    
    print()
    print("Target ", i, "- (", centerlon, centerlat,"), kya=", kya)
    print(targets['Name'][i])
    print("Earliest age in sample:",earliestage)

    nearest = nearestnode(centerlon,centerlat,lon,lat)
    
    preedges = loadadjfromfile(adjfile)

    clustersize1,popsize1,cells1 = popbyadj(lon,lat,nearest,kya,preedges,densities)

    clustersize2,popsize2,cells2 = popbyproduct(lon,lat,nearest,kya,preedges,productthresh,densities)

    timeindex = 6084-int(kya*40)
    print('   Time index:',timeindex)
    print('   Nearest cell:', nearest, '(', lon[nearest], lat[nearest], ')')
    cix = cells1[0]
    print('      densities['+str(timeindex)+']['+str(cix)+']:',
              densities[timeindex][cells1[0]])
    print('   Surrounding cells')
    for i in range(1,7):
       cix = cells1[i]
       print('      ',cix, '(', lon[cix], lat[cix], ')',end='')
       print('      densities['+str(timeindex)+']['+str(cix)+']:',
                 densities[timeindex][cells1[cix]])
