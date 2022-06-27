import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import collections as mc
from moviepy.editor import *

def plotworld(c1,c2,c3,lon,lat,filename,caption):
   plt.figure()
   plt.scatter(lon, lat, color='blue')
   clon = []
   clat = []
   for i in c2:
      clon.append(lon[i])
      clat.append(lat[i])
   plt.scatter(clon, clat, color='red')
   clon = []
   clat = []
   for i in c3:
      clon.append(lon[i])
      clat.append(lat[i])
   plt.scatter(clon, clat, color='green')
   plt.xlabel('longitude')
   plt.ylabel('latitude')
   plt.title(caption)
   plt.grid(True)
   plt.savefig(filename)
#   plt.show()
   plt.close()

def plotcluster(c,lon,lat,filename,caption):
   plt.figure()
   plt.scatter(lon, lat, color='blue')
   clon = []
   clat = []
   for i in c:
      clon.append(lon[i])
      clat.append(lat[i])
   plt.scatter(clon, clat, color='red')
   plt.xlabel('longitude')
   plt.ylabel('latitude')
   plt.title(caption)
   plt.grid(True)
   plt.savefig(filename)
#   plt.show()
   plt.close()

def plotworldclusters(clusters,lon,lat,filename,caption):
   plt.figure()
   plt.scatter(lon, lat, color='blue') # default color
   for c in clusters:
      if len(c) > 1: # plot only for non-single-cell clusters
         clon = []
         clat = []
         for i in c:
            clon.append(lon[i])
            clat.append(lat[i])
         plt.scatter(clon, clat)
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
