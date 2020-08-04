from datetime import datetime
import gzip
import pandas as pd
import numpy as np

start = datetime.now()

f = gzip.open("crsp_daily.gz")
data = pd.read_csv(f)

print("Loading:", "\n", (datetime.now()-start).total_seconds())

start = datetime.now()

data['RET'] = pd.to_numeric(data['RET'], errors = "coerce")
data.dropna()
data['y'] = round(data.date/10000)
data.groupby(['PERMNO', 'y'])['RET'].agg(['mean', 'std', 'count'])

print("Processing:", "\n", (datetime.now()-start).total_seconds())
