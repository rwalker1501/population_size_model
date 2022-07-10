
from popdata import *

# the following code tests the contents of loaded populations
# against output of clusterplot.py for the following params:
# centerlon = 355.877
# centerlat = 43.377
# adjthresh = 150
# fromkya = 36
# tokya = 35.6
# productthresh = 20000000

base_path = ''
filename = 'pop-adj150-prod20000000'
popload = loadpopcomputations(base_path)

print("test loaded values...")
for i in range(4644,4660):
   print(i,"population:",popload[i][5864])


