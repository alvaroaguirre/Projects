from datetime import datetime
import gzip
import pandas as pd
import numpy as np

# Loading compressed

start = datetime.now()
f = gzip.open("crsp_daily.gz")
data = pd.read_csv(f)
load_comp = (datetime.now()-start).total_seconds()

print("output,Python,read_compressed,", load_comp)
