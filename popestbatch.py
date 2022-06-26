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
from popdata import *

plotsfolder = "PLOTS/"

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
# =============================================================================
# lonfile = "DATA/long.txt"
# latfile = "DATA/lat.txt"
# =============================================================================

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
    kya = targets['Earliest age in sample'][i]/1000
    
    print("Target ", i, "-", centerlon, centerlat, kya)

    nearest = nearestnode(centerlon,centerlat,lon,lat)
    
#   preedges = makeadj(lon,lat,adjthresh,centerlon,centerlat)
    preedges = loadadjfromfile(adjfile)

    clustersize1,popsize1,cells1 = popbyadj(lon,lat,nearest,kya,preedges,densities)

    clustersize2,popsize2,cells2 = popbyproduct(lon,lat,nearest,kya,preedges,productthresh,densities)

    clustersize3,popsize3,cells3 = popbygravity(lon,lat,nearest,kya,preedges,gravitythresh,densities)

    targets.at[i,"Nearest hexagon"] = nearest
    targets.at[i,"Nearest longitude"] = lon[nearest]
    targets.at[i,"Nearest latitude"] = lat[nearest]
    targets.at[i,"Adjacent cell count"] = clustersize1
    targets.at[i,"Adjacent population"] = popsize1
    targets.at[i,"Product-based cell count"] = clustersize2
    targets.at[i,"Product-based population"] = popsize2
    targets.at[i,"Gravity-based cell count"] = clustersize3
    targets.at[i,"Gravity-based population"] = popsize3

    caption = targets['Name'][i]
    filename = plotsfolder+"world"+str(i)+".png"
    plotworld(cells1,cells2,cells3,lon,lat,filename,caption)

print()
print("Results written to file:", outfile)
targets.to_csv(outfile)
