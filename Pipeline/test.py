
import random
import time
import context
import pandas as pd
import pickle
l=[]
df = pd.read_csv("/home/celebal/Data/companies_data.csv")
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1920, 1080))  
display.start()

#try:
for i in range(114, len(df)):
    company = df.iloc[i, 3]
    website = df.iloc[i, 0]
    obj = context.context(company,website,100)
    l.append(obj.Ditribute())
    pickle.dump(l, open('outputs/context_output.pkl', 'wb'))
    min = random.randint(1,2)
    time.sleep(min*60)
#except Exception as e:
    #display.stop()
    #file = open('logs/context.txt','a')
    #file.write(str(e))
    #file.close()
display.stop()