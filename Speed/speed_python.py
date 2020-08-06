from datetime import datetime
import gzip
import pandas as pd
import numpy as np

# Loading uncompressed
start = datetime.now()
data = pd.read_csv("crsp_daily")
load_uncomp = (datetime.now()-start).total_seconds()

print("output,Python,read_uncompressed,", load_uncomp)

# Processing

data['RET'] = pd.to_numeric(data['RET'], errors = "coerce")
data.dropna()
data['year'] = round(data.date/10000)

start = datetime.now()
data.groupby(['PERMNO', 'year'])['RET'].agg(['mean', 'std', 'count'])
processing = (datetime.now()-start).total_seconds()

print("output,Python,process,", processing)




