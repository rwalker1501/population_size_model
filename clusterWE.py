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
from mobility import *
from elevation import *

def clusterworld(lon,lat,adjlist,ix,productthresh,densities,mobfactor,elev):
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
               elevdiff = abs(elev[i]-elev[j])
               if (sq*mobfactor >= productthresh) and (elevdiff < elevthresh):
             # I tested this function but results do not look good
             #  if (sq*mobfactor >= productthresh) and elev[i]<elevthresh and elev[j]<elevthresh:
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

def addtrace(clustertrace,counter,ya,clusters,colors,densities,ix):
   singletonpop = 0
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
      else:
         singletonpop = singletonpop + densities[ix][c[0]]
   return singletonpop

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
   clusters.sort(key=len,reverse=True)
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
productthresh = 400000000
#added parametrization
elevthresh=500
#fromkya = 36.4
#tokya = 36
#step = 1
#fromkya = 120
#tokya = 0
#step = 40
fromkya = 17
tokya = 2
step = 4

if (len(sys.argv)>1):
  adjthresh = int(sys.argv[1])
if (len(sys.argv)>2):
  productthresh = int(sys.argv[2])
if (len(sys.argv)>3):
  fromkya = int(sys.argv[3])
if (len(sys.argv)>4):
  tokya = int(sys.argv[4])

adjfile = "population_data/all-adj.txt"
if adjthresh == 300:
   adjfile = "population_data/all-adj300.txt"

print("Parameters")
print(" ---")
print(" Product threshold (population^2)", productthresh)
print(" From (kiloyears ago)", fromkya)
print(" To   (kiloyears ago)", tokya)
print()
 
lon=population_data.lon_array
lat=population_data.lat_array
densities=population_data.density_array
elev=getelevationarray()

preedges = loadadjfromfile(adjfile)
adjlist = makeadjlist(len(lon),preedges)
mobdf = readmobility()

numquarters = 6084
first = int(numquarters-1 - fromkya*40)
last = int(numquarters-1 - tokya*40)

print("time indexes:",first,last)

counter = 1
images = []
clustertrace = {}
clustertrace['clusterid'] = []
spops = {}
stryas = []
for ix in range(first,last,step):
   ya = (numquarters - ix)*25
   print(ix,"(",ya,"years ago )")
   mobfactor = getmobility(mobdf,ya)
   # mobfactor = 1
   clusters = clusterworld(lon,lat,adjlist,ix,productthresh,densities,mobfactor,elev)
   caption = str(ya) + " years ago"
   ix0 = f'{counter:02d}'+'-'
   filename = "PLOTS/world"+ix0+str(ya)+"ya.png"
   images.append(filename)
   if counter == 1:
      colortags = tagclusters(clusters,len(lon),densities[ix])
   else:
      temptags = tagclusters(clusters,len(lon),densities[ix])
      colortags = resolvetags(temptags,oldtags,clusters,densities[ix])
   clustercolors = getcolors(clusters,colortags)
   printclusters(clusters,clustercolors,densities,ix)
   spop = addtrace(clustertrace,counter,ya,clusters,clustercolors,densities,ix) 
   strya = str(ya)+'ya'
   stryas.append(strya)
   spops[strya] = spop
   # print(strya,spop)
   plotWEclusters(clusters,clustercolors,lon,lat,filename,caption)
   oldtags = colortags
   counter = counter + 1

# add row of singleton totals
clustertrace['clusterid'].append(-1)
for s in stryas:
   clustertrace[s].append(spops[s])
df = pd.DataFrame(clustertrace)
df.to_csv("trace.csv",index = False)

animate(images,"PLOTS/movie.mp4")
