
import sys
import math
from adjlib import *
from nvalslib import *
from poplib2 import *
from popdata import *
import matplotlib.pyplot as plt
from elevation import *
from mobility import *
import os.path as path
from matplotlib.widgets import TextBox

center = 7944
potteryfilename = "cardium.txt"
kya = 8
numquarters = 6084
ix = int(numquarters-1 - kya*40)
print(f"kiloyears ago: {kya}, index: {ix}");

productthresh = 5000000
elevthresh = 360
def connected(a,b):
    sq = densities[ix][a]*densities[ix][b]
    elevdiff = abs(elev[a]-elev[b])
    return (sq >= productthresh) and (elevdiff < elevthresh)

def buildcluster(index):
    cluster = {index}
    queue = [index]
    while len(queue) > 0:
        p = queue.pop(0)
        for j in adjlist[p]:
            if connected(p,j):
                if not j in cluster:
                    cluster.add(j)
                    queue.append(j)
    return cluster

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

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
    print(f"      [{nb[0]}]         [{nb[1]}]")
    print(f"      {dd(nb[0])}         {dd(nb[1])}")
    print(f"      {ee(nb[0])}         {ee(nb[1])}")
    print(f"[{nb[5]}]         [{center}]      [{nb[2]}]")
    print(f"{dd(nb[5])}         {dd(center)}      {dd(nb[2])}")
    print(f"{ee(nb[5])}         {ee(center)}      {ee(nb[2])}")
    print(f"      [{nb[4]}]         [{nb[3]}]")
    print(f"      {dd(nb[4])}         {dd(nb[3])}")
    print(f"      {ee(nb[4])}         {ee(nb[3])}")
    print("----------------------------------")

def onclick(event):
    if event.inaxes is not None and event.inaxes == pbox:
#        print("p Textbox clicked")
        ptextbox.set_active(True)
    elif event.inaxes is not None and event.inaxes == ebox:
#        print("e Textbox clicked")
        etextbox.set_active(True)
    else:
        if event.button == 1:
            x = event.xdata
            y = event.ydata
    #        print(f"x={x:.2f},y={y:.2f}")
            global center
            center = nearestnode(x,y,lon,lat)
    #        print(f"lon={lon[p]:.2f},lat={lat[p]:.2f}")
            redraw(center)
            displaywithneighbors(center,adjlist[center])

pbox = None
ptextbox = None
ebox = None
etextbox = None

def redraw(centerindex):
    mapper = [0]*len(lon)
    pottery = loadhexagons()
    thecluster = buildcluster(centerindex)
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
    plt.clf()
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
    global pbox
    global ptextbox
    global ebox
    global etextbox
    pbox = plt.axes([0.24, 0.83, 0.15, 0.04])
    ptextbox = TextBox(pbox, 'product:', initial=str(productthresh))
    ptextbox.on_submit(update_pthresh)
    ebox = plt.axes([0.24, 0.78, 0.15, 0.04])
    etextbox = TextBox(ebox, 'elevation:', initial=str(elevthresh))
    etextbox.on_submit(update_ethresh)

    plt.draw()


def plotWE():
    fig = plt.figure()
    fig.canvas.mpl_connect('button_press_event',onclick)
    redraw(center)
    plt.show()
    plt.close()

def update_pthresh(text):
    global productthresh
    productthresh = int(text)
    redraw(center)

def update_ethresh(text):
    global elevthresh
    elevthresh = int(text)
    redraw(center)

base_path=''
population_data_name='Eriksson'
population_data=load_population_data_source(base_path, population_data_name)
lon=population_data.lon_array
lat=population_data.lat_array

adjfile = "population_data/all-adj.txt"
densities = population_data.density_array
elev = getelevationarray()
preedges = loadadjfromfile(adjfile)
adjlist = makeadjlist(len(lon),preedges)
mobdf = readmobility()

plotWE()
