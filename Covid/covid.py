import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime

today = datetime.today()
today = 'Latest update: ' + str(today.day) + '-' + str(today.month) + '-' + str(today.year)

COLOR = '#F6F7EB'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
df = pd.read_csv(url, error_bad_lines=False)

df = df.loc[df['iso_code'].isin(['ESP','GBR','PER'])]
df['date'] = pd.to_datetime(df['date'])
df.index = pd.DatetimeIndex(df.pop('date'))
df = df.sort_index().last('30D')

# PNG

fig, ax = plt.subplots(figsize=(10,7));
df.groupby('iso_code').new_cases_smoothed.plot(ax=ax);
plt.legend(fancybox=True, framealpha=0.2);
plt.title('New cases last 30 days');
plt.text(0.7, 0, today, fontsize=10, transform=plt.gcf().transFigure)
plt.savefig('daily_cases_smooth.png', bbox_inches = 'tight', transparent=True);

fig, ax = plt.subplots(figsize=(10,7));
df.groupby('iso_code').new_cases.plot(ax=ax);
plt.legend(fancybox=True, framealpha=0.2);
plt.title('New cases last 30 days');
plt.text(0.7, 0, today, fontsize=10, transform=plt.gcf().transFigure)
plt.savefig('daily_cases.png', bbox_inches = 'tight', transparent=True);

fig, ax = plt.subplots(figsize=(10,7));
df.groupby('iso_code').new_deaths.plot(ax=ax);
plt.legend(fancybox=True, framealpha=0.2);
plt.title('New deaths last 30 days');
plt.text(0.7, 0, today, fontsize=10, transform=plt.gcf().transFigure)
plt.savefig('daily_deaths.png', bbox_inches = 'tight', transparent=True);

# SVG

fig, ax = plt.subplots(figsize=(10,7));
df.groupby('iso_code').new_cases_smoothed.plot(ax=ax);
plt.legend(fancybox=True, framealpha=0.2);
plt.title('New cases last 30 days\n7-day rolling average');
plt.text(0.7, 0, today, fontsize=10, transform=plt.gcf().transFigure)
plt.savefig('daily_cases_smooth.svg', bbox_inches = 'tight', transparent=True);

fig, ax = plt.subplots(figsize=(10,7));
df.groupby('iso_code').new_cases.plot(ax=ax);
plt.legend(fancybox=True, framealpha=0.2);
plt.title('New cases last 30 days');
plt.text(0.7, 0, today, fontsize=10, transform=plt.gcf().transFigure)
plt.savefig('daily_cases.svg', bbox_inches = 'tight', transparent=True);

fig, ax = plt.subplots(figsize=(10,7));
df.groupby('iso_code').new_deaths.plot(ax=ax);
plt.legend(fancybox=True, framealpha=0.2);
plt.title('New deaths last 30 days');
plt.text(0.7, 0, today, fontsize=10, transform=plt.gcf().transFigure)
plt.savefig('daily_deaths.svg', bbox_inches = 'tight', transparent=True);

fig, ax = plt.subplots(figsize=(10,7));
df.groupby('iso_code').new_deaths.plot(ax=ax);
plt.legend(fancybox=True, framealpha=0.2);
plt.title('New deaths last 30 days\n7-day rolling average');
plt.text(0.7, 0, today, fontsize=10, transform=plt.gcf().transFigure)
plt.savefig('daily_deaths_smooth.svg', bbox_inches = 'tight', transparent=True);
