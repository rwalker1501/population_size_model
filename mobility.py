import pandas as pd

def readmobility():
   df = pd.read_csv('population_data/mobility.csv')
   return df

def getmobility(df,ya):
   maxya = max(df['ya'])
   minya = min(df['ya'])
   index = ((ya+50)//100)*100
   if ya > maxya:
      index = maxya
   if ya < minya:
      index = minya
   mobility = df[df.ya==index]['mobility'].values[0]
   if mobility < 1:
      mobility = 1
   return mobility

def testcases():
   df = readmobility()
   print(df.head())
   print(getmobility(df,14001))
   print(getmobility(df,14000))
   print("---")
   print(getmobility(df,2000))
   print(getmobility(df,1990))
   print("---")
   print(getmobility(df,13490))
   print(getmobility(df,13500))
   print(getmobility(df,13540))
   print("---")
   print(getmobility(df,13550))
   print(getmobility(df,13560))
   print(getmobility(df,13600))
   print(getmobility(df,13610))

# testcases()
