# Speed

I wanted to check how fast are the three main languages used in computational finance (Julia, Python, R) when loading and performing an operation on very large databases. For this, I used the "crsp_daily.gz" file, which holds historical data on daily stock prices. The file had a compressed weight of 1.03 GB, and contained over 97 million rows and 11 columns.

This was ran on an AWS Ubuntu machine with 8 cpu and 64gb RAM.