# Creating a clickable map using Folium
from collections import defaultdict

import branca.colormap
import folium
import pandas as pd
import numpy as np
from folium.plugins import HeatMap

# This loads the world map
m = folium.Map(location=[52.1326, 5.2913], zoom_start=5)

folium.TileLayer('Stamen Terrain').add_to(m)
folium.TileLayer('Stamen Toner').add_to(m)
folium.TileLayer('Stamen Water Color').add_to(m)
folium.TileLayer('cartodbpositron').add_to(m)
folium.TileLayer('cartodbdark_matter').add_to(m)

# HeatMap data
data = (
        np.random.normal(size=(100, 3)) *
        np.array([[1, 1, 1]]) +
        np.array([[48, 5, 1]])
).tolist()

steps = 20
colormap = branca.colormap.linear.YlOrRd_09.scale(0, 1).to_step(steps)
gradient_map = defaultdict(dict)
for i in range(steps):
    gradient_map[1 / steps * i] = colormap.rgb_hex_str(1 / steps * i)
colormap.add_to(m)  # add color bar at the top of the map

HeatMap(data, gradient=gradient_map).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))

folium.LayerControl().add_to(m)

# Reads in a test file
geo_df1 = pd.read_excel('geo_supplier_data.xlsx')

# Creates a dataframe with the location by zipping latitude and longitude
df = geo_df1.assign(location=[*zip(geo_df1.Latitude, geo_df1.Longitude)])

suppliers = df['location'].to_numpy()

# Create the hyperlink for the markers
href_b = "<a href="
href_e = "</a>"
goog = "https://en.wikipedia.org/wiki/"

# Turns the text field of the df into the hyperlink
df['Text'] = href_b + goog + df['City'] + ">" + df['City'] + href_e

# Create markers for each row.
for i, r in df.iterrows():
    folium.Marker(location=r['location'],
                  popup=r['Text'],
                  tooltip='Click For Info').add_to(m)
    folium.Circle(r['location'],
                  radius=25000
                  ).add_to(m)

clients = [(48.85, 2.35), (43.29, 5.36)]
supplier = (52.37, 4.9)


# Colors based on how sustainable can stuff be

for i in clients:
    coordinates = [supplier, i]
    folium.PolyLine(coordinates, color="blue", weight=5, opacity=1).add_to(m)

print(suppliers)
# folium.PolyLine(coordinates, color="blue", weight=5, opacity=1).add_to(m)


# Save the map to an html
m.save('testMap.html')
