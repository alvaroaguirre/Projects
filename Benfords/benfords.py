import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# New cases
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
data = pd.read_csv(url, error_bad_lines=False)
df = data.dropna(subset=['new_cases'])
df = df[df.new_cases> 0]
df['Benford'] = df.apply(lambda row: int(str(row.new_cases).replace('0','').replace('.','')[0]), axis = 1)
benfords_law_new_cases = round((df.Benford.value_counts() / len(df.Benford))*100,2)

# Total cases
df = data.dropna(subset=['total_cases_per_million'])
df = df[df.total_cases_per_million> 0]
df['Benford'] = df.apply(lambda row: int(str(row.total_cases_per_million).replace('0','').replace('.','')[0]), axis = 1)
benfords_law_total_cases = round((df.Benford.value_counts() / len(df.Benford))*100,2)

# Benford's Law theoretical distirbution
benfords_law_theory = pd.Series([30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6])
benfords_law_theory.index = range(1,10)

fig = plt.figure(figsize=(12,8), dpi= 100, facecolor='w', edgecolor='k')
plt.rcParams.update({'font.size': 20})
ax = plt.subplot(111)
ax.bar(benfords_law_new_cases.index - 0.2, benfords_law_new_cases, width = 0.4, align='center', 
       label = 'Daily new cases', color = '#DDD8C4')
ax.bar(benfords_law_new_cases.index, benfords_law_total_cases, width = 0.4, align='center', 
       label = 'Total cases per million', color = '#A3C9A8')
ax.bar(benfords_law_new_cases.index + 0.2, benfords_law_theory, width = 0.4, align='center', 
       label = "Benford's law", color ='#50808E')
plt.title("Benford's Law and Corona")
plt.xlabel("Leading digit")
plt.ylabel("Frequency (in %)")
plt.xticks(benfords_law_new_cases.index)
ax.legend()
plt.show()
fig.savefig('benford_corona.png', bbox_inches="tight")
fig.savefig('benford_corona.svg', bbox_inches="tight")




