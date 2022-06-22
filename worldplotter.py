import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import collections as mc

def plotworld(c1,c2,c3,lon,lat,filename,caption):
   plt.figure()
   plt.scatter(lon, lat, cmap=plt.cm.Blues)
   clon = []
   clat = []
   for i in c2:
      clon.append(lon[i])
      clat.append(lat[i])
   plt.scatter(clon, clat, cmap=plt.cm.Reds)
   clon = []
   clat = []
   for i in c3:
      clon.append(lon[i])
      clat.append(lat[i])
   plt.scatter(clon, clat, cmap=plt.cm.Greens)
   plt.xlabel('longitude')
   plt.ylabel('latitude')
   plt.title(caption)
   plt.grid(True)
   plt.savefig(filename)
#   plt.show()
   plt.close()


