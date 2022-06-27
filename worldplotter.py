import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import collections as mc
from moviepy.editor import *

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


def plotcluster(c,lon,lat,filename,caption):
   plt.figure()
   plt.scatter(lon, lat, cmap=plt.cm.Blues)
   clon = []
   clat = []
   for i in c:
      clon.append(lon[i])
      clat.append(lat[i])
   plt.scatter(clon, clat, cmap=plt.cm.Reds)
   plt.xlabel('longitude')
   plt.ylabel('latitude')
   plt.title(caption)
   plt.grid(True)
   plt.savefig(filename)
#   plt.show()
   plt.close()

def animate(filenames,movie):
   cliplist = []
   for f in filenames:
      ic = ImageClip(f).set_duration(1)
      cliplist.append(ic)
   video = concatenate(cliplist, method="compose")
   video.write_videofile(movie, fps=24)
