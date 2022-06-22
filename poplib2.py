from adjlib import *
from nvalslib import *

def popbyadj(lon,lat,nearest,kya,edges,densities):
    adjlist = makeadjlist(len(lon),edges)
    clusterindexes = getcluster(adjlist,nearest)
    # print(" Number of node-pairs (connections) within adjacency threshold", len(edges))
    poparray = getonepoparray(kya,densities)
    popsize = sumpop(poparray,clusterindexes)
    clustersize = len(clusterindexes)
    return clustersize,popsize,clusterindexes

def popbyproduct(lon,lat,nearest,kya,preedges,productthresh,densities):
    edges = filterbypopproduct(preedges,lon,lat,kya,productthresh,densities)
    # print(" Number of connections after product filter", len(edges))
    adjlist = makeadjlist(len(lon),edges)
    clusterindexes = getcluster(adjlist,nearest)
    poparray = getonepoparray(kya,densities)
    popsize = sumpop(poparray,clusterindexes)
    clustersize = len(clusterindexes)
    return clustersize,popsize,clusterindexes


def popbygravity(lon,lat,nearest,kya,preedges,gravitythresh,densities):
    edges = filterbygravity(preedges,lon,lat,kya,gravitythresh,densities)
    # print(" Number of connections after gravity filter", len(edges))
    adjlist = makeadjlist(len(lon),edges)
    clusterindexes = getcluster(adjlist,nearest)
    poparray = getonepoparray(kya,densities)
    popsize = sumpop(poparray,clusterindexes)
    clustersize = len(clusterindexes)
    return clustersize,popsize,clusterindexes
