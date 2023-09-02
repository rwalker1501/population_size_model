import sys
import numpy as np
from adjlib import *
from nvalslib import *
from poplib2 import *
from classes_module import Target, PopulationData
from worldplotter import *
from popdata import *
import pandas as pd
from mobility import *
from elevation import *
import os.path as path

kya = 8
frompthresh = 4000000
topthresh =  10000000
steppthresh =  500000
fromethresh = 300
toethresh =   500
stepethresh =  20

def clusterworld(adjlist,ix,productthresh,densities,mobfactor,elev,ethresh):
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
                p = queue.pop(0)
                for j in adjlist[p]:
                    sq = densities[ix][p]*densities[ix][j]
                    elevdiff = abs(elev[i]-elev[j])
                    if (sq >= productthresh) and (elevdiff < ethresh):
#                   if (sq >= productthresh):
                        if (not visited[j]):
                            visited[j] = True
                            clusters[clustercount].append(j)
                            queue.append(j)
            if len(clusters[clustercount]) > 1:
                nonsingletons = nonsingletons + 1
            clustercount = clustercount + 1
#   print("cluster count:",clustercount,",",nonsingletons,"non-singletons")
    return clusters

def extractclusters(clusters,colors,densities,ix):
    celltocluster = {}
    clustertocell = {}
    n = len(clusters)
    clustertocell[-1] = []
    for i in range(n):
        clustertocell[i] = []
        c = clusters[i]
        size = len(c)
        for cell in c:
            if (lat[cell]>31 and lat[cell]<62) and (lon[cell]>353 or lon[cell]<60):
                if size > 1:
                    celltocluster[cell] = i
                    clustertocell[i].append(cell)
                else:
                    celltocluster[cell] = -1
                    clustertocell[-1].append(cell)
    return (celltocluster,clustertocell)

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

def getcolors(clusters,colortags):
    n = len(clusters)
    colors = [-1]*n
    for i in range(n):
        colors[i] = colortags[clusters[i][0]]
    return colors

potteryfilename = "cardium.txt"

def savehexagons(indexes,outfile = potteryfilename):
    with open(outfile,'w') as f:
        for x in indexes:
            # print(>> f, x, lon[x], lat[x])
            print(x,lon[x],lat[x], end="\n", file=f)

def loadhexagons(infile = potteryfilename):
    indexes = []
    if path.isfile(infile):
        with open(infile) as f:
             for x in f.read().splitlines():
                 indexes.append(int(x.split()[0]))
    return indexes

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def hamming(cellmap,clustermap,pottery):
    bestscore = len(cellmap)
    bestcluster = []
    bestM = 0
    numpottery = len(pottery)
    for c in clustermap:
        clus = clustermap[c]
        if len(clus) > 1 and c >= 0:
            mid = intersection(clus,pottery)
            M = len(mid)
            numclus = len(clus)
            thisscore = (numpottery+numclus) -2*M
            if thisscore < bestscore:
                bestscore = thisscore
                bestcluster = clus
                bestM = M
    return bestscore,bestcluster,bestM

def trythreshold(pottery,pthresh,eth,kya):
    numquarters = 6084
    ix = int(numquarters-1 - kya*40)
    ya = (numquarters - ix)*25
    mobfactor = getmobility(mobdf,ya)
    # mobfactor = 1
    clusters = clusterworld(adjlist,ix,pthresh,densities,mobfactor,elev,eth)
    caption = str(ya) + " years ago"
    filename = "PLOTS/WEsnap20M"+str(ya)+"ya.png"
    colortags = tagclusters(clusters,len(lon),densities[ix])
    clustercolors = getcolors(clusters,colortags)
    (cellmap,clustermap) = extractclusters(clusters,clustercolors,densities,ix)
    count = 0
    n = len(clusters)
    for i in range(n):
        if len(clustermap[i])>0:
            count = count + 1
    
    return hamming(cellmap,clustermap,pottery)

def clip(df):
   filterdf = df[(df['lat']>31) & (df['lat']<62) &
                 ((df['lon']>353) | (df['lon']< 60))]
   return filterdf

def plotWE(pottery,thecluster,caption):
    mapper = [0]*len(lon)
    for i in pottery:
        mapper[i] = 1
    for i in thecluster:
        if mapper[i] == 1:
            mapper[i] = 3
        else:
            mapper[i] = 2
    unclippeddf = pd.DataFrame({'lon':lon,'lat':lat,'pottery':mapper})
    unclippeddf['lon'] = [(x if x < 340 else x-360) for x in unclippeddf['lon']]
    df = clip(unclippeddf)
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    A = len(thecluster)
    B = len(pottery)
    M = len(intersection(thecluster,pottery))
    hamming = (A+B)-2*M
    plt.title(f'hamming distance:{hamming}, {caption}')
    plt.grid(True)
    values = df['pottery']
    colors = []
    for val in values:
        if val == 0:
            c = 'lightgrey' #bg - #D3D3D3
        elif val == 1:
            c = 'cyan'
        elif val == 2:
            c = 'blue' 
        else:
            c = '#7879FF' # intersection 
        colors.append(c)
    plt.scatter(df['lon'], df['lat'], s=30, color=colors)
    plt.show()


base_path='smb://127.0.0.1/Google Drive/My Drive/Documents 2022/Human exceptionalism/Population size/John Vergara Model/POPESTNew/'
base_path=''
population_data_name='Eriksson'
population_data=load_population_data_source(base_path, population_data_name)

adjthresh = 150 # change to 300 if you want more adjacencies

if (len(sys.argv)>1):
  kya = int(sys.argv[1])
if (len(sys.argv)>2):
  adjthresh = int(sys.argv[2])

adjfile = "population_data/all-adj.txt"
if adjthresh == 300:
   adjfile = "population_data/all-adj300.txt"

origlon=population_data.lon_array
lon = [(x if x < 340 else x-360) for x in origlon]
lat=population_data.lat_array
densities=population_data.density_array
elev=getelevationarray()
preedges = loadadjfromfile(adjfile)
adjlist = makeadjlist(len(lon),preedges)
mobdf = readmobility()

pthlist = []
ethlist = []
scorelist = []
cslist = []
intlist = []
bestscore = 100000
bpt = 0
bet = 0
bint = 0
bcluster = []
pottery = loadhexagons()
print('thresholds ',end='')
for eth in range(fromethresh,toethresh,stepethresh):
     print(f'{eth:4}',end='')
print()
for productthresh in range(frompthresh,topthresh,steppthresh):
    print(f'{productthresh:10} ',end='')
    for eth in range(fromethresh,toethresh,stepethresh):
        (score,matchcluster,intersect) = trythreshold(pottery,productthresh,eth,kya)
        print(f'{score:4}',end='')
#        print(productthresh,eth,score,len(matchcluster),intersect)
        pthlist.append(productthresh)
        ethlist.append(eth)
        scorelist.append(score)
        cslist.append(len(matchcluster))
        intlist.append(intersect)
        if score < bestscore:
            bestscore = score
            bpt = productthresh
            bet = eth
            bint = intersect
            bcluster = matchcluster
    print()

print(f'best hamming distance:{bestscore}, threshold: {bpt}')
print(f'cluster size:{len(bcluster)}, intersection size: {bint}')
filename = f'best{bpt}-{bet}.txt'
savehexagons(bcluster,filename)
caption = f'thresholds: {bpt},{bet}'
plotWE(pottery,bcluster,caption)
