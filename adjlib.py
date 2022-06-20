# import numpy as np
from math import radians, cos, sin, asin, sqrt, atan2, degrees
from nvalslib import getkya

def dist(lon1,lat1,lon2,lat2):
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
  dlon = lon2 - lon1 
  dlat = lat2 - lat1 
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a)) 
  r = 6371 # Radius of earth
  return c * r

def angle(lon1,lat1,lon2,lat2):
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
  dlon = lon2 - lon1 
  dlat = lat2 - lat1 
  bearing = atan2(sin(dlon)*cos(lat2),
                  cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(dlon))
  return (degrees(bearing) + 360) % 360

def makeadj(lon, lat, adjthresh = 150,
            centerlon = 355.877, centerlat = 43.377):
            
    edges = []
    n = len(lon)
    for i in range(n):
      x1 = lon[i]
      y1 = lat[i]
      for j in range(n):
        if (i != j):
          x2 = lon[j]
          y2 = lat[j]
          d2 = dist(x2,y2,centerlon,centerlat)
          d = dist(x1,y1,x2,y2)
          if d < adjthresh:
            edges.append(str(i)+' '+str(j))
                 
    return edges

def saveadj(edgesastext,outfile = "gui-adj.txt"):
 
    with open(outfile,'w') as f:
        for x in edgesastext:
           # print(>> f, x)
           print(x, end="\n", file=f)
           
def loadadjfromfile(adjfile = "out-adj.txt"):
    edges = []
    with open(adjfile) as f:
      for x in f.read().splitlines():
         edges.append(x)
    return edges
    
def nearestnode(centerlon, centerlat, lon, lat):
    n = len(lon)
    mindist = 1000000.0
    minindex = -1
    for i in range(n):
      x1 = lon[i]
      y1 = lat[i]
      d = dist(x1,y1,centerlon,centerlat)
      if (d < mindist):
         minindex = i
         mindist = d
    return minindex

def makeadjlist(numnodes,edgesastext):
    adjlist = []
    for i in range(numnodes):
       adjlist.append([])
    for x in edgesastext:
       [i,j] = [int(index) for index in x.split(' ')]
       adjlist[i].append(j)
    return adjlist

visited = []
def getcluster(adjlist, nearest):
    global visited
    n = len(adjlist)
    visited = []
    for i in range(n):
       visited.append(False)
    cluster = crawl(nearest,adjlist)
    return cluster

def crawldfs(v,adjlist):
   global visited
   result = []
   if (not visited[v]):
      visited[v] = True
      result = result + [v]
      for j in adjlist[v]:
         result = result + crawl(j,adjlist)
   return result

def crawl(v,adjlist):
   global visited
   result = []
   queue = [v]
   visited[v] = True
   while len(queue) > 0:
      p = queue.pop(0);
#     print(p,len(queue))
      result = result + [p]
      for j in adjlist[p]:
         if (not visited[j]):
            queue.append(j)
            visited[j] = True
   return result

def getclusterwithedges(adjlist, nearest):
    global visited
    n = len(adjlist)
    visited = []
    for i in range(n):
       visited.append(False)
    cluster,clusteredges = crawlwithedges(-1,nearest,adjlist)
    return cluster, clusteredges

def crawlwithedges(fromv,v,adjlist):
   global visited
   result = []
   resultedges = []
   if (visited[v]):
      resultedges = resultedges + [str(fromv)+" "+str(v)]
   else:
      visited[v] = True
      result = result + [v]
      if fromv != -1:
         resultedges = resultedges + [str(fromv)+" "+str(v)]
      for j in adjlist[v]:
         vv,ee = crawlwithedges(v,j,adjlist)
         result = result + vv
         resultedges = resultedges + ee
   return result,resultedges
   
   
def filterbypopproduct(alledges,lon,lat,kya,productthresh,densities):
    
    kyarec = getkya(kya,kya,densities)    
    snap = [int(x) for x in kyarec[0]]
    kya = snap[0]*25/1000.0

    # edges = loadadjfromfile("out-adj.txt")
    newedges = []
    for x in alledges:
        [i,j] = [int(y) for y in x.split(' ')]
        sq = snap[i-1]*snap[j-1]
        if sq >= productthresh:
           newedges.append(x)

    return newedges

def filterbygravity(alledges,lon,lat,kya,gravitythresh,densities):
    
    kyarec = getkya(kya,kya,densities)    
    snap = [int(x) for x in kyarec[0]]
    kya = snap[0]*25/1000.0

    # edges = loadadjfromfile("out-adj.txt")
    newedges = []
    for x in alledges:
        [i,j] = [int(y) for y in x.split(' ')]
        d = dist(lon[i],lat[i],lon[j],lat[j])
        sq = (snap[i-1]*snap[j-1])
        if d <= 0.01:
           newedges.append(x)
        else:
           if (sq/(d*d)) >= gravitythresh:
              newedges.append(x)

    return newedges

