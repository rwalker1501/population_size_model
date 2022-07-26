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
    #In some cases a target cell has 0 population (sometimes because it has a sea border)
    # In this case we replace the recorded population with the mean of all immediately adjacent cells
    # This means the clustef is likely to be a lot bigger
    kyarec = getkya(kya,kya,densities)    
    snap = [int(x) for x in kyarec[0]]
    pop_nearest=snap[nearest]
    mean_pop=0
    if pop_nearest==0:
        total_pop=0
        immediates=gettrueadjacents (preedges, nearest)
        for aCell in immediates:
            total_pop=total_pop+snap[aCell]
        mean_pop=total_pop/len(immediates)
    edges = filterbypopproduct(preedges,lon,lat,kya,productthresh,densities,nearest,mean_pop)
    # print(" Number of connections after product filter", len(edges))
    adjlist = makeadjlist(len(lon),edges)
    clusterindexes = getcluster(adjlist,nearest)
    poparray = getonepoparray(kya,densities)
    popsize = sumpop(poparray,clusterindexes)+mean_pop
    clustersize = len(clusterindexes)
    return clustersize,popsize,clusterindexes

def popbyproductonetimeindex(lon,lat,nearest,ix,preedges,productthresh,densities):
    edges = filterbypopproductindex(preedges,lon,lat,ix,productthresh,densities)
    # print(" Number of connections after product filter", len(edges))
    adjlist = makeadjlist(len(lon),edges)
    clusterindexes = getcluster(adjlist,nearest)
    poparray = densities[ix]
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
