import sys
import numpy as np
import json
from adjlib import *
from nvalslib import *
from poplib2 import *
from classes_module import Target, PopulationData
from worldplotter import *
from popdata import *

def clusterworld(lon,lat,adjlist,ix,productthresh,densities):
   n = len(adjlist)
   clustercount = 0
   clusters = []
   visited = []
   for i in range(n):
      visited.append(False)
   nonsingletons = 0
   for i in range(n):
      if (not visited[i]):
         visited[i] = True
         clusters.append([])
         clusters[clustercount] = [i]
         queue = [i]
         while len(queue) > 0:
            p = queue.pop(0);
#            print(p,len(queue))
            for j in adjlist[p]:
               sq = densities[ix][p]*densities[ix][j]
               if sq >= productthresh:
                  if (not visited[j]):
                     visited[j] = True
                     clusters[clustercount].append(j)
                     queue.append(j)
         if len(clusters[clustercount]) > 1:
            nonsingletons = nonsingletons + 1
         clustercount = clustercount + 1
   print("cluster count:",clustercount,",",nonsingletons,"non-singletons")
   return clusters

def printclusters(clusters,densities,ix):
   for c in clusters:
      size = len(c)
      if size > 1:
         pop = 0
         for cell in c:
            pop = pop + densities[ix][cell]
         print("   ",size,"("+str(pop)+")")
   print()

def initialtags(clusters,n):
   tags = [-1]*n
   counter = 0
   for c in clusters:
      if len(c) > 1:
         for i in c:
            tags[i] = counter
         counter = counter + 1
   return tags

def maxtag(c,oldtags):
   tagdict = dict()
   for i in c:
      tag = oldtags[i]
      if tag in tagdict:
         tagdict[tag] = tagdict[tag] + 1
      else:
         tagdict[tag] = 1
   commontag = max(tagdict, key=tagdict.get)
   return commontag

def tagclusters(clusters,oldtags):
   n = len(oldtags)
   tags = [-1]*n
   for c in clusters:
      if len(c) > 1:
         tagnum = maxtag(c,oldtags)
         for i in c:
            tags[i] = tagnum
   return tags

def getcolors(clusters,colortags):
   n = len(clusters)
   colors = [-1]*n
   for i in range(n):
      colors[i] = colortags[clusters[i][0]]
   return colors

base_path='smb://127.0.0.1/Google Drive/My Drive/Documents 2022/Human exceptionalism/Population size/John Vergara Model/POPESTNew/'
base_path=''
population_data_name='Eriksson'
population_data=load_population_data_source(base_path, population_data_name)

adjfile = "population_data/all-adj.txt"
adjthresh = 250  ##this actually uses adjacencies file
fromkya = 120
tokya = 0
productthresh = 20000000
if (len(sys.argv)>1):
  productthresh = int(sys.argv[1])
if (len(sys.argv)>2):
  fromkya = int(sys.argv[2])
if (len(sys.argv)>3):
  tokya = int(sys.argv[3])

print("Parameters")
print(" ---")
print(" Product threshold (population^2)", productthresh)
print(" From (kiloyears ago)", fromkya)
print(" To   (kiloyears ago)", tokya)
print()
 
lon=population_data.lon_array
lat=population_data.lat_array
densities=population_data.density_array

preedges = loadadjfromfile(adjfile)
adjlist = makeadjlist(len(lon),preedges)

numquarters = 6084
first = int(numquarters - fromkya*40)
last = int(numquarters - tokya*40)

print("time indexes:",first,last)

counter = 1
images = []
for ix in range(first,last,40):
   ya = (numquarters - ix)*25
   print(ix,"(",ya,"years ago )")
   clusters = clusterworld(lon,lat,adjlist,ix,productthresh,densities)
   printclusters(clusters,densities,ix)
   caption = str(ya) + " years ago"
   ix0 = f'{counter:02d}'+'-'
   filename = "PLOTS/world"+ix0+str(ya)+"ya.png"
   images.append(filename)
   if counter == 1:
      colortags = initialtags(clusters,len(lon))
   else:
      colortags = tagclusters(clusters,oldtags)
   clustercolors = getcolors(clusters,colortags)
   plotworldclusters(clusters,clustercolors,lon,lat,filename,caption)
   oldtags = colortags
   counter = counter + 1

animate(images,"PLOTS/movie.mp4")
