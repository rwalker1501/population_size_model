# =============================================================================
# def getkya(fromkya,tokya,nvals):   
#     
#     nvals = "DATA/N_Vals.txt"
#     numlines = 6084
#     fromlinenum = numlines - fromkya*40
#     tolinenum = numlines - tokya*40
# 
#     kyarec = []
#     with open(nvals) as f:
#        countl = 0
#        for recs in f.read().splitlines():
#          countl = countl + 1
#          if countl >= fromlinenum:
#            kyarec.append(recs)
#          if countl >= tolinenum:
#            break
#           
#     return kyarec
# =============================================================================

def getkya(fromkya,tokya,densities):   
    
    
    numlines = 6084
    fromlinenum = int(numlines - fromkya*40)
    tolinenum = int(numlines - tokya*40)
    kyarec=densities[fromlinenum:tolinenum+1]
# =============================================================================
#     with open(nvals) as f:
#        countl = 0
#        for recs in f.read().splitlines():
#          countl = countl + 1
#          if countl >= fromlinenum:
#            kyarec.append(recs)
#          if countl >= tolinenum:
#            break
#           
# =============================================================================
    return kyarec


def getonepoparray(kya,densities):
   kyarec = getkya(kya,kya,densities)
#   snap = [int(x) for x in kyarec[0].split()]
   snap = [int(x) for x in kyarec[0]]
   return snap

def sumpop(poparray, indexes):
    sum = 0
    for i in indexes:
       sum = sum + poparray[i]
    return sum