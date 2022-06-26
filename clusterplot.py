import sys
import numpy as np
import json
from adjlib import *
from nvalslib import *
from poplib2 import *
from classes_module import Target, PopulationData
from worldplotter import *
from popdata import *

base_path='smb://127.0.0.1/Google Drive/My Drive/Documents 2022/Human exceptionalism/Population size/John Vergara Model/POPESTNew/'
base_path=''
population_data_name='Eriksson'
population_data=load_population_data_source(base_path, population_data_name)

adjfile = "population_data/all-adj.txt"
centerlon = 355.877
centerlat = 43.377
adjthresh = 150
fromkya = 36
tokya = 35.6
productthresh = 10000000
if (len(sys.argv)>1):
  centerlon = float(sys.argv[1])
if (len(sys.argv)>2):
  centerlat = float(sys.argv[2])
if (len(sys.argv)>3):
  productthresh = int(sys.argv[3])
if (len(sys.argv)>4):
  fromkya = int(sys.argv[4])
if (len(sys.argv)>5):
  tokya = int(sys.argv[5])

print("Parameters")
print(" Target", centerlon, centerlat)
print(" ---")
print(" Product threshold (population^2)", productthresh)
print(" From (kiloyears ago)", fromkya)
print(" To   (kiloyears ago)", tokya)
print()
 
lon=population_data.lon_array
lat=population_data.lat_array
densities=population_data.density_array
nearest = nearestnode(centerlon,centerlat,lon,lat)
print(nearest, ":", lon[nearest],lat[nearest], "is the nearest node to target", centerlon, centerlat)

preedges = loadadjfromfile(adjfile)

numquarters = 6084
first = int(numquarters - fromkya*40)
last = int(numquarters - tokya*40)

print("time indexes:",first,last)

counter = 1
images = []
for ix in range(first,last):
   clustersize,popsize,cells = popbyproductonetimeindex(lon,lat,nearest,ix,
                preedges,productthresh,densities)
   ya = (numquarters - ix)*25
   print(ix,"(",ya,"years ago ): ",end='')
   print(" cluster size =", clustersize, end='')
   print(" and population size =", popsize)
   caption = str(ya) + " years ago (" + str(clustersize) + " clusters)"
   ix0 = f'{counter:02d}'+'-'
   filename = "PLOTS/world"+ix0+str(ya)+"ya.png"
   images.append(filename)
   plotcluster(cells,lon,lat,filename,caption)
   counter = counter + 1

animate(images,"PLOTS/movie.mp4")
