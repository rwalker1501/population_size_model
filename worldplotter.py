import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import collections as mc
from moviepy.editor import *
import colorconsts

def plotworld(c1,c2,c3,origlon,lat,filename,caption):
   plt.figure()
   lon = [(x if x < 340 else x-360) for x in origlon]
   plt.scatter(lon, lat, s=1, color='blue')
   clon = []
   clat = []
   for i in c2:
      clon.append(lon[i])
      clat.append(lat[i])
   plt.scatter(clon, clat, s=1, color='red')
   clon = []
   clat = []
   for i in c3:
      clon.append(lon[i])
      clat.append(lat[i])
   plt.scatter(clon, clat, s=1, color='green')
   plt.xlabel('longitude')
   plt.ylabel('latitude')
   plt.title(caption)
   plt.grid(True)
   plt.savefig(filename)
#   plt.show()
   plt.close()

def plotcluster(c,origlon,lat,filename,caption):
   plt.figure()
   lon = [(x if x < 340 else x-360) for x in origlon]
   plt.scatter(lon, lat, s=1, color='blue')
   clon = []
   clat = []
   for i in c:
      clon.append(lon[i])
      clat.append(lat[i])
   plt.scatter(clon, clat, s=1, color='red')
   plt.xlabel('longitude')
   plt.ylabel('latitude')
   plt.title(caption)
   plt.grid(True)
   plt.savefig(filename)
#   plt.show()
   plt.close()

def plotworldclusters(clusters,colors,origlon,lat,filename,caption):
   lon = [(x if x < 340 else x-360) for x in origlon]
   plt.figure()
   plt.scatter(lon, lat, s=1, color=colorconsts.nonzerocolor())
   # default color for singletons
   clon = []
   clat = []
   n = len(clusters)
   for i in range(n):
      c = colors[i]
      if c == colorconsts.zerotag():
         cellindex = clusters[i][0]
         clon.append(lon[cellindex])
         clat.append(lat[cellindex])
   # color the zero pop singletons differently
   plt.scatter(clon, clat, s=1, color = colorconsts.zerocolor())
   cycle = 0
   for i in range(n):
      c = clusters[i]
      clustercolor = colors[i]
      if len(c) > 1:
         clon = []
         clat = []
         for i in c:
            clon.append(lon[i])
            clat.append(lat[i])
         availcolor = colorconsts.getcolor(clustercolor)
         plt.scatter(clon, clat, s=1, color = availcolor)
         cycle = cycle + 1
         
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
