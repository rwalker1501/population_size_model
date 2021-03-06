import sys
import numpy as np
import json
from adjlib import *
from nvalslib import *
from poplib2 import *
from classes_module import Target, PopulationData
from worldplotter import *
from popdata import *
import pandas as pd

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

def printclusters(clusters,colors,densities,ix):
   n = len(clusters)
   for i in range(n):
      c = clusters[i]
      size = len(c)
      if size > 1:
         pop = 0
         for cell in c:
            pop = pop + densities[ix][cell]
         print("   ",size,"("+str(pop)+") id:",colors[i])
   print()

def mergeclusters(clusters,densities,ix,populations):
   n = len(clusters)
   for i in range(n):
      c = clusters[i]
      size = len(c)
      if size > 1:
         pop = 0
         for cell in c:
            pop = pop + densities[ix][cell]
         for cell in c:
            populations[ix][cell] = pop

def addtrace(clustertrace,counter,ya,clusters,colors,densities,ix):
   strya = str(ya)+'ya'
   clustertrace[strya] = [0]*len(clustertrace['clusterid'])
   n = len(clusters)
   for i in range(n):
      c = clusters[i]
      size = len(c)
      if size > 1:
         pop = 0
         for cell in c:
            pop = pop + densities[ix][cell]
         id = colors[i]
         if id >= len(clustertrace['clusterid']):
            for key in clustertrace.keys():
               clustertrace[key].append(0)
            clustertrace['clusterid'][id]=id
         clustertrace[strya][id] = pop

def tagclusters(clusters,n,popix):
   tags = [-1]*n
   counter = 0
   for c in clusters:
      if len(c) == 1:
         if popix[c[0]] > 0:
            tags[c[0]] = -2
      elif len(c) > 1:
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
   if commontag == -1:
      del tagdict[-1]
      if len(tagdict)>0:
         commontag = max(tagdict, key=tagdict.get)
         if commontag == -2:
            del tagdict[-2]
            if len(tagdict)>0:
               commontag = max(tagdict, key=tagdict.get)
#   print("common:",commontag)
   return commontag

def resolvetags(newtags,oldtags,clusters,popix):
   availtag = max(oldtags)+1 # getnextavailabletag
   usedtags = {-1,-2}
   n = len(oldtags)
   tags = [-1]*n
   for c in clusters:
      if len(c) == 1:
         if popix[c[0]] > 0:
            tags[c[0]] = -2
      elif len(c) > 1:
         tagnum = maxtag(c,oldtags)
         if tagnum in usedtags:
            tagnum = availtag
            availtag = availtag+1
         usedtags.add(tagnum)
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

adjthresh = 150 # change to 300 if you want more adjacencies
productthresh = 20000000
#fromkya = 36.4
#tokya = 36
#step = 1
fromkya = 120
tokya = 0
step = 40


if (len(sys.argv)>1):
  adjthresh = int(sys.argv[1])
if (len(sys.argv)>2):
  productthresh = int(sys.argv[2])

adjfile = "population_data/all-adj.txt"
if adjthresh == 300:
   adjfile = "population_data/all-adj300.txt"

print("Parameters")
print(" ---")
print(" Product threshold (population^2)", productthresh)
 
lon=population_data.lon_array
lat=population_data.lat_array
densities=population_data.density_array

preedges = loadadjfromfile(adjfile)
adjlist = makeadjlist(len(lon),preedges)

numquarters = 6084
first = 0
last = 6084
# update the above to the following if you want a quicker run for testing
# first = 4600
# last = 4700
step = 1
print(" From (years ago)", (numquarters-1 - first)*25)
print(" To   (years ago)", (numquarters-1 - last)*25)
print()

print("time indexes:",first,last)
populations = densities.copy()

counter = 1
images = []
clustertrace = {}
clustertrace['clusterid'] = []
for ix in range(first,last,step):
   ya = (numquarters-1 - ix)*25
   print(ix,"(",ya,"years ago )")
   clusters = clusterworld(lon,lat,adjlist,ix,productthresh,densities)
   caption = str(ya) + " years ago"
   if counter == 1:
      colortags = tagclusters(clusters,len(lon),densities[ix])
   else:
      temptags = tagclusters(clusters,len(lon),densities[ix])
      colortags = resolvetags(temptags,oldtags,clusters,densities[ix])
   clustercolors = getcolors(clusters,colortags)
   # printclusters(clusters,clustercolors,densities,ix)
   mergeclusters(clusters,densities,ix,populations)
   oldtags = colortags
   counter = counter + 1

# the following code tests the contents of populations
# against output of clusterplot.py for the following params:
# centerlon = 355.877
# centerlat = 43.377
# adjthresh = 150
# fromkya = 36
# tokya = 35.6
# productthresh = 20000000

print("test values...")
for i in range(4644,4660):
   print(i,"population:",populations[i][5864])

# richard, you may save the populations list at this point
# below is my version

savefilename = 'pop-'+'adj'+str(adjthresh)+'-prod'+str(productthresh)
savepopcomputations(base_path,populations,savefilename)

