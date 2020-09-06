import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
import os

source_file = os.path.dirname(os.path.abspath(__file__))

today = datetime.now()
today = 'Latest update: \n' + str(today.day) + '-' + str(today.month) + '-' + str(today.year) 

COLOR = '#252627'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR
mpl.rcParams['font.size'] = 16
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['#BB0A21', '#4B88A2', '#D3D4D9']) 
mpl.rcParams['lines.linewidth'] = 2

url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
df = pd.read_csv(url, error_bad_lines=False)

df = df.loc[df['iso_code'].isin(['ESP','GBR','PER'])]
df['date'] = pd.to_datetime(df['date'])
df.index = pd.DatetimeIndex(df.pop('date'))
df = df.sort_index().last('30D')

fig, ax = plt.subplots(figsize=(10,7));
df.groupby('iso_code').new_cases_smoothed.plot(ax=ax);
plt.legend(fancybox=True, framealpha=0.2);
plt.title('New cases last 30 days\n7-day rolling average');
plt.text(0.1, 0, today, fontsize=10, transform=plt.gcf().transFigure)
plt.savefig(source_file + '/daily_cases_smooth.svg', bbox_inches = 'tight', transparent=True);

fig, ax = plt.subplots(figsize=(10,7));
df.groupby('iso_code').new_cases.plot(ax=ax);
plt.legend(fancybox=True, framealpha=0.2);
plt.title('New cases last 30 days');
plt.text(0.1, 0, today, fontsize=10, transform=plt.gcf().transFigure)
plt.savefig(source_file + '/daily_cases.svg', bbox_inches = 'tight', transparent=True);

fig, ax = plt.subplots(figsize=(10,7));
df.groupby('iso_code').new_deaths.plot(ax=ax);
plt.legend(fancybox=True, framealpha=0.2);
plt.title('New deaths last 30 days');
plt.text(0.1, 0, today, fontsize=10, transform=plt.gcf().transFigure)
plt.savefig(source_file + '/daily_deaths.svg', bbox_inches = 'tight', transparent=True);

fig, ax = plt.subplots(figsize=(10,7));
df.groupby('iso_code').new_deaths_smoothed.plot(ax=ax);
plt.legend(fancybox=True, framealpha=0.2);
plt.title('New deaths last 30 days\n7-day rolling average');
plt.text(0.1, 0, today, fontsize=10, transform=plt.gcf().transFigure)
plt.savefig(source_file + '/daily_deaths_smooth.svg', bbox_inches = 'tight', transparent=True);
