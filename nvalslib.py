
def getkya(fromkya,tokya,densities):   
    numlines = 6084
    fromlinenum = int(numlines - fromkya*40)
    tolinenum = int(numlines - tokya*40)
    kyarec=densities[fromlinenum:tolinenum+1]
    return kyarec

def getonepoparray(kya,densities):
   kyarec = getkya(kya,kya,densities)
   snap = [int(x) for x in kyarec[0]]
   return snap

def sumpop(poparray, indexes):
    sum = 0
    for i in indexes:
       sum = sum + poparray[i]
    return sum
