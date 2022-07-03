
def getcolor(clustercolor):
   clist = ['red','yellow','orange','green','cyan','magenta', 'gold',
            'forestgreen','teal','purple','coral','lawngreen','pink',
            'brown','gold','darkkhaki','darkgreen','skyblue','plum','hotpink',
            'salmon','tan','palegreen','navy','violet','lime','lavender'
           ]
   n = len(clist)
   index = clustercolor % n
#   print(clist[index])
   return clist[index]

def zerotag():
   return -1

def zerocolor():
   return "grey"

def nonzerotag():
   return -2

def nonzerocolor():
   return "blue"

