
import sys
from adjlib import *
from nvalslib import *
from poplib2 import *
from popdata import *
import matplotlib.pyplot as plt
from elevation import *
import os.path as path

potteryfilename = "cardium2.txt"

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
                 indexes.append(x.split()[0])
    return indexes

def clip(df):
   filterdf = df[(df['lat']>31) & (df['lat']<62) &
                 ((df['lon']>353) | (df['lon']< 60))]
   return filterdf

zeroes = []

def onclick(event):
    if event.button == 1:
        x = event.xdata
        y = event.ydata
        # print(x,y)
        ix = nearestnode(x,y,lon,lat)
        zeroes[ix] = 1 - zeroes[ix]
        redraw()

def onclose(event):
    print('saving pottery file ...')
    n = len(zeroes)
    indexes = []
    for i in range(n):
        if (zeroes[i] == 1):
            indexes.append(i)
            # print(i,lon[i],lat[i])
    savehexagons(indexes)

def redraw():
    unclippeddf = pd.DataFrame({'lon':lon,'lat':lat,'pottery':zeroes})
    unclippeddf['lon'] = [(x if x < 340 else x-360) for x in unclippeddf['lon']]
    df = clip(unclippeddf)
    plt.clf()
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.title('POTTERY')
    plt.grid(True)
    values = df['pottery']
    colors = ['green' if val == 1 else 'lightblue' for val in values]
    plt.scatter(df['lon'], df['lat'], s=30, color=colors)
    plt.draw()

def plotWE():
    fig = plt.figure()
    fig.canvas.mpl_connect('button_press_event',onclick)
    fig.canvas.mpl_connect('close_event', onclose)
    global zeroes
    zeroes = [0]*len(lon)
    indexes = loadhexagons()
    for i in indexes:
        zeroes[int(i)] = 1
    redraw()
    plt.show()
    plt.close()

base_path=''
population_data_name='Eriksson'
population_data=load_population_data_source(base_path, population_data_name)
lon=population_data.lon_array
lat=population_data.lat_array

plotWE()
