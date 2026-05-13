# -*- coding: utf-8 -*-
from skyfield.api import EarthSatellite, load
import pandas as pd
import matplotlib.pyplot as plt


tle_file = r'C:\Users\PARSIAN-IT\Desktop\iss_tle_2005_2025\iss_tle_2005_2025.txt'

with open(tle_file, 'r') as f:
    lines = f.readlines()

tle_pairs = []
i = 0
while i < len(lines) - 1:
    line1 = lines[i].strip()
    line2 = lines[i+1].strip()
    if line1.startswith("1 25544") and line2.startswith("2 25544"):
        tle_pairs.append((line1, line2))
        i += 2
    else:
        i += 1  


ts = load.timescale()


data = []
for line1, line2 in tle_pairs:
    try:
        satellite = EarthSatellite(line1, line2, 'ISS', ts)
        epoch = satellite.epoch.utc_datetime()
        a = satellite.model.a       
        e = satellite.model.ecco    
        r_earth_km = 6378.137 #redous for earth plant (in Agu 2025 year)  
        mean_altitude = a * r_earth_km * (1 - e**2) - r_earth_km
        data.append((epoch, mean_altitude))
    except:
        continue  

df = pd.DataFrame(data, columns=['Date', 'Altitude_km'])
df.sort_values('Date', inplace=True)

df.to_csv('ISS_Orbital_Altitude_2005_2025.csv', index=False)

plt.figure(figsize=(16, 8))
plt.plot(df['Date'], df['Altitude_km'], color='blue', linewidth=1)
plt.title('ISS Orbital Altitude (2005–2025)', fontsize=16)

plt.xlabel('Date (UTC)', fontsize=14)
plt.ylabel('Mean Orbital Altitude (km)', fontsize=14)
plt.grid(True)

plt.tight_layout()

plt.savefig('ISS_Real_Orbital_Decay.png', dpi=300)
plt.show()



#---
