
import math
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
frompthresh =  3000000
topthresh =   10000000
steppthresh =  1000000
fromethresh = 300
toethresh =   500
stepethresh =  25

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
                    elevmax = max(elev[p],elev[j])
                    if (sq >= productthresh) and (elevmax < ethresh):
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


numquarters = 6084
ix = int(numquarters-1 - kya*40)
def fixlat0cross(x):
    if x > 350:
        return x-360
    if x < -350:
        return x+360
    return x

# angle formed by vector pointing to left from center and neighbor
def angle(neighbor,center):
    pointx = fixlat0cross(lon[neighbor]-lon[center])
    pointy = fixlat0cross(lat[neighbor]-lat[center])
    num = -1*pointx + 0*pointy
    denom = math.sqrt(pointx*pointx+pointy*pointy)
    angle = np.arccos(num/denom)
    angle = 180*angle/math.pi
#    print(f"{angle:.2f},{pointx:.2f},{pointy:.2f}")
    if pointy < 0:
       angle = 360-angle
    return angle

# angle formed by vector pointing to left from center and neighbor
# def angle(neighbor,center):
#     deltaL = lat[neighbor]-lat[center]
#     x = math.cos(lon[neighbor]*math.sin(deltaL))
#     yleft = math.cos(lon[center])*math.sin(lon[neighbor])
#     yright = math.sin(lon[center])*math.cos(lon[neighbor])*math.cos(deltaL)
#     y = yleft - yright
#     beta = math.atan2(x,y)
#     return 180*beta/math.pi

def dd(cell):
    if cell == -1:
        return "     "
    else:
        return f"{densities[ix][cell]:6.1f}"

def ee(cell):
    if cell == -1:
        return "     "
    else:
        return f"{elev[cell]:6.1f}"

# def arrange(cells,center):
#     pad = [-1]*6
#     for c in cells:
#         cellangle = angle(c,center)
#         cellangle = cellangle - 30
#         cellangle = cellangle if cellangle >= 0 else 360+cellangle
#         
#         print(f"*** {cellangle:.2f} [{pizzacut}]")
#         pad[pizzacut] = c
#     return pad

def stretch(trips):
    if (len(trips)==6):
        return trips
    gaps = 6 - len(trips)
    answer = []
    i = 0
    for t in trips:
        if t[2] <= i:
            answer.append(t)
            i = i + 1
        else:
            pad = t[2]-i
            if pad >= gaps:
                pad = gaps
            if (pad > 0):
                answer = answer +[(-1,-1,-1)]*pad
                i = i + pad
                gaps = gaps - pad
            answer.append(t)
            i = i + 1
    answer = answer + [(-1,-1,-1)]*(6-len(answer))
    return answer

def arrange(cells,center):
    trips = []
    for c in cells:
        cellangle = angle(c,center)
        cellangle = cellangle - 30
        cellangle = cellangle if cellangle >= 0 else 360+cellangle
        pizzacut = int(cellangle) // 60
#        print(f"*** {cellangle:.2f} [{pizzacut}]")
        trips.append((c,cellangle,pizzacut))
    trips.sort(key=lambda x: x[1])
    trips = stretch(trips)
#    print(trips)
    sortedcells = [x[0] for x in trips]
    return sortedcells

def displaywithneighbors(center,neighbors):
     nb = arrange(neighbors,center)
     print("----------------------------------")
     print(f"      {dd(nb[0])}         {dd(nb[1])}")
     print(f"      {ee(nb[0])}         {ee(nb[1])}")
     print(f"{dd(nb[5])}         {dd(center)}      {dd(nb[2])}")
     print(f"{ee(nb[5])}         {ee(center)}      {ee(nb[2])}")
     print(f"      {dd(nb[4])}         {dd(nb[3])}")
     print(f"      {ee(nb[4])}         {ee(nb[3])}")
     print("----------------------------------")

def onclick(event):
    if event.button == 1:
        x = event.xdata
        y = event.ydata
#        print(f"x={x:.2f},y={y:.2f}")
        p = nearestnode(x,y,lon,lat)
#        print(f"lon={lon[p]:.2f},lat={lat[p]:.2f}")
        displaywithneighbors(p,adjlist[p])

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

    fig = plt.figure()
    fig.canvas.mpl_connect('button_press_event',onclick)

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
    color_meanings={
        'lightgrey':'No Intersection',
        'cyan':'Pottery',
        'blue': 'Inferred cluster',
        'black': 'Intersection'}
    for val in values:
        if val == 0:
            c = 'lightgrey' #bg - #D3D3D3
        elif val == 1:
            c = 'cyan'
        elif val == 2:
            c = 'blue' 
        else:
            c = 'black' # intersection 
        colors.append(c)
    plt.scatter(df['lon'], df['lat'], s=30, color=colors)
    # Create legend for each unique color
    for color, label in color_meanings.items():
        plt.scatter([], [], c=color, s=100, label=label)
    plt.legend(loc='upper right')
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
savehexagons(bcluster,'best.txt')
caption = f'thresholds: {bpt},{bet}'
plotWE(pottery,bcluster,caption)
