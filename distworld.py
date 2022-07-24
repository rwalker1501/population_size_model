import sys
from adjlib import *
from nvalslib import *
from poplib2 import *
from classes_module import Target, PopulationData
from popdata import *
from worldplotter import *
import matplotlib.pyplot as plt

def allproducts(nums,edgesastext):
    products = []
    for x in edgesastext:
       [i,j] = [int(index) for index in x.split(' ')]
       products.append(nums[i]*nums[j])
    return products

def plothistos(nums,products,filename,caption):
   plt.figure()
   fig, (subfig1, subfig2) = plt.subplots(2)
   fig.tight_layout(pad=3.0)
   nums = [i for i in nums if i > 0]
   products = [i for i in products if i > 0]
   subfig1.hist(nums,bins=100)
   subfig1.set_title('Densities '+caption)
   subfig2.hist(products,bins=100)
   subfig2.set_title('Products')
   plt.savefig(filename)
   plt.close()

base_path='smb://127.0.0.1/Google Drive/My Drive/Documents 2022/Human exceptionalism/Population size/John Vergara Model/POPESTNew/'
base_path=''
population_data_name='Eriksson'
population_data=load_population_data_source(base_path, population_data_name)

adjthresh = 150 # change to 300 if you want more adjacencies
#fromkya = 36.4
#tokya = 36
#step = 1
fromkya = 120
tokya = 0
step = 40

if (len(sys.argv)>1):
  adjthresh = int(sys.argv[1])
if (len(sys.argv)>2):
  fromkya = int(sys.argv[2])
if (len(sys.argv)>3):
  tokya = int(sys.argv[3])

adjfile = "population_data/all-adj.txt"
if adjthresh == 300:
   adjfile = "population_data/all-adj300.txt"

print("Parameters")
print(" ---")
print(" Adjacency threshold", adjthresh)
print(" From (kiloyears ago)", fromkya)
print(" To   (kiloyears ago)", tokya)
print()
 
lon=population_data.lon_array
lat=population_data.lat_array
densities=population_data.density_array

edges = loadadjfromfile(adjfile)

numquarters = 6084
first = int(numquarters-1 - fromkya*40)
last = int(numquarters-1 - tokya*40)

print("time indexes:",first,last)

images = []
counter = 1
for ix in range(first,last,step):
   ya = (numquarters-1 - ix)*25
   print(ix,"(",ya,"years ago )")
   caption = str(ya) + " years ago"
   ix0 = f'{counter:02d}'+'-'
   filename = "PLOTS/histo"+ix0+str(ya)+"ya.png"
   images.append(filename)
   products = allproducts(densities[ix],edges)
   plothistos(densities[ix],products,filename,caption)
   counter = counter+1

animate(images,"PLOTS/histmovie.mp4")

