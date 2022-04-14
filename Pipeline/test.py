
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
for i in range(200, len(df)):
    start = time.time()
    company = df.iloc[i, 3]
    website = df.iloc[i, 0]
    obj = context.context(company,website,100)
    l.append(obj.Ditribute())
    end = time.time()
    file = open('/home/celebal/Pipeline/logs/context.txt','a')
    file.write('Time taken for {} company = {} min\n'.format(company,(end-start)/60))
    pickle.dump(l, open('outputs/context_output.pkl', 'wb'))
    #min = random.randint(1,2)
    #time.sleep(min*60)
#except Exception as e:
    #display.stop()
    #file = open('logs/context.txt','a')
    #file.write(str(e))
    #file.close()
display.stop()