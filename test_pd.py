import pandas as pd
import os
import numpy as np
data = pd.read_csv( os.getcwd()+"/embed-vecs.csv")


photo_dir= os.getcwd() +"photos"

print(np.array(data.iloc[0][:]))