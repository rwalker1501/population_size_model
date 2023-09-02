
import sys
from adjlib import *
from nvalslib import *
from poplib2 import *
from popdata import *
import matplotlib.pyplot as plt
from elevation import *
import os.path as path

cfname = 'best.txt'
if len(sys.argv)>1:
    cfname = sys.argv[1]

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

potteryfilename = "cardium.txt"

def loadhexagons(infile = potteryfilename):
    indexes = []
    if path.isfile(infile):
        with open(infile) as f:
             for x in f.read().splitlines():
                 indexes.append(int(x.split()[0]))
    return indexes

def clip(df):
   filterdf = df[(df['lat']>31) & (df['lat']<62) &
                 ((df['lon']>353) | (df['lon']< 60))]
   return filterdf

def plotWE():
    mapper = [0]*len(lon)
    pottery = loadhexagons()
    thecluster = loadhexagons(cfname)
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
    plt.title('Hamming Distance: '+str(hamming))
    plt.grid(True)
    values = df['pottery']
    colors = []
    for val in values:
        if val == 0:
            c = 'lightgrey'
        elif val == 1:
            c = 'cyan'
        elif val == 2:
            c = 'blue'
        else:
            c = '#7879FF'
        colors.append(c)
    plt.scatter(df['lon'], df['lat'], s=30, color=colors)
    plt.show()

base_path=''
population_data_name='Eriksson'
population_data=load_population_data_source(base_path, population_data_name)
lon=population_data.lon_array
lat=population_data.lat_array

plotWE()
